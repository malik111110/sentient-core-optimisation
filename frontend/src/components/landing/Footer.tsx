"use client";

import Link from "next/link";
import { Mountain } from 'lucide-react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t border-gray-200 dark:border-gray-800">
      <p className="text-xs text-gray-500 dark:text-gray-400">
        © {currentYear} Sentient Core. All rights reserved.
      </p>
      <div className="sm:ml-auto flex gap-4 sm:gap-6 items-center">
        <Link className="flex items-center justify-center" href="#">
          <Mountain className="h-6 w-6" />
          <span className="sr-only">Sentient Core</span>
        </Link>
        <Link className="text-xs hover:underline underline-offset-4" href="/terms">
          Terms of Service
        </Link>
        <Link className="text-xs hover:underline underline-offset-4" href="/privacy">
          Privacy
        </Link>
      </div>
    </footer>
  );
}
