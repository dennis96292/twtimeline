# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Taiwan Historical Events Timeline (台灣發生了什麼?) — a static web app displaying Taiwan history from 1895 to present. No build step required; pure HTML/CSS/JS deployed to GitHub Pages.

Live site: https://dennis96292.github.io/twtimeline/

## Local Development

Serve the `web/` directory with any static file server:

```bash
# Copy data files into web/ (mirrors what CI does)
cp -r data web/data

# Serve locally
cd web && python -m http.server 8080
```

The site loads `data/events.json` at runtime. Without the copy step, data won't load locally.

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) deploys on push to `main`:
1. Copies `data/` into `web/data/`
2. Uploads `web/` as the GitHub Pages artifact

## Architecture

### Data layer

All events live in `data/events.json` (consolidated) and `data/batch_*.json` (period-based splits). The app fetches `data/events.json` once on load and holds all events in memory for client-side filtering.

Event schema (defined in `EVENT_FORMAT.md`):
```json
{
  "date": "YYYY-MM-DD",
  "title": "≤20 chars",
  "desc": "50–150 chars (optional)",
  "tags": ["政治","選舉","兩岸","外交","經濟","社會","人權","災害","疫情","環境","歷史"],
  "sources": ["https://..."]
}
```

### Frontend (`web/js/index.js`)

Single-file vanilla JS, no framework. Key globals:
- `allEvents` / `filtered` — full dataset and current search results
- `cursor` — index into `filtered` for infinite scroll (batch size: 20)
- `rowCount` — total rendered rows (drives left/right alternation)

Key functions:
- `loadBatch()` — appends next 20 events to DOM; called by IntersectionObserver on sentinel element
- `applySearch(q)` — filters `allEvents` by query (matches title, desc, tags, formatted dates), resets `cursor`/`rowCount`, re-renders
- `buildRow(ev, side, staggerIdx)` — builds one timeline card DOM node; `side` is `"left"` or `"right"`, `staggerIdx` drives CSS `--stagger` for entry animation

### Styling (`web/css/index.css`)

Dark theme (background `#0f0f0f`, accent `#FF6B00`). Timeline is a center-spine layout that collapses to left-spine single-column on mobile (`≤640px`). Card reveal animations use `opacity`/`transform` driven by the `.visible` class added by IntersectionObserver, with per-card stagger via `--stagger` CSS variable.

## Adding Events

Edit `data/events.json` (and the relevant `data/batch_*.json` if maintaining splits). Keep events sorted by date ascending. Follow the schema in `EVENT_FORMAT.md` strictly — `title` must be ≤20 characters, `tags` must be from the predefined list.
