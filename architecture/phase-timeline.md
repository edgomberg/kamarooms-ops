# Kamarooms AI-Native Architecture — Implementation Timeline

## Phase Overview

```
WEEK  1  2  3  4  5  6  7  8  9  10  11  12  16  20  24
      ├──────────────┤
      Phase 0: Measure (scorecard + data extraction + dashboard v1)
               ├─────────────────────┤
               Phase 1: Data Layer (PMS decision + integration + consolidation)
                        ├──────────────────────────────────┤
                        Phase 2: AI Agents (revenue → guest → ops)
                                                ├──────────────────────┤
                                                Phase 3: Franchise Package
      ├──────────────────────────────────────────────────────┤
      Phase 4: Security (continuous, parallel)
```

## Phase 0: Measure Before You Move (Weeks 1-4)

**Deliverable:** All 10 KPIs have 12mo historical data, dashboard live, daily auto-refresh working.

| Week | Task | Owner | Status |
|------|------|-------|--------|
| 1 | Define 10 KPIs in scorecard.json | Ed + Claude | DONE |
| 1 | Extract PMS data (12mo daily: occ, ADR, RevPAR) | Semen + Ed | TODO — need PMS export |
| 1 | Extract Travelline data (channel mix, commissions) | Semen | TODO — need TL admin access |
| 1-2 | Extract 1C financials (monthly P&L, payroll, utilities) | Natalia / Semen | TODO — need 1C report |
| 2 | Scrape review ratings (Booking, Yandex, 2GIS) | Claude automated | TODO |
| 2-3 | Build dashboard v1 (static HTML) | Ed + Claude | DONE — generator built |
| 3-4 | Deploy dashboard (Yandex Cloud or VPS) | Semen / Ed | TODO |
| 4 | Dashboard live with daily refresh | — | TODO |

## Phase 1: Unified Data Layer (Weeks 3-8)

**Deliverable:** Single API call retrieves today's occupancy, ADR, RevPAR, channel mix.

| Week | Task | Owner | Status |
|------|------|-------|--------|
| 3-4 | Deep PMS evaluation (Shelter vs TL WebPMS vs Bnovo vs keep) | Ed + Dmitry | TODO |
| 4-5 | Set up PostgreSQL on Yandex Cloud | Semen / Dmitry | TODO |
| 5-6 | Build ETL pipelines (PMS → DB, 1C → DB, TL → DB) | Ed + Claude | TODO |
| 6-7 | Set up n8n (self-hosted) for orchestration | Semen / Dmitry | TODO |
| 7-8 | System consolidation: pick R-Keeper vs iiko, consolidate telephony | Ludmila + Ed | TODO |
| 8 | Flask API serving dashboard from DB | Ed + Claude | TODO |

## Phase 2: AI Agents (Weeks 6-16)

**Deliverable:** Revenue agent running 30 days with human approval, measurable ADR impact.

| Week | Task | Owner | Status |
|------|------|-------|--------|
| 6-8 | Revenue agent v1: rules-based rate suggestions | Ed + Claude | SCAFFOLD BUILT |
| 8-10 | Competitor scraper operational | Ed + Claude | SCAFFOLD BUILT |
| 10-12 | Revenue agent v2: GigaChat/YandexGPT integration | Ed | TODO |
| 10-12 | Guest communication Telegram bot | Ed + Claude | TODO |
| 12-14 | Operations intelligence agent (daily briefing) | Ed + Claude | TODO |
| 14-16 | 30-day revenue agent validation period | Ludmila | TODO |

## Phase 3: Franchise-Ready Package (Months 4-8)

**Deliverable:** Second property onboardable in < 2 weeks using KOS.

| Month | Task | Owner | Status |
|-------|------|-------|--------|
| 4-5 | Package PMS + AI stack as deployable system | Ed | TODO |
| 5-6 | Build franchise unit economics model | Ed + Claude | TODO |
| 6-7 | Training materials for AI-augmented ops | Ed + Ludmila | TODO |
| 7-8 | Dashboard as franchise marketing asset | Ed | TODO |

## Phase 4: Security Foundation (Weeks 1-12, parallel)

| Week | Task | Owner | Status |
|------|------|-------|--------|
| 1-2 | Complete Keeper rollout (37 services) | Semen + Vladimir | IN PROGRESS |
| 2-4 | Eliminate shared credentials | Semen | TODO |
| 3-6 | Resolve VPN instability | Dmitry / Semen | BLOCKED (5+ weeks) |
| 4-8 | Network segmentation | Dmitry | TODO |
| 6-10 | Automated backups | Semen | TODO |
| 8-12 | 152-FZ compliance audit | Natalia + external | TODO |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Staff IT fatigue | Adoption failure | Phase 0 = measurement only, no new staff tools |
| PMS migration disruption | Revenue loss | 30-day parallel running |
| AI quality (GigaChat/YandexGPT) | Bad rate suggestions | Human approval loop, 60-day validation |
| Core objective undecided | Wasted franchise investment | Phases 0-2 deliver value regardless |
| Dmitry engagement stalled | No IT partner | Plan proceeds without Dmitry |

## Budget Estimate

| Item | One-time | Monthly | Notes |
|------|----------|---------|-------|
| Yandex Cloud (PostgreSQL + VPS) | — | 5-15K RUB | Depends on instance size |
| PMS license (Shelter Cloud) | — | 30-60K RUB | If switching |
| n8n hosting | — | 0 (self-hosted) | On same VPS |
| Custom AI dev (Claude Code) | — | via Ed's time | No additional cost |
| GigaChat API | — | 5-15K RUB | Usage-based |
| Domain + SSL | 2K RUB | — | open.kamarooms.com |
| **Total estimate** | **~2K RUB** | **40-90K RUB/mo** | Conservative |
