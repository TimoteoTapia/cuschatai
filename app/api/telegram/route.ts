import { NextRequest, NextResponse } from "next/server";
import { OpenAI } from "openai";
import TelegramBot from "node-telegram-bot-api";

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
  start: "Welcome! Ask me about business hours, location, or contact info.",
  hours: "Our business hours are from 9 AM to 6 PM, Monday to Friday. We are closed on weekends.",
  location:
    'We are located at 123 Business Avenue, City, Country. <a href="https://maps.google.com?q=123+Business+Avenue">Click here to view on Google Maps</a>',
  contact:
    'You can contact us at (123) 456-7890, email us at contact@ourbusiness.com, or visit our <a href="https://www.ourbusiness.com">website</a>.',
};

// Command Handlers
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, commands.start);
});

bot.onText(/\/hours/, (msg) => {
  bot.sendMessage(msg.chat.id, commands.hours);
});

bot.onText(/\/location/, (msg) => {
  bot.sendMessage(msg.chat.id, commands.location, { parse_mode: "HTML" });
});

bot.onText(/\/contact/, (msg) => {
  bot.sendMessage(msg.chat.id, commands.contact, { parse_mode: "HTML" });
});

// Message Handler (Handles Non-Command Messages)
bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  // Ignore messages starting with "/"
  if (text?.startsWith("/")) return;

  // Initialize user context if not exists
  if (!userContexts[chatId]) {
    userContexts[chatId] = {
      messages: [{ role: "system", content: "You are a helpful assistant." }],
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

    const reply = completion.choices[0].message.content ?? "Sorry, I couldn't generate a response.";

    // Add AI response to context
    userContexts[chatId].messages.push({ role: "assistant", content: reply });

    // Limit context size to last 10 messages
    if (userContexts[chatId].messages.length > 10) {
      const systemMessage = userContexts[chatId].messages[0]; // Keep system prompt
      userContexts[chatId].messages = [
        systemMessage,
        ...userContexts[chatId].messages.slice(-9),
      ];
    }

    // Send AI-generated reply
    bot.sendMessage(chatId, reply);
  } catch (error) {
    console.error("Error generating AI response:", error);
    bot.sendMessage(chatId, "Sorry, I encountered an error processing your request.");
  }
});

// Next.js API Handler for Webhook Integration
export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    if (data.message) {
      // Removed unused 'message' variable
      bot.processUpdate(data); // Pass data to Telegram bot instance
    }

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Error processing webhook:", error);
    return NextResponse.json({ error: "Failed to process webhook" }, { status: 500 });
  }
}
