# kamarooms-ops

IT-трансформация гостиницы «Камские палаты» (Kamarooms Business Hotel & SPA).

Kamarooms hotel IT transformation. 108 rooms, 4★, Naberezhnye Chelny, Tatarstan.

## Быстрый старт / Quick Start

```bash
# 1. Clone
git clone git@github.com:edgomberg/kamarooms-ops.git
cd kamarooms-ops

# 2. Read
# CLAUDE.md — AI collaboration contract, scope, key files
# README.md — this file

# 3. Explore
# architecture/  — system topology, 1C research, transformation roadmap
# context/       — hotel profile, 15+ systems inventory, team directory

# 4. Dashboard (optional)
pip install jinja2
cd dashboard && python generate_open_page.py
# Output: dashboard/dist/
```

## Структура / Structure

```
kamarooms-ops/
├── CLAUDE.md                    # AI collaboration contract
├── README.md                    # This file
├── .env.example                 # API keys template
│
├── architecture/                # System design & roadmap
│   ├── integration-architecture.md   # System topology diagram
│   ├── 1c-integration-research.md    # 8 open questions on 1C
│   ├── phase-timeline.md             # 4-stage transformation
│   ├── database-schema.sql           # PostgreSQL target
│   └── scorecard.json                # KPI structure
│
├── context/                     # Hotel & team context
│   ├── hotel-profile.md               # Public hotel facts
│   ├── systems-inventory.md           # 15+ current systems
│   ├── it-literacy-roadmap.md         # Staff digital skills
│   └── team-directory-ops.md          # Roles & departments
│
├── environment/                 # Device & MDM specs
│   ├── mac-setup-spec.md              # Standard config per role
│   └── mdm-plan.md                    # Mosyle Fuse setup
│
├── dashboard/                   # Transparency page
│   ├── generate_open_page.py          # Jinja2 generator
│   ├── templates/                     # HTML templates
│   └── dist/                          # Built static site
│
├── pipelines/                   # Data extraction (future)
├── lib/                         # Shared modules (future)
├── config/                      # Static JSON configs
├── data/                        # Runtime output (gitignored)
├── deploy/                      # Server deployment
├── tests/                       # Verification tests
└── docs/                        # CE documentation
    ├── brainstorms/
    ├── plans/
    ├── runbooks/
    └── solutions/
```

## Ключевые документы / Key Docs

| Документ | Описание |
|----------|----------|
| `architecture/integration-architecture.md` | Топология систем + план консолидации |
| `architecture/1c-integration-research.md` | 8 открытых вопросов по миграции 1С |
| `context/systems-inventory.md` | 15+ текущих систем ("Зоопарк") |
| `architecture/phase-timeline.md` | 4-этапная дорожная карта трансформации |
| `environment/mac-setup-spec.md` | Стандартная конфигурация Mac по ролям |

## Приоритеты / Priorities

1. **1C веб-клиент** — Миграция с тонкого клиента на браузер (Chrome). Снимает проблемы с установкой и обновлениями.
2. **Консолидация систем** — 15+ разрозненных систем → единый стек с PostgreSQL.
3. **Сеть и инфраструктура** — Mikrotik, сегментация, скорость интернета.

## Кто работает / Team

- **Эд Гомберг** — стратегия, продукт, дашборд
- **Дмитрий Караев** — IT-архитектура, интеграции, 1С
