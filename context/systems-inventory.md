# Kamarooms — Systems Inventory ("The Zoo")

15+ systems, **not integrated**. No centralized identity management, no network segmentation, no automated backup.

## IT Assessment (Ed, Feb 11): Grade D/C
"Отель местами держится на ручном управлении и «героизме» отдельных людей. Если завтра ключевой админ выиграет в лотерею и улетит на Бали — мы встанем."

**Target:** B (Твёрдый стандарт) within 6 months.
**Approach:** "Суверенная Инфраструктура" — own the keys, no sanction dependency, no vendor lock-in. Copy Marriott architectural principles on OpenSource/Linux stack.

## Core Operations

| System | Purpose | Status | Notes |
|--------|---------|--------|-------|
| **1C Hotel** | Hotel accounting | Active | Managed by GM/Finance. One of THREE separate 1C instances. |
| **1C SPA** | SPA accounting | Active | Separate instance from Hotel 1C. |
| **1C Бухгалтерия** | Corporate accounting | Active | Main financial system. Natalia manages. |
| **Local PMS** | Hotel property management | Active | Needs data export for audit. Dashboard data discrepancies vs Natalia's entries. |
| **R-Keeper** | Restaurant POS | Active | Used at restaurant "Boho". |
| **iiko** | Restaurant POS (Admin) | Active | Listed in Keeper tracker alongside R-Keeper — potentially redundant. Investigate. |
| **StoreHouse** | Restaurant inventory/server | Active | Server-based. Listed in Keeper tracker. |
| **Travelline** | Channel manager / booking engine | Active | Visible on kamarooms.com. Handles OTA distribution. Owner: Ревенью/Ресепшн. |
| **Bitrix24** | CRM | Active @ crm.spa-list.ru | NEW contractor being evaluated for CRM funnels (Mar 13). Ludmila driving. Khalim manages current. |

## Guest-Facing

| System | Purpose | Status |
|--------|---------|--------|
| **2roomz** | Mobile guest services / chat widget | Active @ kamarooms.2roomz.com |
| **Tilda** | Website CMS | Active @ kamarooms.com (kamarooms.ru does NOT resolve) |

## Communication & IT

| System | Purpose | Status | Notes |
|--------|---------|--------|-------|
| **Yandex 360** | Current email/office suite | Active — being replaced | Migration to Google Workspace in progress |
| **Google Workspace** | Email/office (target) | Migration in progress | Domain: kamarooms.org (adminkama@kamarooms.org active). kamarooms.net planned but NOT set up. Billing being moved to company PST.net card (Feb 19). Security alert Mar 2. |
| **Megafon VATS** | Telephony (АТС) | Active | Managed by Khalim. Owner: Людмила/GM. B2B contract. |
| **Дом.ру VPBX** | Secondary phone system | Active | Discovered via Keeper tracker. DUAL phone systems running — consolidation candidate. |
| **Keeper** | Password management | Rolled out Feb 19-20 | Cloud migration in progress. Staff struggled with adoption. 37 services mapped, ALL "ToDo" status — migration incomplete. Triggered by Dec 28 fraud incident (14,750 RUB loss). |

## Analytics & Management

| System | Purpose | Status |
|--------|---------|--------|
| **Yandex Metrica** | Website analytics | Active |
| **Notion** | HQ pages, role blueprints, checklists | Active |
| **Google Sheets** | Owner Dashboard, Cash Flow tracking | Active — being filled since Mar 12 |

## Payment Infrastructure

| System | Purpose | Status |
|--------|---------|--------|
| **PST.net** | Virtual US BIN cards for international payments | Being set up (Feb 19) |
| **USDT (TRC-20)** | Crypto bridge for PST funding | Active — Ed funds |
| **Robokassa (ПУЛЬС)** | Payment gateway for ООО Пульс (hotel) | Active |
| **Robokassa (ЮНОСТЬ)** | Payment gateway for second entity | Active — entity "ЮНОСТЬ" needs identification |
| **ЮKassa** | Payment gateway | Active |
| **Alfa-Bank** | юр.лицо online banking | Active |
| **Sberbank** | юр.лицо online banking | Active |
| **VTB** | юр.лицо online banking | Active |

## Ad & Marketing Platforms

| System | Purpose | Status |
|--------|---------|--------|
| **eLama** | Ad management platform | Active — both Kamarooms and Cubrooms |
| **2GIS** | Business listing + ads | Active |
| **Avito** | Listing platform | Active |
| **Яндекс.Карты / Яндекс Бизнес** | Business listing | Active |

## Unknown Entity: Cubrooms

Discovered in Keeper import template. Has its own:
- Google account, eLama ads, 2GIS listing, Яндекс.Карты listing
- Email: info@cubrooms.com, cubrooms@yandex.ru
- **Status:** Unknown entity — needs investigation. May be a sub-brand, different property, or concept.

## Domains & Web Properties
- **kamarooms.com** — Active (Tilda CMS)
- **kamarooms.ru** — Does NOT resolve
- **kamarooms.org** — Google Workspace admin domain
- **kamarooms.net** — Planned but NOT set up
- **spa-list.ru** — SPA CRM (Bitrix)
- **kamarooms.2roomz.com** — Guest services
- **Ownership audit:** INCOMPLETE — who owns each domain (юрлицо vs физлицо) unknown per Dmitry's audit questions

## Known Critical Gaps (from Dmitry's Stage 2 Audit)
1. **No network segmentation** — guest WiFi may see office network
2. **No centralized identity management** — shared logins (admin, reception, bar) likely in use
3. **No automated backup** — single point of failure on key systems
4. **No offboarding checklist** — ex-employee access not systematically revoked
5. **No IT helpdesk** — problems reported via WhatsApp to personal phones
6. **BYOD risk** — unknown how many staff use personal devices
7. **License audit incomplete** — Windows licensing, antivirus status unknown
8. **Vendor dependency** — unclear who has root access to router/network equipment
9. **WiFi compliance** — ФЗ-97 guest identification status unknown

## Online Reputation
- **Booking.com:** 9.4
- **Yandex:** 5.0 ("Good Place 2026" winner)
- **2GIS:** 4.8 (392 reviews, "Best Hotel 2025")

## Google Drive Resources
- Floor plans: https://drive.google.com/drive/folders/1ZHMa1Sw-N-CwgXiDhVfmugQWwIRy9M_r
- Current dashboards/KPIs: https://drive.google.com/drive/folders/1m2W5CtB16XVfyezAqLkXpptdjhzBlLeA
- Loom training videos shared by Ed to Dmitry
