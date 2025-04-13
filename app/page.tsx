import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500/60 via-white to-purple-200 dark:from-gray-900 dark:via-black dark:to-gray-800 text-black dark:text-white flex flex-col items-center justify-center p-8 sm:p-20 font-[var(--font-geist-sans)]">
      <main className="flex flex-col items-center gap-10 text-center">
        <Image
          src="/ccai-logo1.png"
          alt="CusChatAI Logo"
          width={200}
          height={200}
          className="dark:invert animate-bounce-slow rounded-3xl"
        />
        <h1 className="text-3xl sm:text-5xl font-bold">CusChatAI</h1>
        <p className="text-lg sm:text-2xl max-w-xl">
          Hello, I&apos;m CusChatAI, your smart and friendly business assistant!
        </p>
        <p className="text-lg sm:text-xl">
          I am ready to help you with basic business information, right in your Telegram!
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <a
            href="https://t.me/CusChatAI_Bot"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-500 text-white rounded-full px-6 py-3 text-lg font-medium hover:bg-blue-600 transition duration-300 transform hover:scale-105 shadow-lg"
          >
            Talk to CusChatAI on Telegram
          </a>
        </div>
      </main>

      <footer className="mt-20 text-sm opacity-60">
        © {new Date().getFullYear()} CusChatAI | Created by CSE499Team3 | Matthew Perkins • Kevin Tapia • Juan Leyva • Anelisa Ferreira
      </footer>
    </div>
  );
}
