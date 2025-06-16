'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { AgentCard } from '@/components/agents/agent-card'
import { ProjectCard } from '@/components/projects/project-card'
import { TaskCard } from '@/components/tasks/task-card'
import { Button } from '@/components/ui/button'
import { Agent, Project, Task, AgentStatus, ProjectStatus, TaskStatus, TaskPriority } from '@/types'

// Mock data for demonstration
const mockAgents: Agent[] = [
  {
    id: 'agent-1',
    name: 'Frontend Specialist',
    type: 'FRONTEND',
    description: 'Specialized in Next.js and React development',
    status: AgentStatus.RUNNING,
    capabilities: ['React', 'Next.js', 'TypeScript', 'Tailwind CSS'],
    version: '1.0.0',
    lastActive: new Date().toISOString(),
    currentTask: {
      id: 'task-1',
      title: 'Building dashboard components',
      progress: 0.75
    }
  },
  {
    id: 'agent-2',
    name: 'Backend Engineer',
    type: 'BACKEND',
    description: 'FastAPI and Python backend development',
    status: AgentStatus.IDLE,
    capabilities: ['Python', 'FastAPI', 'PostgreSQL', 'Redis'],
    version: '1.0.0',
    lastActive: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: 'agent-3',
    name: 'DevOps Automation',
    type: 'DEVOPS',
    description: 'Infrastructure and deployment automation',
    status: AgentStatus.BUSY,
    capabilities: ['Docker', 'Kubernetes', 'Terraform', 'CI/CD'],
    version: '1.0.0',
    lastActive: new Date().toISOString(),
  }
]

const mockProjects: Project[] = [
  {
    id: 'project-1',
    name: 'E-commerce Platform',
    description: 'A modern e-commerce platform with AI-powered recommendations',
    status: ProjectStatus.IN_PROGRESS,
    progress: 0.65,
    techStack: ['Next.js', 'FastAPI', 'PostgreSQL', 'Redis', 'Stripe'],
    createdAt: new Date(Date.now() - 7 * 24 * 3600000).toISOString(),
    updatedAt: new Date().toISOString(),
    agents: ['agent-1', 'agent-2'],
    artifacts: ['frontend-app', 'backend-api', 'database-schema']
  },
  {
    id: 'project-2',
    name: 'Task Management App',
    description: 'Collaborative task management with real-time updates',
    status: ProjectStatus.COMPLETED,
    progress: 1.0,
    techStack: ['React', 'Node.js', 'MongoDB', 'Socket.io'],
    createdAt: new Date(Date.now() - 14 * 24 * 3600000).toISOString(),
    updatedAt: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
    agents: ['agent-1'],
    artifacts: ['web-app', 'mobile-app', 'api-docs']
  }
]

const mockTasks: Task[] = [
  {
    id: 'task-1',
    title: 'Implement user authentication',
    description: 'Set up OAuth 2.1 with JWT tokens and session management',
    status: TaskStatus.IN_PROGRESS,
    priority: TaskPriority.HIGH,
    progress: 0.8,
    assignedAgent: 'Backend Engineer',
    estimatedDuration: 240,
    createdAt: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
    startedAt: new Date(Date.now() - 24 * 3600000).toISOString(),
    dependencies: ['Database setup']
  },
  {
    id: 'task-2',
    title: 'Create dashboard UI',
    description: 'Build responsive dashboard with charts and metrics',
    status: TaskStatus.COMPLETED,
    priority: TaskPriority.MEDIUM,
    progress: 1.0,
    assignedAgent: 'Frontend Specialist',
    estimatedDuration: 180,
    createdAt: new Date(Date.now() - 3 * 24 * 3600000).toISOString(),
    startedAt: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
    completedAt: new Date(Date.now() - 6 * 3600000).toISOString(),
  },
  {
    id: 'task-3',
    title: 'Set up CI/CD pipeline',
    description: 'Configure automated testing and deployment',
    status: TaskStatus.PENDING,
    priority: TaskPriority.CRITICAL,
    assignedAgent: 'DevOps Automation',
    estimatedDuration: 300,
    createdAt: new Date().toISOString(),
    dependencies: ['Code repository setup']
  }
]

export default function DashboardPage() {
  const [agents, setAgents] = useState<Agent[]>(mockAgents)
  const [projects, setProjects] = useState<Project[]>(mockProjects)
  const [tasks, setTasks] = useState<Task[]>(mockTasks)

  const handleStartAgent = (agentId: string) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: AgentStatus.RUNNING }
        : agent
    ))
  }

  const handleStopAgent = (agentId: string) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: AgentStatus.IDLE }
        : agent
    ))
  }

  const handleStartTask = (taskId: string) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: TaskStatus.IN_PROGRESS, startedAt: new Date().toISOString() }
        : task
    ))
  }

  const handleCompleteTask = (taskId: string) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { 
            ...task, 
            status: TaskStatus.COMPLETED, 
            progress: 1.0,
            completedAt: new Date().toISOString() 
          }
        : task
    ))
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">
              Monitor your agents, projects, and tasks in real-time
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">Import Project</Button>
            <Button>New Project</Button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-lg border bg-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Active Agents</p>
                <p className="text-2xl font-bold">
                  {agents.filter(a => a.status === AgentStatus.RUNNING || a.status === AgentStatus.BUSY).length}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center">
                <div className="h-4 w-4 rounded-full bg-green-500" />
              </div>
            </div>
          </div>
          
          <div className="rounded-lg border bg-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Active Projects</p>
                <p className="text-2xl font-bold">
                  {projects.filter(p => p.status === ProjectStatus.IN_PROGRESS).length}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                <div className="h-4 w-4 rounded-full bg-blue-500" />
              </div>
            </div>
          </div>
          
          <div className="rounded-lg border bg-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Pending Tasks</p>
                <p className="text-2xl font-bold">
                  {tasks.filter(t => t.status === TaskStatus.PENDING || t.status === TaskStatus.IN_PROGRESS).length}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-yellow-100 flex items-center justify-center">
                <div className="h-4 w-4 rounded-full bg-yellow-500" />
              </div>
            </div>
          </div>
          
          <div className="rounded-lg border bg-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Completed Today</p>
                <p className="text-2xl font-bold">
                  {tasks.filter(t => t.status === TaskStatus.COMPLETED && 
                    t.completedAt && 
                    new Date(t.completedAt).toDateString() === new Date().toDateString()
                  ).length}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-purple-100 flex items-center justify-center">
                <div className="h-4 w-4 rounded-full bg-purple-500" />
              </div>
            </div>
          </div>
        </div>

        {/* Active Agents */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Active Agents</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onStart={handleStartAgent}
                onStop={handleStopAgent}
              />
            ))}
          </div>
        </div>

        {/* Recent Projects */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Recent Projects</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
              />
            ))}
          </div>
        </div>

        {/* Active Tasks */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Active Tasks</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onStart={handleStartTask}
                onComplete={handleCompleteTask}
              />
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}