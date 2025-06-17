"use client";

import { motion } from 'framer-motion';
import { Zap, Users, BrainCircuit, GitGraph, ShieldCheck, Scaling } from 'lucide-react';

const features = [
  {
    icon: <Users className="h-8 w-8 text-blue-500" />,
    title: 'Dynamic Team Composition',
    description: 'Our platform dynamically assembles teams of specialized agents (e.g., Frontend, Database, Security) to ensure every component is crafted with precision.',
  },
  {
    icon: <BrainCircuit className="h-8 w-8 text-purple-500" />,
    title: 'Agent-of-Agents Architecture',
    description: 'Meta-Agents act as expert managers, composing and overseeing bespoke agent teams to tackle novel, industry-specific challenges with tailored expertise.',
  },
  {
    icon: <GitGraph className="h-8 w-8 text-green-500" />,
    title: 'Stateful Orchestration Engine',
    description: 'A central orchestrator manages the entire development workflow as a stateful graph, ensuring seamless context and logical project progression.',
  },
  {
    icon: <Zap className="h-8 w-8 text-yellow-500" />,
    title: 'Persistent Contextual Knowledge',
    description: 'Agents operate on a persistent knowledge graph, ensuring that the system\'s understanding and output become more insightful and accurate over time.',
  },
  {
    icon: <ShieldCheck className="h-8 w-8 text-red-500" />,
    title: 'Systemic Observability & Governance',
    description: 'Dedicated monitoring agents observe the entire system, analyzing performance, costs, and outputs to ensure the ecosystem remains efficient and trustworthy.',
  },
  {
    icon: <Scaling className="h-8 w-8 text-indigo-500" />,
    title: 'Adaptive User Experience',
    description: 'The interface evolves with you, from a simple prompt for novices to advanced tools for designing custom agentic workflows for experts.',
  },
];

export function FeaturesSection() {
  return (
    <motion.section
      id="features"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
      className="w-full py-12 md:py-24 lg:py-32 bg-gray-50 dark:bg-gray-800"
    >
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-gray-100 px-3 py-1 text-sm dark:bg-gray-700">Key Features</div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">The Future of Application Development</h2>
            <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
              Sentient Core is built on six pillars that redefine how software is created, from initial concept to enterprise-scale deployment.
            </p>
          </div>
        </div>
        <div className="mx-auto grid max-w-5xl items-start gap-12 py-12 lg:grid-cols-3">
          {features.map((feature, index) => (
            <div key={index} className="grid gap-4">
              <div className="flex items-center gap-4">
                {feature.icon}
                <h3 className="text-xl font-bold">{feature.title}</h3>
              </div>
              <p className="text-gray-500 dark:text-gray-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </motion.section>
  );
}
