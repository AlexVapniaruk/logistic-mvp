# Frontend — Nuxt 4 + TypeScript

## Stack
Nuxt 4 · Vite 8 · TypeScript · Pinia · SCSS + BEM

## Layer responsibilities
| Layer | Rule |
|---|---|
| `pages/` | Routing + layout only. `<script setup lang="ts">`. No HTTP, no heavy logic. |
| `stores/` | State + async actions via Pinia. No raw HTTP — call `api-sdk` functions. |
| `composables/` | Reusable reactive logic only. |
| `components/` | Presentational UI. Receive props, emit events. |
| `api-sdk/` | **All HTTP lives here.** See `api-sdk/CLAUDE.md`. |

## SCSS / BEM
Structure: `assets/scss/abstracts/` · `base/` · `components/` · `layout/`
- Abstracts auto-imported in every SFC via `vite.css.preprocessorOptions`
- Use BEM: `.block__element--modifier`
- Use `@include element()` / `@include modifier()` mixins in component stylesheets
- SFC scoped styles: `<style lang="scss" scoped>`

## Rules
- Never call `$fetch` or `useFetch` directly in pages or stores — use `api-sdk/`
- All types imported from `api-sdk/types.ts`
- WebSocket via `api-sdk/ws.client.ts` only
