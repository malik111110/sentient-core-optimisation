'use client'

import { Task, TaskStatus, TaskPriority } from '@/types'
import { Button } from '@/components/ui/button'
import { cn, formatRelativeTime } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onStart?: (taskId: string) => void
  onPause?: (taskId: string) => void
  onComplete?: (taskId: string) => void
  onCancel?: (taskId: string) => void
  className?: string
}

const statusColors = {
  [TaskStatus.PENDING]: 'bg-gray-500',
  [TaskStatus.IN_PROGRESS]: 'bg-blue-500',
  [TaskStatus.COMPLETED]: 'bg-green-500',
  [TaskStatus.FAILED]: 'bg-red-500',
  [TaskStatus.CANCELLED]: 'bg-gray-400',
  [TaskStatus.PAUSED]: 'bg-yellow-500',
}

const statusLabels = {
  [TaskStatus.PENDING]: 'Pending',
  [TaskStatus.IN_PROGRESS]: 'In Progress',
  [TaskStatus.COMPLETED]: 'Completed',
  [TaskStatus.FAILED]: 'Failed',
  [TaskStatus.CANCELLED]: 'Cancelled',
  [TaskStatus.PAUSED]: 'Paused',
}

const priorityColors = {
  [TaskPriority.LOW]: 'text-green-600 bg-green-50 border-green-200',
  [TaskPriority.MEDIUM]: 'text-yellow-600 bg-yellow-50 border-yellow-200',
  [TaskPriority.HIGH]: 'text-orange-600 bg-orange-50 border-orange-200',
  [TaskPriority.CRITICAL]: 'text-red-600 bg-red-50 border-red-200',
}

const priorityLabels = {
  [TaskPriority.LOW]: 'Low',
  [TaskPriority.MEDIUM]: 'Medium',
  [TaskPriority.HIGH]: 'High',
  [TaskPriority.CRITICAL]: 'Critical',
}

export function TaskCard({ 
  task, 
  onStart, 
  onPause, 
  onComplete, 
  onCancel, 
  className 
}: TaskCardProps) {
  const isInProgress = task.status === TaskStatus.IN_PROGRESS
  const isPending = task.status === TaskStatus.PENDING
  const isPaused = task.status === TaskStatus.PAUSED
  const isCompleted = task.status === TaskStatus.COMPLETED
  const isFailed = task.status === TaskStatus.FAILED

  return (
    <div className={cn(
      "rounded-lg border bg-card p-4 shadow-sm transition-shadow hover:shadow-md",
      className
    )}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h4 className="font-medium text-base">{task.title}</h4>
            <div className="flex items-center gap-1">
              <div className={cn(
                "h-2 w-2 rounded-full",
                statusColors[task.status]
              )} />
              <span className="text-xs text-muted-foreground">
                {statusLabels[task.status]}
              </span>
            </div>
          </div>
          
          {task.description && (
            <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
              {task.description}
            </p>
          )}
          
          <div className="flex items-center gap-2 mb-3">
            <span className={cn(
              "inline-flex items-center rounded-md border px-2 py-1 text-xs font-medium",
              priorityColors[task.priority]
            )}>
              {priorityLabels[task.priority]}
            </span>
            
            {task.assignedAgent && (
              <span className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
                {task.assignedAgent}
              </span>
            )}
            
            {task.estimatedDuration && (
              <span className="text-xs text-muted-foreground">
                Est. {task.estimatedDuration}min
              </span>
            )}
          </div>
        </div>
      </div>
      
      {task.progress !== undefined && (
        <div className="mb-3">
          <div className="flex justify-between text-xs text-muted-foreground mb-1">
            <span>Progress</span>
            <span>{Math.round(task.progress * 100)}%</span>
          </div>
          <div className="w-full bg-secondary rounded-full h-1.5">
            <div 
              className="bg-primary h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${task.progress * 100}%` }}
            />
          </div>
        </div>
      )}
      
      <div className="flex items-center justify-between text-xs text-muted-foreground mb-3">
        <div>
          Created: {formatRelativeTime(task.createdAt)}
        </div>
        {task.startedAt && (
          <div>
            Started: {formatRelativeTime(task.startedAt)}
          </div>
        )}
        {task.completedAt && (
          <div>
            Completed: {formatRelativeTime(task.completedAt)}
          </div>
        )}
      </div>
      
      {task.dependencies && task.dependencies.length > 0 && (
        <div className="mb-3">
          <div className="text-xs text-muted-foreground mb-1">Dependencies:</div>
          <div className="flex flex-wrap gap-1">
            {task.dependencies.map((dep) => (
              <span
                key={dep}
                className="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium text-muted-foreground"
              >
                {dep}
              </span>
            ))}
          </div>
        </div>
      )}
      
      <div className="flex gap-2">
        {isPending && onStart && (
          <Button
            size="sm"
            onClick={() => onStart(task.id)}
          >
            Start
          </Button>
        )}
        
        {isInProgress && onPause && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPause(task.id)}
          >
            Pause
          </Button>
        )}
        
        {isPaused && onStart && (
          <Button
            size="sm"
            onClick={() => onStart(task.id)}
          >
            Resume
          </Button>
        )}
        
        {(isInProgress || isPaused) && onComplete && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => onComplete(task.id)}
          >
            Complete
          </Button>
        )}
        
        {(isPending || isInProgress || isPaused) && onCancel && (
          <Button
            variant="destructive"
            size="sm"
            onClick={() => onCancel(task.id)}
          >
            Cancel
          </Button>
        )}
      </div>
      
      {task.error && (
        <div className="mt-3 p-2 bg-destructive/10 border border-destructive/20 rounded-md">
          <div className="text-xs font-medium text-destructive mb-1">
            Error:
          </div>
          <div className="text-xs text-destructive">{task.error}</div>
        </div>
      )}
    </div>
  )
}