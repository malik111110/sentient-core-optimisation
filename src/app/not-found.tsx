import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="max-w-md mx-auto text-center p-6">
        <div className="mb-6">
          <div className="text-6xl font-bold text-gray-300 dark:text-gray-600 mb-4">
            404
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Page Not Found
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>

        <div className="space-y-4">
          <Button asChild className="w-full">
            <Link href="/dashboard">
              Go to Dashboard
            </Link>
          </Button>
          <Button variant="outline" asChild className="w-full">
            <Link href="/">
              Go to Homepage
            </Link>
          </Button>
        </div>

        <div className="mt-8">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            If you believe this is an error, please{' '}
            <Link href="/contact" className="text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300">
              contact support
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}