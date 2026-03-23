# kamarooms-ops — Claude Context

## What This Is

IT transformation ops for Kamarooms hotel (108 rooms, 4★, Naberezhnye Chelny, Tatarstan).
Day-to-day collaborators: Ed Gomberg (strategy, product) + Dmitry Karaev (IT architecture).

## Scope

**Dmitry Karaev (IT Consultant):**
- IT infrastructure: network, servers, workstations, MDM
- Integration architecture: 1C, Travelline, Bitrix24, Yandex Cloud
- 1C web client migration (thin client → browser-based)
- System consolidation (15+ systems → unified stack)

**Ed Gomberg (Strategy):**
- Product direction, stakeholder management, finance
- Dashboard and transparency page
- Team coordination and vendor decisions

## What's NOT Here

Financial audits, valuation models, sale considerations, personal contacts,
stakeholder communications, telegram analysis. Those live in a private repo.

## Import Conventions

- **dashboard/** contains the open transparency page generator. Run: `cd dashboard && python generate_open_page.py`
- **architecture/** has the system topology, 1C research, phase timeline, and KPI scorecard structure
- **context/** has hotel profile, systems inventory, IT literacy roadmap, team directory (roles only)
- **environment/** has Mac setup specs and MDM plan
- **config/** has static JSON configs (future)
- **data/** has runtime output (gitignored). Use `KAMAROOMS_OPS_DIR` env var or default to `data/`
- Never reference external repos or private paths

## Key Files

| File | Purpose |
|------|---------|
| `architecture/integration-architecture.md` | System topology + consolidation plan |
| `architecture/1c-integration-research.md` | 8 open questions on 1C migration |
| `architecture/phase-timeline.md` | 4-stage IT transformation roadmap |
| `architecture/database-schema.sql` | PostgreSQL target schema |
| `architecture/scorecard.json` | KPI structure (no actual values) |
| `context/systems-inventory.md` | The 15-system zoo |
| `context/hotel-profile.md` | Public hotel facts |
| `context/it-literacy-roadmap.md` | Staff digital skills plan |
| `dashboard/generate_open_page.py` | Jinja2 transparency page generator |

## Language

Russian for docs (hotel context). English for code, config, and commit messages.

## Testing

```bash
python -m pytest tests/
```
