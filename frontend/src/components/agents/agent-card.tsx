'use client'

import { Agent, AgentStatus } from '@/types'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface AgentCardProps {
  agent: Agent
  onStart?: (agentId: string) => void
  onStop?: (agentId: string) => void
  onConfigure?: (agentId: string) => void
  className?: string
}

const statusColors = {
  [AgentStatus.IDLE]: 'bg-gray-500',
  [AgentStatus.RUNNING]: 'bg-green-500',
  [AgentStatus.BUSY]: 'bg-yellow-500',
  [AgentStatus.ERROR]: 'bg-red-500',
  [AgentStatus.OFFLINE]: 'bg-gray-400',
}

const statusLabels = {
  [AgentStatus.IDLE]: 'Idle',
  [AgentStatus.RUNNING]: 'Running',
  [AgentStatus.BUSY]: 'Busy',
  [AgentStatus.ERROR]: 'Error',
  [AgentStatus.OFFLINE]: 'Offline',
}

export function AgentCard({ 
  agent, 
  onStart, 
  onStop, 
  onConfigure, 
  className 
}: AgentCardProps) {
  const isRunning = agent.status === AgentStatus.RUNNING || agent.status === AgentStatus.BUSY

  return (
    <div className={cn(
      "rounded-lg border bg-card p-6 shadow-sm transition-shadow hover:shadow-md",
      className
    )}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="font-semibold text-lg">{agent.name}</h3>
            <div className="flex items-center gap-1">
              <div className={cn(
                "h-2 w-2 rounded-full",
                statusColors[agent.status]
              )} />
              <span className="text-xs text-muted-foreground">
                {statusLabels[agent.status]}
              </span>
            </div>
          </div>
          <p className="text-sm text-muted-foreground mb-3">
            {agent.description}
          </p>
          <div className="flex flex-wrap gap-1 mb-4">
            {agent.capabilities.map((capability) => (
              <span
                key={capability}
                className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground"
              >
                {capability}
              </span>
            ))}
          </div>
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">
          <div>Type: {agent.type}</div>
          <div>Version: {agent.version}</div>
          {agent.lastActive && (
            <div>Last Active: {new Date(agent.lastActive).toLocaleString()}</div>
          )}
        </div>
        
        <div className="flex gap-2">
          {onConfigure && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onConfigure(agent.id)}
            >
              Configure
            </Button>
          )}
          
          {isRunning ? (
            onStop && (
              <Button
                variant="destructive"
                size="sm"
                onClick={() => onStop(agent.id)}
              >
                Stop
              </Button>
            )
          ) : (
            onStart && (
              <Button
                size="sm"
                onClick={() => onStart(agent.id)}
                disabled={agent.status === AgentStatus.ERROR}
              >
                Start
              </Button>
            )
          )}
        </div>
      </div>
      
      {agent.currentTask && (
        <div className="mt-4 p-3 bg-muted rounded-md">
          <div className="text-xs font-medium text-muted-foreground mb-1">
            Current Task:
          </div>
          <div className="text-sm">{agent.currentTask.title}</div>
          {agent.currentTask.progress !== undefined && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-muted-foreground mb-1">
                <span>Progress</span>
                <span>{Math.round(agent.currentTask.progress * 100)}%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-1.5">
                <div 
                  className="bg-primary h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${agent.currentTask.progress * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}