"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Mountain } from "lucide-react";

export function Header() {
  return (
    <header className="px-4 lg:px-6 h-14 flex items-center bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50 border-b border-gray-200 dark:border-gray-800">
      <Link className="flex items-center justify-center" href="#">
        <Mountain className="h-6 w-6" />
        <span className="sr-only">Sentient Core</span>
      </Link>
      <nav className="ml-auto hidden lg:flex gap-4 sm:gap-6">
        <Link
          className="text-sm font-medium hover:underline underline-offset-4"
          href="#features"
        >
          Features
        </Link>
        <Link
          className="text-sm font-medium hover:underline underline-offset-4"
          href="#hackathon"
        >
          Hackathon
        </Link>
        <Link
          className="text-sm font-medium hover:underline underline-offset-4"
          href="/docs"
        >
          Docs
        </Link>
        <Button size="sm" variant="outline" asChild>
          <Link href="/dashboard">Login</Link>
        </Button>
        <Button size="sm" asChild>
          <Link href="/dashboard">Get Started</Link>
        </Button>
      </nav>
      <Sheet>
        <SheetTrigger asChild>
          <Button className="ml-auto lg:hidden" size="icon" variant="outline">
            <Menu className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <div className="grid gap-2 py-6">
            <Link
              className="flex w-full items-center py-2 text-lg font-semibold"
              href="#"
            >
              Sentient Core
            </Link>
            <Link
              className="flex w-full items-center py-2 text-lg font-semibold"
              href="#features"
            >
              Features
            </Link>
            <Link
              className="flex w-full items-center py-2 text-lg font-semibold"
              href="#hackathon"
            >
              Hackathon
            </Link>
            <Link
              className="flex w-full items-center py-2 text-lg font-semibold"
              href="/docs"
            >
              Docs
            </Link>
            <div className="flex flex-col gap-4 mt-4">
              <Button variant="outline" asChild><Link href="/dashboard">Login</Link></Button>
              <Button asChild><Link href="/dashboard">Get Started</Link></Button>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </header>
  );
}
