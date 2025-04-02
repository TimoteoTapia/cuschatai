import { NextRequest, NextResponse } from "next/server";
import { OpenAI } from "openai";
import TelegramBot from "node-telegram-bot-api";

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Set up Telegram bot
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN as string);

// Store user contexts
type UserContext = {
  messages: { role: "user" | "assistant" | "system"; content: string }[];
};

const userContexts: Record<number, UserContext> = {};

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    // Check if this is a message update
    if (data && data.message) {
      const { message } = data;
      const chatId = message.chat.id;
      const text = message.text;

      // Initialize context if needed
      if (!userContexts[chatId]) {
        userContexts[chatId] = {
          messages: [
            { role: "system", content: "You are a helpful assistant." },
          ],
        };
      }

      // Add user message to context
      userContexts[chatId].messages.push({ role: "user", content: text });

      // Get response from OpenAI
      const completion = await openai.chat.completions.create({
        model: "gpt-4", // or your model of choice
        messages: userContexts[chatId].messages,
      });

      const reply = completion.choices[0].message.content;

      // Add assistant response to context
      userContexts[chatId].messages.push({
        role: "assistant",
        content: reply as string,
      });

      // Limit context size to prevent token overflow
      if (userContexts[chatId].messages.length > 10) {
        const systemMessage = userContexts[chatId].messages[0];
        userContexts[chatId].messages = [
          systemMessage,
          ...userContexts[chatId].messages.slice(-9),
        ];
      }

      // Send response back to user
      await fetch(
        `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_id: chatId,
            text: reply,
          }),
        }
      );
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
