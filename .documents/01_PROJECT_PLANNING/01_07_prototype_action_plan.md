# Prototype Action Plan (E2B + WebContainer Hybrid)

**ID:** plan:prototype:action_v1  
**Last Updated:** June 2025

---

## 0. Prerequisites
- Sentient Core repo cloned & dependencies installed.  
- E2B API key stored in `.env` (`E2B_API_KEY`).  
- COOP/COEP headers configured for local dev (`next.config.js` middleware).  
- SurrealDB & Supabase services running via Docker-Compose.

## 1. Sandbox Tooling Layer
| Step | Task | Owner | Status |
|------|------|-------|--------|
| 1.1 | Implement `WebContainerTool` wrapper (Typescript) | Front-End Agent | ☐ |
| 1.2 | Implement `E2BSandboxTool` wrapper (Python) | Back-End Agent | ☐ |
| 1.3 | Add `Chooser` utility (Decision Tree §3) | Core Agent | ☐ |
| 1.4 | Persist Desktop IDs in SurrealDB | Persistence Agent | ☐ |
| 1.5 | Snapshot export endpoint (WC tar) | Front-End Agent | ☐ |

## 2. Agent Graph Wiring
| Step | Task | Owner | Status |
|------|------|-------|--------|
| 2.1 | Update LangGraph definition to include new tools | Architecting Agent | ☐ |
| 2.2 | Configure graph service in `sentient-brain-smithery` | Back-End Agent | ☐ |
| 2.3 | Add audit log streams to Weaviate | Full-Stack Agent | ☐ |

## 3. UI Integration
| Step | Task | Owner | Status |
|------|------|-------|--------|
| 3.1 | Embed WC iframe with live port proxy | Front-End Agent | ☐ |
| 3.2 | Build sandbox status panel (RAM, CPU) | Front-End Agent | ☐ |
| 3.3 | Implement log console component (SSE) | Front-End Agent | ☐ |

## 4. Testing & QA
| Step | Task | Owner | Status |
|------|------|-------|--------|
| 4.1 | Unit tests for tool wrappers (pytest, vitest) | Testing Agent | ☐ |
| 4.2 | E2B quota exhaustion scenario | Testing Agent | ☐ |
| 4.3 | WC offline / Safari fallback test | Testing Agent | ☐ |

## 5. Milestones & Timeline
| Week | Deliverable |
|------|-------------|
| 1 | Tool wrappers + Chooser MVP |
| 2 | Agent graph updated & backend endpoints |
| 3 | UI sandbox embed + live preview |
| 4 | Persistence & audit logging |
| 5 | Comprehensive QA & docs freeze |

## 6. Dependencies & Risks
- **E2B pricing**: Ensure budget for desktop hours.  
- **Browser isolation policies**: Potential breakage on older browsers.  
- **Cross-tool latency**: Watch for overhead when switching between sandboxes.

## 7. Next Steps
1. Assign owners (update table).  
2. Kick-off implementation for Step 1.1 and 1.2 in parallel.  
3. Schedule weekly check-ins; update this doc accordingly.

---
*Prepared by Sentient Core Tech-Research agent, June 2025*
