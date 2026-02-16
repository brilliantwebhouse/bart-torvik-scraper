# Product Requirements Document (PRD)

**Project Name:** Sports Data Scraper – Bart Torvik Edition  
**Version:** 1.0  
**Date:** February 16, 2026  
**Author:** Muhammad (with Grok assistance)  
**Repo:** https://github.com/egomes2107/SPORTS-DATA-SCRAPPER  

## 1. Overview & Purpose

Build a **fully free, automated daily web scraper** that collects college men's basketball (MBB) data from barttorvik.com and saves it as structured JSON files in a GitHub repository.

**Core Goals:**
- Run automatically once per day (no manual effort after setup).
- Collect accurate, up-to-date data from two key pages.
- Store data in clean, separate JSON files (no mixing between schedule and rankings).
- Provide historical tracking via git commits.
- Be reliable for light usage (few pages/day; scalable to ~100 pages/day later).
- Avoid paid services; use GitHub Actions only.
- Bypass common blocks (e.g., User-Agent issues seen in Google Apps Script).

**Why this project?**  
Bart Torvik (T-Rank) has excellent tempo-free stats, predictions, and rankings, but no official API or export for daily use. This scraper enables personal tracking without manual visits or paid tools like ParseHub.

## 2. Target Users & Use Cases

**Primary User:** Muhammad (personal use, basketball fan/analytics hobbyist)  
**Location/Timezone:** Pakistan (PKT) – schedule runs in UTC, but data is date-based.

**Use Cases:**
- Check today's full MBB schedule with T-Rank predictions every morning.
- Monitor daily changes in national team rankings (top teams, adj efficiencies, Barthag, etc.).
- Track historical trends by viewing git commit history of JSON files.
- Manually trigger a run anytime via GitHub Actions UI for on-demand updates.
- Later: Expand to multiple dates or team-specific pages if needed.

## 3. Features & Scope

### In-Scope
- **Data Sources (2 pages):**
  - **Schedule Page:** https://barttorvik.com/schedule.php  
    - Today's date games (default; can add ?date=YYYYMMDD param later).
    - Extract per game: time (e.g., 09:00 PM), matchup (ranked teams, away @ home), network (ESPN/ESPN+/etc.), T-Rank line (spread, predicted score, confidence %), TTQ metric, result if completed, relevant links.
  - **Rankings/Home Page:** https://barttorvik.com/  
    - Current T-Rank table (all ~350–365 D-I teams).
    - Extract per team: rank, team name (with link), conference, games played, record, AdjOE, AdjDE, Barthag/net rating, other key stats (Efg%, TOR, ORB, etc.) – at minimum top 50–100 teams.

- **Output Format:**
  - Separate files for clarity:
    - `schedule.json` → array of games + metadata (date, scraped_at, total_games).
    - `rankings.json` → array of teams + metadata (scraped_at, total_teams).
  - Clean JSON structure with timestamps.
  - Git commit on every run (creates version history for changes).

- **Automation & Triggering:**
  - Daily cron schedule (e.g., 13:00 UTC ≈ evening PKT).
  - Manual trigger via GitHub Actions "Run workflow" button.
  - Simple on-demand API-like trigger possible later (workflow_dispatch).

- **Reliability Features:**
  - Realistic User-Agent to avoid basic blocks.
  - Error handling & logging in Actions.
  - Timeout & retry logic if needed.

### Out-of-Scope (for v1)
- Email/Slack notifications.
- Full JS rendering (unless blocked – can upgrade to Playwright).
- Proxies/rotation (add if IP-blocked later).
- Data visualization/dashboard.
- Export to Google Sheets/CSV auto-push.
- Multi-year/historical backfill.

## 4. Technical Requirements

**Stack:**
- Language: Python 3.12
- Libraries: requests, beautifulsoup4 (core); optional: playwright if needed.
- Hosting/Orchestration: GitHub Actions (public repo → unlimited minutes).
- Storage: JSON files committed to repo.
- Dependencies installed via pip in workflow.

**Non-Functional:**
- Cost: $0 (public repo free tier).
- Runtime: <5–10 min per run (light volume).
- Frequency: 1x/day + manual.
- Data freshness: Daily updates.
- Error tolerance: Log failures; don't break repo.
- Legal/Ethical: Respect robots.txt; low volume; personal use only (site allows reasonable access per public comments).

## 5. Success Criteria

**MVP Acceptance:**
- Workflow runs daily without errors.
- `schedule.json` contains 30–100+ games with time, matchup, prediction, TTQ.
- `rankings.json` contains top teams with rank, name, conf, record, adj efficiencies.
- Manual run works in Actions tab.
- JSON files update/commit on each run.
- No rate-limiting/blocking observed in first week.

**Nice-to-Have (v2):**
- Add tomorrow/next week schedule.
- Parse full rankings (all teams).
- Handle date param for schedule.
- Add simple diff detection (e.g., big ranking changes).

## 6. Risks & Mitigations

- **Risk:** Site blocks scraper (User-Agent, rate limit).  
  **Mitigation:** Start with headers; add delays; switch to Playwright if needed.
- **Risk:** Page structure changes.  
  **Mitigation:** Use robust selectors; monitor logs.
- **Risk:** GitHub Actions limits (unlikely).  
  **Mitigation:** Public repo = unlimited.

## 7. Next Steps / Roadmap

1. Commit workflow YAML & scraper.py (current status).
2. Test manual run → verify JSON output.
3. Fix selectors if data missing (based on logs).
4. Monitor daily run for 3–5 days.
5. Optional: Add more pages/dates.

**Approved by:** Muhammad  
**Status:** In Development (setup phase)

Feel free to edit/add notes in the repo.