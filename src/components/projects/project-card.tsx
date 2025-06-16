'use client'

import Link from 'next/link'
import { Project, ProjectStatus } from '@/types'
import { Button } from '@/components/ui/button'
import { cn, formatRelativeTime } from '@/lib/utils'

interface ProjectCardProps {
  project: Project
  onDelete?: (projectId: string) => void
  onDuplicate?: (projectId: string) => void
  className?: string
}

const statusColors = {
  [ProjectStatus.DRAFT]: 'bg-gray-500',
  [ProjectStatus.IN_PROGRESS]: 'bg-blue-500',
  [ProjectStatus.COMPLETED]: 'bg-green-500',
  [ProjectStatus.FAILED]: 'bg-red-500',
  [ProjectStatus.PAUSED]: 'bg-yellow-500',
}

const statusLabels = {
  [ProjectStatus.DRAFT]: 'Draft',
  [ProjectStatus.IN_PROGRESS]: 'In Progress',
  [ProjectStatus.COMPLETED]: 'Completed',
  [ProjectStatus.FAILED]: 'Failed',
  [ProjectStatus.PAUSED]: 'Paused',
}

export function ProjectCard({ 
  project, 
  onDelete, 
  onDuplicate, 
  className 
}: ProjectCardProps) {
  return (
    <div className={cn(
      "rounded-lg border bg-card p-6 shadow-sm transition-shadow hover:shadow-md",
      className
    )}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Link 
              href={`/dashboard/projects/${project.id}`}
              className="font-semibold text-lg hover:text-primary transition-colors"
            >
              {project.name}
            </Link>
            <div className="flex items-center gap-1">
              <div className={cn(
                "h-2 w-2 rounded-full",
                statusColors[project.status]
              )} />
              <span className="text-xs text-muted-foreground">
                {statusLabels[project.status]}
              </span>
            </div>
          </div>
          <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
            {project.description}
          </p>
        </div>
      </div>
      
      {project.techStack && project.techStack.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-4">
          {project.techStack.slice(0, 5).map((tech) => (
            <span
              key={tech}
              className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground"
            >
              {tech}
            </span>
          ))}
          {project.techStack.length > 5 && (
            <span className="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium text-muted-foreground">
              +{project.techStack.length - 5} more
            </span>
          )}
        </div>
      )}
      
      <div className="flex items-center justify-between text-xs text-muted-foreground mb-4">
        <div>
          Created: {formatRelativeTime(project.createdAt)}
        </div>
        <div>
          Updated: {formatRelativeTime(project.updatedAt)}
        </div>
      </div>
      
      {project.progress !== undefined && (
        <div className="mb-4">
          <div className="flex justify-between text-xs text-muted-foreground mb-1">
            <span>Progress</span>
            <span>{Math.round(project.progress * 100)}%</span>
          </div>
          <div className="w-full bg-secondary rounded-full h-2">
            <div 
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${project.progress * 100}%` }}
            />
          </div>
        </div>
      )}
      
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          {project.agents && (
            <div className="flex items-center gap-1">
              <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>{project.agents.length} agents</span>
            </div>
          )}
          {project.artifacts && (
            <div className="flex items-center gap-1">
              <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>{project.artifacts.length} files</span>
            </div>
          )}
        </div>
        
        <div className="flex gap-2">
          {onDuplicate && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onDuplicate(project.id)}
            >
              Duplicate
            </Button>
          )}
          
          <Link href={`/dashboard/projects/${project.id}`}>
            <Button size="sm">
              Open
            </Button>
          </Link>
          
          {onDelete && (
            <Button
              variant="destructive"
              size="sm"
              onClick={() => onDelete(project.id)}
            >
              Delete
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}