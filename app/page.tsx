import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500/60 via-white to-purple-200 dark:from-blue-950 dark:via-gray-900 dark:to-purple-950 text-black dark:text-white">
      <div className="container mx-auto px-4 py-12 flex flex-col items-center justify-center min-h-screen backdrop-blur-sm">
        <main className="flex flex-col items-center gap-12 text-center max-w-4xl w-full">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-3xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur-xl" />
            <Image
              src="/ccai-logo1.png"
              alt="CusChatAI Logo"
              width={200}
              height={200}
              className="relative rounded-3xl transition-transform duration-300 group-hover:scale-110 animate-float"
              style={{
                filter: "var(--image-filter)",
              }}
            />
          </div>

          <div className="space-y-6 animate-slide-in">
            <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">
              CusChatAI
            </h1>
            <p className="text-xl md:text-3xl max-w-2xl font-light">
              Hello, I&apos;m CusChatAI, your smart and friendly business
              assistant!
            </p>
            <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300">
              I am ready to help you with basic business information, right in
              your Telegram!
            </p>
          </div>

          <div
            className="relative group animate-slide-in delay-200"
            style={{ animationDelay: "0.2s" }}
          >
            <a
              href="https://t.me/CusChatAI_Bot"
              target="_blank"
              rel="noopener noreferrer"
              className="relative inline-flex items-center gap-2 bg-blue-500 text-white rounded-full px-8 py-4 text-lg font-medium 
                       hover:bg-blue-600 transition duration-300 transform hover:scale-105 shadow-lg
                       hover:shadow-blue-500/50 active:scale-95"
            >
              <svg
                className="w-6 h-6"
                fill="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.2-.04-.28-.02-.12.03-2 1.27-5.64 3.72-.53.36-1.02.54-1.46.53-.48-.01-1.4-.27-2.08-.49-.84-.28-1.51-.43-1.45-.91.03-.25.38-.51 1.05-.78 4.12-1.79 6.87-2.97 8.26-3.54 3.93-1.63 4.75-1.91 5.27-1.91.12 0 .38.03.55.17.14.12.18.28.2.45-.02.05-.02.31-.03.61z" />
              </svg>
              Talk to CusChatAI on Telegram
            </a>
          </div>
        </main>

        <footer
          className="mt-20 text-sm text-center opacity-60 animate-slide-in delay-400"
          style={{ animationDelay: "0.4s" }}
        >
          © {new Date().getFullYear()} CusChatAI | Created by CSE499Team3 |
          <br className="md:hidden" /> Matthew Perkins • Kevin Tapia • Juan
          Leyva • Anelisa Ferreira
        </footer>
      </div>
    </div>
  );
}
