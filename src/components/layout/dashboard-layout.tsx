'use client'

import { ReactNode } from 'react'
import { Header } from './header'
import { Sidebar } from './sidebar'
import { cn } from '@/lib/utils'

interface DashboardLayoutProps {
  children: ReactNode
  className?: string
}

export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className={cn(
          "flex-1 overflow-y-auto bg-background p-6",
          className
        )}>
          {children}
        </main>
      </div>
    </div>
  )
}