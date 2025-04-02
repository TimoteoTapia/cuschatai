This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

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

## Hosting Platforms for CusChatAI

For hosting the backend of the CusChatAI project, we researched several hosting platforms to identify the best option based on scalability, ease of use, integration capabilities, and cost-effectiveness. Below are the platforms we considered and the reasons for selecting the final choice.

### Platforms Considered:
1. **Vercel**
   - **Pros**:
     - Easy deployment with GitHub integration.
     - Excellent for serverless functions, making it a good fit for a chatbot-based application.
     - Automatic scaling.
     - Free tier with generous usage limits.
     - Fast global CDN for low-latency responses.
   - **Cons**:
     - Some limitations on serverless execution duration and memory on free tier.

2. **Render**
   - **Pros**:
     - Simple deployment with auto-scaling.
     - Free tier available for small projects.
     - Supports databases and backend services.
   - **Cons**:
     - Not as widely known as other platforms like AWS, so some documentation might be lacking.

3. **AWS (Amazon Web Services)**
   - **Pros**:
     - Highly scalable with a vast range of services.
     - Can support complex application architectures.
   - **Cons**:
     - Steep learning curve.
     - Pricing can get complex and expensive as the application grows.

4. **Google Cloud**
   - **Pros**:
     - Highly scalable and robust infrastructure.
     - Good integration with Google services like Calendar API.
   - **Cons**:
     - Similar to AWS, pricing and setup can be complex.
