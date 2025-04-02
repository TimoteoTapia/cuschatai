import { NextResponse } from "next/server";

export async function GET() {
  try {
    const response = await fetch(
      `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/setWebhook?url=${process.env.WEBHOOK_URL}`,
      { method: "GET" }
    );

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error setting webhook:", error);
    return NextResponse.json(
      { error: "Failed to set webhook" },
      { status: 500 }
    );
  }
}
