"use client";

import { Server, Store, Cpu } from 'lucide-react';

const tracks = [
  {
    icon: <Server className="h-8 w-8 text-white" />,
    sponsor: 'Vultr',
    title: 'Enterprise Agentic Workflow Platform',
    description: 'Deploying the Sentient Core platform on Vultr to provide scalable, enterprise-grade agentic workflows for automating complex business intelligence tasks.',
    bgColor: 'bg-blue-600',
  },
  {
    icon: <Store className="h-8 w-8 text-white" />,
    sponsor: 'Prosus',
    title: 'Agent-Powered E-Commerce Solution',
    description: 'Building an e-commerce agent pack with knowledge graph-based user profiles and Tavily API integration for hyper-personalized shopping experiences.',
    bgColor: 'bg-green-600',
  },
  {
    icon: <Cpu className="h-8 w-8 text-white" />,
    sponsor: 'Qualcomm',
    title: 'On-Device Edge AI Utility Generator',
    description: 'Using Sentient Core to generate and compile offline-first AI utilities for Snapdragon X Elite, bridging the gap between cloud development and edge execution.',
    bgColor: 'bg-purple-600',
  },
];

export function HackathonSection() {
  return (
    <motion.section
      id="hackathon"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
      className="w-full py-12 md:py-24 lg:py-32 bg-white dark:bg-gray-900"
    >
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-gray-100 px-3 py-1 text-sm dark:bg-gray-800">Raise Your Hack</div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">Tackling the Sponsor Tracks</h2>
            <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
              Sentient Core showcases its versatility by addressing three distinct sponsor challenges, demonstrating a unified vision from cloud to edge.
            </p>
          </div>
        </div>
        <div className="mx-auto grid max-w-5xl items-stretch gap-8 py-12 lg:grid-cols-3">
          {tracks.map((track) => (
            <div key={track.sponsor} className={`flex flex-col justify-between rounded-lg p-6 text-white shadow-lg ${track.bgColor}`}>
              <div>
                <div className="mb-4 flex items-center gap-4">
                  {track.icon}
                  <h3 className="text-2xl font-bold">{track.sponsor}</h3>
                </div>
                <h4 className="mb-2 text-xl font-semibold">{track.title}</h4>
                <p className="text-gray-200">
                  {track.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.section>
  );
}
