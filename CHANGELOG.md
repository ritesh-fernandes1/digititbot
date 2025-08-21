# 📜 Changelog

All notable changes to this project will be documented in this file.

---

## [3.0.7] - 2025-08-02
### 🚀 New Features
- Added **dynamic `robots.txt` route** in `app.py` to always serve the latest version for crawlers.
- Implemented **dynamic `sitemap.xml` generation** with `<lastmod>` auto-updating to the server’s current UTC date.
- Included a **fallback static sitemap** (`/static/sitemap.xml`) for backup access.

### 🔧 Improvements
- Ensured **Google Search Console compatibility** for sitemaps and robots.txt.
- Updated SEO response headers with correct MIME types (`application/xml` for sitemaps, `text/plain` for robots.txt).
- Streamlined backend delivery of SEO files without relying on static file reads.

### 🐞 Fixes
- Resolved sitemap crawling issues by guaranteeing dynamic freshness for every Googlebot request.
- Fixed sitemap accessibility errors (`404` and `Couldn't Fetch`) reported in Search Console.

---

## [3.0.6] - 2025-08-01
- Added **dynamic `<lastmod>` field** in sitemap to auto-update daily.
- Verified sitemap accessibility via Google Search Console.

---

## [3.0.5] - 2025-07-31
- Initial SEO integration with robots.txt and sitemap.xml.
- Added Google Search Console verification route.

---

## [3.0.0 - 3.0.4] - 2025-07
- Major rewrite using **OpenAI GPT‑4 API**.
- Introduced **modern UI** with dark mode, avatars, scrollable chat, and markdown rendering.
- Added **healthcheck route** for Render diagnostics.
- Migrated deployment to **Render.com** for stability and public availability.

---

## [2.x.x] - Early Versions
- First working prototype with basic Q&A functionality.
- Local-only testing environment.

---
