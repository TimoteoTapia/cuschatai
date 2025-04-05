This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

If you haven’t already, install the project dependencies by running:

   ```bash
   npm install
   ```

Once everything’s installed, you can launch the dev server with

    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    # or
    bun dev
    ```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

# CusChatAI

CusChatAI is a chatbot to assist customers and to help businesses to have a better support service

Anne's favorite quote: "The future is as bright as your faith." Thomas S. Monson

Juan Plasencia:
Allow [the Lord] to make more of you than you can make of yourself on your own. Treasure His involvement.
Ronald A. Rasband

“It is mentally rigorous to strive to look unto Him in every thought. But, when we do, our doubts and fears flee.”—President Russell M. Nelson, “Drawing the Power of Jesus Christ into Our Lives”
-Matthew Perkins

Timoteo Tapia:
"Obedience brings success; exact obedience brings miracles."Russell M. Nelson (Kevin Tapia)

## Tech Stack:
- Telegram for interface platform (Matthew Perkins). Telegram has a bot API called Telegram Bot, which allows for easy building of chatbots and choosing what functionaility you want to build for your chatbot. We will use the Telegram Bot API for basic interfacing with the user, and will integrate an AI model with Telegram Bot to allow for natural language to be used during a conversation.
### Links: 
- [Telegram Bot](https://core.telegram.org/bots)
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)

Standup Week 03:
LLMs Mode Integration with Telegram (Juan Plasencia)
When investigating the integration of LLMs with Telegram, it has been found that it is necessary to design an API that integrates the interface services offered by Telegram with those of a back-end that consumes the pre-trained models in the cloud, and these can return the necessary information to the chat bot. 

# 📅 Google Calendar Integration Options for the Dunder Mifflin Chatbot

To allow customers to schedule appointments with Dunder Mifflin, we are considering integrating Google Calendar functionality into our Telegram chatbot. There are **two main approaches** to implement this feature:

---

## 🔹 Option 1: Google Calendar Integration within the Chatbot

In this approach, the chatbot (built using Node.js) directly handles the Google Calendar scheduling functionality using the Google Calendar API.

### 🔧 How it works:
- The user tells the bot they want to schedule an appointment.
- The bot guides them through available dates and times.
- The bot uses the Google Calendar API to check availability and create events.
- The user receives a confirmation message within the Telegram chat.

### ✅ Pros:
- Seamless experience within Telegram – users never leave the chat.
- Full control over how appointments are booked and confirmed.
- More flexibility to customize logic (e.g., max appointments per day, buffer times, etc.).

### ❌ Cons:
- Requires handling authentication with Google API (OAuth2).
- Slightly more complex to implement and secure.
- You must maintain the logic to handle scheduling flow and conflict resolution.

---

## 🔹 Option 2: Calendar Integration via Telegram Interface (External Link or Button)

In this approach, the bot sends a link or interactive button to redirect the user to an external Google Calendar booking page (e.g., using Google Calendar appointment slots or a service like Calendly connected to Google Calendar).

### 🔧 How it works:
- The user asks to book a meeting.
- The bot replies with a link to a booking page (hosted externally).
- The user opens the link and selects their preferred time.
- Confirmation is sent via email or follow-up message from the bot.

### ✅ Pros:
- Easier and faster to implement.
- No need to manage calendar conflicts or Google API logic in the bot.
- Scalable and secure — leverages Google or third-party systems.

### ❌ Cons:
- User leaves the Telegram app to complete the booking.
- Less control over the UI/UX and confirmation flow.
- May feel less integrated or personal.
