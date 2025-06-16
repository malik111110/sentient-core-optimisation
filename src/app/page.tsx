'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    // Auto-redirect to dashboard after a short delay
    const timer = setTimeout(() => {
      router.push('/dashboard')
    }, 2000)

    return () => clearTimeout(timer)
  }, [router])

  const handleGetStarted = () => {
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
              Genesis Engine
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              The next-generation AI-powered development platform that transforms ideas into production-ready applications through intelligent multi-agent collaboration.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="text-lg px-8 py-3"
                onClick={handleGetStarted}
              >
                Get Started
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="text-lg px-8 py-3"
                onClick={() => router.push('/docs')}
              >
                View Documentation
              </Button>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg border">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-Powered Development</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Leverage specialized AI agents for frontend, backend, DevOps, and more to accelerate your development workflow.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg border">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Multi-Agent Collaboration</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Orchestrate multiple specialized agents working together seamlessly to handle complex development tasks.
              </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg border">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Production Ready</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Generate enterprise-grade applications with best practices, security, and scalability built-in from day one.
              </p>
            </div>
          </div>

          {/* Tech Stack */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-8 shadow-lg border">
            <h3 className="text-2xl font-semibold mb-6">Built with Modern Technologies</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
              {[
                'Next.js 15',
                'React 19',
                'TypeScript',
                'Tailwind CSS',
                'FastAPI',
                'PostgreSQL',
                'Redis',
                'Docker',
                'AutoGen',
                'LangGraph',
                'Supabase',
                'WebContainer'
              ].map((tech) => (
                <div key={tech} className="text-center">
                  <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{tech}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Auto-redirect notice */}
          <div className="mt-8 text-sm text-gray-500 dark:text-gray-400">
            Redirecting to dashboard in a few seconds...
          </div>
        </div>
      </div>
    </div>
  )
}
