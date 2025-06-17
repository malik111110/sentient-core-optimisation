# Next.js 15 - Developer Guide

This guide summarizes the key features, changes, and improvements introduced in Next.js 15, based on the official release announcements from `nextjs.org`.

## 1. Core Upgrades

### a. React 19 Support

Next.js 15 is built on and fully supports **React 19**. This is the most significant update, unlocking new capabilities for both client and server components. Developers can now leverage new React APIs directly, including:
*   **React Actions:** Simplifies data mutations and state management by allowing functions to be passed from Server Components to client-side forms.
*   **New Hooks:** `useFormState`, `useFormStatus`, and `useOptimistic` are now available for building more robust and user-friendly forms and interactive components.

### b. Turbopack is Now Stable for Development

The Rust-based bundler, **Turbopack**, is now stable for `next dev`.
*   **How to use:** Run your development server with the `--turbo` flag: `next dev --turbo`.
*   **Performance:** Offers significant speed improvements for local development, including up to 53% faster server startup and 96% faster code updates with Fast Refresh.

## 2. Key Features and API Changes

### a. Breaking Change: Caching Behavior

This is a critical change from Next.js 14. In Next.js 15, **`fetch` requests are no longer cached by default**.
*   **Old Behavior (Next.js 14):** `fetch` requests were automatically cached.
*   **New Behavior (Next.js 15):** You must explicitly opt-in to caching for each request.
*   **How to Cache:**
    *   Use the `next.revalidate` option: `fetch('...', { next: { revalidate: 3600 } })`
    *   Use the standard `cache: 'force-cache'` option.
*   **Impact:** This change gives developers more control and prevents unintentional caching of dynamic data. All existing data-fetching code should be reviewed to ensure caching is applied where needed.

### b. New `<Form>` Component (`next/form`)

To complement React 19's Actions, Next.js 15 introduces a new `<Form>` component. This component simplifies form handling by abstracting away some of the boilerplate associated with `useFormState` and `useFormStatus`.

### c. Partial Prerendering (Experimental)

Partial Prerendering (PPR) is a new, experimental rendering model.
*   **Concept:** It allows a page to be served with a static, prerendered shell, while dynamic parts ("holes") are streamed in asynchronously.
*   **Goal:** Combines the performance of static sites with the full dynamism of server-rendered apps.
*   **Status:** As it is experimental, it should be used with caution in production.

## 3. Tooling and Developer Experience

### a. Upgrading to Next.js 15

Next.js provides an automated command-line tool to help with the upgrade process:
```bash
npx @next/codemod@canary upgrade latest
```
Alternatively, you can upgrade manually:
```bash
npm install next@latest react@rc react-dom@rc
```

### b. ESLint 9 Support

Next.js 15 adds support for ESLint 9, while maintaining backward compatibility with ESLint 8, allowing for a flexible transition.

### c. Improved `create-next-app`

The project scaffolding tool has been updated to be faster and includes new prompts for configuring your project, such as enabling Turbopack from the start.

## 4. Summary for Hackathon Implementation

*   **Embrace React 19:** Utilize Server Actions for data mutations to build robust forms for user interactions (e.g., in the Prosus e-commerce track).
*   **Use Turbopack:** Enable `--turbo` in development for a faster, more efficient workflow.
*   **Verify Caching:** Double-check all `fetch` calls to ensure that data that should be cached (like product information) is explicitly configured to do so.
*   **Forms:** Use the new `<Form>` component to simplify UI development.
