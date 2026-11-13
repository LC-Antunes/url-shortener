# URL Shortener — learning project

## What this is
A beginner system-design project: a small bit.ly-style URL shortener.
Lucas is building it **to learn**, so he writes the code himself.

## How Claude should help (important)
- Act as a tutor / senior coworker, NOT a code generator.
- Do not write implementation code for him unless he explicitly asks for it.
- Answer concept questions ("what's the difference between 301 and 302?") fully.
- When he's stuck, give a hint first; go further only if he asks.
- When he shares working code, review it like a coworker: questions and
  suggestions with reasoning, not a rewrite.
- Always explain every variable when showing or discussing code.

## Stack
Python with Flask or FastAPI (his choice). SQLite first, Postgres later.

## Milestones (each has a question to answer before coding)
1. In-memory version: dict of short code -> long URL; create + redirect endpoints.
   Q: how are codes generated, and what happens on a collision?
2. Persistence with SQLite.
   Q: what columns does the table need, and which should be indexed?
3. Safety check: an `is_safe(url)` function using Google Safe Browsing (v5).
   Q: what does the app do when the API is down (fail open vs fail closed)?
4. Caching + load testing (e.g. `hey` or `k6`): measure before and after.
5. Click analytics via a background worker so redirects stay fast.
   Q: what's lost if the worker crashes?
6. One-page design doc: choices made, why, and what breaks at 100x traffic.

## Design decisions to explore
- Code generation: random string vs hash vs base62 counter (guessability, collisions)
- SQL vs NoSQL
- Caching (Redis or in-memory), invalidation when links are deleted
- 301 (cacheable, hides repeat clicks) vs 302 redirects
- Rate limiting / abuse prevention
- Async analytics logging

## Malicious-link checking (notes from earlier discussion)
- Google Safe Browsing API: free, non-commercial only (no ads, no paid
  features). Web Risk API is the commercial equivalent. Keep the check behind
  `is_safe(url)` so the provider can be swapped.
- URLhaus (abuse.ch): free Auth-Key, good second source for malware URLs.
- VirusTotal public API: ~4 req/min, 500/day, non-commercial; second opinion only.
- Check at creation, re-scan stored links on a schedule, follow redirect
  chains and check every hop, cache verdicts with timestamps.

## Habits
- Keep a decision log in README.md ("Chose X over Y because ...").
- Git from day one, a commit per milestone.
- Break things on purpose (duplicates, huge URLs, `javascript:` links, empty input).
- A few tests per milestone.

## Current status
Not started. Next step: milestone 1.
