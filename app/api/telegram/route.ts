import { NextRequest, NextResponse } from "next/server";
import { OpenAI } from "openai";
import TelegramBot from "node-telegram-bot-api";
import path from "path";
import fs from "fs";

// Load initial context
const initialContext = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), "data/initial-context.json"), "utf8")
);

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

// Initialize Telegram bot
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, { polling: true });

// Store user contexts for memory
type UserContext = {
  messages: { role: "user" | "assistant" | "system"; content: string }[];
};

const userContexts: Record<number, UserContext> = {};

// Predefined responses for commands
const commands = {
  start:
    "Welcome! Use the buttons below to ask about business hours, location, or contact info.",
  hours:
    "Our business hours are from 9 AM to 6 PM, Monday to Friday. We are closed on weekends.",
  location:
    'We are located at 123 Business Avenue, City, Country. <a href="https://maps.google.com?q=123+Business+Avenue">Click here to view on Google Maps</a>',
  contact:
    'You can contact us at (123) 456-7890, email us at contact@ourbusiness.com, or visit our <a href="https://www.ourbusiness.com">website</a>.',
  appointment:
    'To schedule an appointment, please use this link to setup an appointment with us <a href="https://calendly.com/macdperkins/30min">On Calendly</a>',
};

// Inline keyboard for the start command
const startKeyboard = {
  reply_markup: {
    inline_keyboard: [
      [{ text: "Business Hours", callback_data: "hours" }],
      [{ text: "Location", callback_data: "location" }],
      [{ text: "Contact Info", callback_data: "contact" }],
      [{ text: "Schedule Appointment", callback_data: "appointment" }],
    ],
  },
};

// Command Handlers
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;

  // Initialize or reset user context with system message
  userContexts[chatId] = {
    messages: [
      { role: "system", content: initialContext.dunderMifflinContext },
    ],
  };

  bot.sendMessage(msg.chat.id, commands.start, startKeyboard);
});

// Callback Query Handler for Buttons
bot.on("callback_query", (query) => {
  const chatId = query.message?.chat.id;
  const data = query.data;

  if (!chatId || !data) return;

  switch (data) {
    case "hours":
      bot.sendMessage(chatId, commands.hours, startKeyboard);
      break;
    case "location":
      bot.sendMessage(chatId, commands.location, {
        ...startKeyboard,
        parse_mode: "HTML",
      });
      break;
    case "contact":
      bot.sendMessage(chatId, commands.contact, {
        ...startKeyboard,
        parse_mode: "HTML",
      });
      break;
    case "appointment":
      bot.sendMessage(chatId, commands.appointment, { parse_mode: "HTML" });
      break;
    default:
      bot.sendMessage(chatId, "Sorry, I didn't understand that.");
  }

  // Acknowledge the callback query
  bot.answerCallbackQuery(query.id);
});

// Message Handler (Handles Non-Command Messages)
bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  // Ignore messages starting with "/"
  if (text?.startsWith("/")) return;

  // Initialize user context if not exists with the customer service reminder
  const companyName = "Dunder Mifflin";
  
  if (!userContexts[chatId]) {
    userContexts[chatId] = {
      messages: [
        {
          role: "system",
          content: 
            "Remember to use all the information that was sent to you in the initial context. " +
            "Also that You are a helpful customer service assistant for " + companyName + " Company, " + 
            "so you should always be polite and professional",
        },
      ],
    };
  }

  // Add user message to context
  if (text) {
    userContexts[chatId].messages.push({ role: "user", content: text });
  }

  try {
    // Get AI response
    const completion = await openai.chat.completions.create({
      model: "gpt-4", // or use "gpt-3.5-turbo" for lower cost
      messages: userContexts[chatId].messages,
    });

    const reply =
      completion.choices[0].message.content ??
      "Sorry, I couldn't generate a response.";

    // Add AI response to context
    userContexts[chatId].messages.push({ role: "assistant", content: reply });

    // Limit context size to last 10 messages
    if (userContexts[chatId].messages.length > 10) {
      const systemMessage = userContexts[chatId].messages[0];
      userContexts[chatId].messages = [
        systemMessage,
        ...userContexts[chatId].messages.slice(-9),
      ];
    }

    // Send AI-generated reply
    bot.sendMessage(chatId, reply);
  } catch (error) {
    console.error("Error generating AI response:", error);
    bot.sendMessage(
      chatId,
      "Sorry, I encountered an error processing your request."
    );
  }
});

// Next.js API Handler for Webhook Integration
export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    if (data.message) {
      bot.processUpdate(data); // Pass data to Telegram bot instance
    }

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Error processing webhook:", error);
    return NextResponse.json(
      { error: "Failed to process webhook" },
      { status: 500 }
    );
  }
}
