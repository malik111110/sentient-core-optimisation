# WebContainer Advanced Integration Guide

**ID:** guide:feature:webcontainer_integration_v2  
**Source Reference(s):** https://webcontainer.io/docs, https://github.com/stackblitz/webcontainer-core  
**Last Validated:** June 2025

---

## 1. Purpose
StackBlitz WebContainers run a full, secure, WASM-based Node.js runtime **inside the browser**. They power instant dev-environments and enable rich client-side tooling. This guide captures the latest (v1.2.x) API surface and shows how Sentient Core can embed WebContainers for UI-centric agent workflows.

## 2. Architecture Overview
```
Browser Tab
│
├─ WebAssembly Sandbox (WebContainer Runtime)
│   ├─ Virtual FS (IndexedDB-backed)
│   ├─ Node.js 20 LTS (WASM build)
│   ├─ Process Scheduler & PTY emulation
│   └─ TCP → Service Worker → iframe (port proxy)
│
├─ @webcontainer/api (JS lib in main thread)
│
└─ Sentient Core UI (React / Next.js)
```
Key takeaways:
* **Isolation:** No host FS/network access beyond fetch/XHR out of browser sandbox.
* **Persistence:** FS saved in IndexedDB per-origin; can snapshot/export.
* **Port Proxy:** HTTP servers started inside container become reachable at random `https://<hash>.stackblitz.io` URLs.

## 3. Installation
```bash
npm install @webcontainer/api@^1.2.0
```
> Requires `crossorigin-isolation`; configure headers via Next.js middleware or Cloudflare Worker.

## 4. Boot Sequence (Updated)
```ts
import { WebContainer } from '@webcontainer/api';

export async function bootWC(projectFiles) {
  const wc = await WebContainer.boot({
    coepCredentialless: true, // new option (v1.2) simplifies isolation
    filesystem: projectFiles, // optional initial FS tree
  });
  return wc;
}
```

### 4.1 Progressive Mounting
Use `wc.fs.mkdir()` + `wc.fs.writeFile()` for lazy loading; speeds up first paint.

### 4.2 Dev Server Detection
```ts
wc.on('server-ready', ({port, url}) => {
  console.log('Dev server running on', port, url);
});
```

## 5. Common Recipes
### 5.1 Vite + React Quickstart
```ts
await wc.spawn('npm', ['create', 'vite@latest', 'app', '--', '--template', 'react']);
```

### 5.2 Running Playwright Tests
```ts
await wc.spawn('npx', ['playwright', 'install', '--with-deps']);
await wc.spawn('npm', ['run', 'test']);
```

### 5.3 Persisting Project Snapshot
```ts
const tarball = await wc.export('/'); // returns Uint8Array tar
saveAs(new Blob([tarball]), 'snapshot.tar');
```

## 6. Integration Patterns in Sentient Core
| Pattern | Description | UI Impact |
|---------|-------------|-----------|
| **Live Demo Sandboxes** | Let AI Front-End agent write code, instantly preview result in iframe | Real-time feedback loop |
| **Tutorial Steps** | Pre-mount lesson files, run commands sequentially | Step indicator sync |
| **Code Diff Review** | Fork snapshot, apply patch, run tests | Visual diff viewer |
| **Client-Side Build** | Run `tsc`, `esbuild` in WC instead of server | Offload compute to client |

## 7. Limitations & Work-arounds (2025)
* No native modules (`node-gyp`) – stick to pure JS packages.
* Max RAM ~ 512 MB; heavy builds may crash.
* SharedArrayBuffer needs isolation; Safari TP required until stable.
* No true multithreading yet; use web-workers outside WC.

## 8. Security Considerations
* **Origin-Scoped FS:** cannot leak across domains.
* **CSP:** Restrict `script-src` to `'self'` and StackBlitz CDN.
* **Malicious Code:** Run only within WC; never eval in main thread.

## 9. Performance Tips
* **Pre-warm Boot:** `WebContainer.boot()` at page load; show skeleton UI until ready.
* **Incremental FS Writes:** Avoid mounting node_modules; run `npm install` inside WC.
* **Log Streaming:** Pipe to `WritableStream` throttled to keep UI responsive.

## 10. Sentient Core Roadmap Alignment
| Milestone | Benefit |
|-----------|---------|
| Week 1-2 | Rapid UI prototyping, live preview |
| Week 3-4 | User-guided tutorials in "YOLO" mode |
| Week 5-6 | On-device compilation/bundling to reduce backend load |

## 11. References
* Official docs – <https://webcontainer.io/docs>
* API – <https://github.com/stackblitz/webcontainer-core/tree/main/docs>
* Example starter – <https://github.com/stackblitz/webcontainer-api-starter>

---
*Prepared by Sentient Core Tech-Research agent, June 2025*
