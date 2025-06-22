# Technology Synthesis & Integration Strategy

**ID:** guide:strategy:tech_synthesis_v1  
**Last Validated:** June 2025

---

## 1. Overview
This document maps Sentient Core prototype requirements (per *blue-print-sentient-core.md* and *prototype-build-outline.md*) to the capabilities of **E2B** and **WebContainers**, defining when and how each sandbox should be invoked by agents.

## 2. Capability Matrix
| Capability | E2B | WebContainer | Primary Use Case |
|------------|-----|--------------|------------------|
| Run Python / Linux CLI | ✅ | 🚫 (Node-only) | Backend code interpreter, data ETL |
| Run Node.js & Front-end dev servers | ⚠️ (via nvm) | ✅ | Live UI preview, tutorials |
| Stateful Sessions (hours) | ✅ | ♻️ (IndexedDB per tab) | Long data pipelines |
| Offline / Client-only | 🚫 | ✅ | Low-latency prototyping |
| Resource Quota | Org-level (RAM/CPU) | Browser RAM (~512 MB) | Governance planning |
| Network Isolation | Configurable ACL | Same-origin only | Security |
| Snapshot / Export | API Tarball | `wc.export()` | Reproducible builds |

## 3. Decision Tree
1. **Does task need Python or external binaries?** → *Use E2B Desktop*.
2. **Is immediate UI feedback required, Node.js only?** → *Use WebContainer*.
3. **Is offline usage mandatory?** → *WebContainer* (cached WASM bundle).
4. **Is data sensitive / requires outbound net block?** → *E2B with ACL*.

## 4. Integration Blueprint
```
Agent Graph (LangGraph)
│
├─ FrontEndAgent ──┬─> WebContainerTool
│                  └─> SnapshotTool (export tar)
│
├─ BackEndAgent ───┬─> E2BSandboxTool
│                  └─> PersistDesktopTool (SurrealDB)
│
└─ Coordinator ────> Chooser (based on Decision Tree)
```

### 4.1 Tool Interfaces
```ts
interface WebContainerToolInput { files: FileTree; commands: string[]; }
interface E2BSandboxToolInput   { language: 'python'|'node'; script: string; }
```

## 5. Security & Compliance
* E2B tokens stored in Supabase secrets table; refreshed via serverless cron.
* WebContainer runs client-side; ensure CSP + COOP/COEP headers.
* Unified audit log: propagate stdout/stderr + metadata to Weaviate knowledge store.

## 6. Roadmap Alignment & Milestones
| Timeline | Deliverable | Responsible |
|----------|-------------|-------------|
| Week 1 | Implement Chooser utility | Core team |
| Week 2 | Wrap WebContainerTool | Front-end agent |
| Week 3 | Wrap E2BSandboxTool | Back-end agent |
| Week 4 | PersistDesktopTool + SnapshotTool | Persistence agent |
| Week 5 | UI dashboards & audit log | UX team |

## 7. Open Questions
1. Do we require GPU access in sandbox (e.g., for WebGL)? → TBD.
2. How to handle secret injection in WebContainer? (likely via env file mount)
3. Cost benchmarking between E2B minutes vs. server-hosted containers.

---
*Prepared by Sentient Core Tech-Research agent, June 2025*
