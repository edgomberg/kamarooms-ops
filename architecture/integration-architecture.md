# Kamarooms Integration Architecture

## System Topology

```
┌─────────────────────────────────────────────┐
│              AI BRAIN (Custom)               │
│  GigaChat API + Yandex GPT + Custom Models  │
│  Revenue optimization · Guest comms · Ops    │
├─────────────────────────────────────────────┤
│           ORCHESTRATION LAYER                │
│     n8n (self-hosted) or Albato              │
│     Webhooks · Scheduled jobs · Routing      │
├────────┬────────┬────────┬─────────┬────────┤
│Shelter │Travel- │ 1C ×3  │Bitrix24 │Telegram│
│Cloud   │line    │(acctg) │(CRM)    │Bot     │
│PMS     │Channel │        │         │(guest) │
│        │Manager │        │         │        │
├────────┴────────┴────────┴─────────┴────────┤
│           ANALYTICAL DATABASE                │
│     PostgreSQL on Yandex Cloud               │
│     Single source of truth for all KPIs      │
├─────────────────────────────────────────────┤
│           PUBLIC DASHBOARD                   │
│     open.kamarooms.com                       │
│     Flask API → Chart.js frontend            │
└─────────────────────────────────────────────┘
```

## System Consolidation Plan

| Current | Action | Est. Savings |
|---------|--------|-------------|
| R-Keeper + iiko (dual POS) | Pick one, kill the other | ~200-400K RUB/yr |
| Megafon VATS + Дом.ру VPBX | Consolidate to one provider | ~300-600K RUB/yr |
| Yandex 360 + Google Workspace | Complete Google migration, kill Yandex 360 | ~100K RUB/yr |
| 3× separate 1C instances | Evaluate consolidation with accountant | Complexity reduction |
| Local PMS → Shelter Cloud | Phase over 3 months | Better data access |

**Estimated annual savings: 600K-1.1M RUB/yr**

## PMS Evaluation Matrix (Phase 1 deliverable)

| Criteria | Shelter Cloud | Travelline WebPMS | Bnovo |
|----------|--------------|-------------------|-------|
| API richness | Token-based, Swagger docs | Universal API at Standard+ | Basic, less documented |
| 1C integration | Native | Via connector | Via APIX-Drive |
| Channel mgmt | Via Travelline/Bnovo | Native (102 channels) | Native (Booking/Airbnb) |
| Electronic locks | 12+ lock brands | HSU only | Limited |
| Fiscal compliance | Built-in | Built-in | Built-in |
| Cloud | Yes | Yes | Yes |
| Price | Mid-range | Mid-range | $29/mo start |

**Decision: Deferred to Phase 1.** Phase 0 proceeds PMS-agnostic.

## Data Flow (Phase 0 — Manual Extract)

```
PMS (local) ──── CSV/XLSX export ────┐
Travelline ──── Manual download ─────┤
1C ──────────── Report export ───────┼──→ Python ETL ──→ scorecard.json
Reviews ─────── Web scraper ─────────┤                      │
                                     │                      ▼
                                     │              Dashboard HTML
                                     │              (static site)
```

## Data Flow (Phase 1 — Automated)

```
PMS API ─────── webhook/poll ────────┐
Travelline ──── API ─────────────────┤
1C ──────────── API/export ──────────┼──→ n8n ──→ PostgreSQL
Reviews ─────── scraper cron ────────┤                │
                                     │                ▼
                                     │         Flask API
                                     │                │
                                     │                ▼
                                     │         Dashboard
                                     │    open.kamarooms.com
```

## Security Requirements (Phase 4, parallel)

1. **Identity:** Complete Keeper rollout (37 services), eliminate shared credentials
2. **Network:** Resolve VPN, segment guest/staff/mgmt WiFi
3. **Backups:** Automated daily backups (currently none)
4. **Compliance:** Russian Federal Law 152-FZ for guest data
5. **Credentials:** Rotate all exposed via Telegram (пароли_спа.docx)
