# Phase 03 — Web Platform Engineering
**Department:** Frontend Engineering | **Course:** CIS 195 — Web Development | **Status:** Complete

---

## Purpose

Establish FLLC's web platform capability — from semantic HTML structure and responsive CSS systems to JavaScript DOM frameworks and REST API integration patterns. These components form the presentation layer of the enterprise platform.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`portfolio.html`](portfolio.html) | Professional portfolio SPA | Semantic HTML5, CSS custom properties, flexbox, grid, sticky nav, timeline component, skill bars, card hover effects, responsive breakpoints |
| [`dom_manipulation.js`](dom_manipulation.js) | DOM manipulation framework | Element factory, event delegation, classList API, localStorage persistence, full TaskManager app (CRUD + filter + stats), modal system |
| [`responsive_design.css`](responsive_design.css) | Enterprise design system | Mobile-first methodology, 4 breakpoints (600/1024/1400px), CSS Grid dashboard layout, dark/light theme toggle, print styles, accessibility (reduced motion, screen reader) |
| [`rest_api.js`](rest_api.js) | REST API client library | `fetch()`, async/await, all HTTP verbs (GET/POST/PUT/DELETE), query parameters, AbortController timeout, retry with exponential backoff, reusable `APIClient` class, pagination, dynamic DOM rendering |

## Enterprise Application

- **Phase 09** integrates the API client patterns with the production REST API
- Design system CSS feeds into the `index.html` coursework portal
- DOM framework patterns apply to any FLLC web application
