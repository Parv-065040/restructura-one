"use client";

import { motion } from "framer-motion";
import clsx from "clsx";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
}

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={clsx("flex", isUser ? "justify-end" : "justify-start")}
    >
      <div
        className={clsx(
          "max-w-[75ch] rounded-card px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-accent-blue/15 text-ink"
            : "panel text-ink"
        )}
      >
        {message.content}
        {message.streaming && (
          <span className="ml-0.5 inline-block h-3.5 w-1.5 animate-pulse bg-accent-teal/70 align-middle" />
        )}
      </div>
    </motion.div>
  );
}
