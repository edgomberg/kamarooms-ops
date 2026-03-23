# 1C:Enterprise Integration Research — Kamarooms

*Research date: March 22, 2026*
*Purpose: Inform conversation with Dmitry Karaev about pulling financial data from 3 x 1C instances*

---

## Current State

You already have scaffolding built:

| Asset | Path | What It Does |
|-------|------|-------------|
| `pull_1c.py` | `scripts/kamarooms/pull_1c.py` | OData client over Tailscale — pulls revenue, expenses, cash, occupancy, guests, employees |
| `extract_1c.py` | `projects/kamarooms/scripts/data-extraction/extract_1c.py` | Parses Excel/CSV 1C exports offline (P&L, intercompany, ФОТ) |
| systemd timer | `ops-hub/systemd/kamarooms-1c-pull.*` | Daily pull at 04:00 UTC (07:00 MSK) |
| Data request | `projects/kamarooms/audit/chelny-visit/1c-data-request.md` | Russian-language data request for Natalia (5 exports) |
| Sample output | `outputs/kamarooms/daily-1c-pull.json` | Sample JSON structure (not live data yet) |

**Bottom line:** The code is ready. The blocker is server-side setup — publishing OData on 1C's web server + Tailscale connectivity.

---

## 1. Integration Methods Available in 1C:Enterprise 8

From most to least modern:

### A. OData / REST Interface (RECOMMENDED)

- **Protocol:** OData v3 (not v4), built into platform since 8.3.5
- **Format:** JSON or Atom/XML
- **Operations:** GET (read), POST (create), PATCH (update), DELETE
- **What's accessible:** Catalogs, documents, constants, enumerations, all register types (accumulation, accounting, information), charts of accounts, business processes, tasks, document journals
- **URL pattern:** `http://<server>:<port>/<database>/odata/standard.odata/<EntityName>`
- **How to enable:** In 1C Designer: Administration > Publish to Web Server > check "Publish standard OData interface"
- **Web server required:** Apache 2.2/2.4 or IIS on the 1C server machine

This is what `pull_1c.py` is already built to use. Endpoint names use Cyrillic (e.g., `Document_РеализацияТоваровУслуг`, `Catalog_Контрагенты`).

### B. Custom HTTP Services (1С: HTTP-сервисы)

- Built into platform since 8.3.9
- You write custom endpoints in 1C's built-in language (1C BSL)
- More control than OData — can return exactly the JSON structure you need
- Requires a 1C developer to write the service code
- Published the same way (Designer > Publish to Web Server)
- Better for complex queries that OData can't handle (e.g., "give me P&L with department breakdown already calculated")

**When to use over OData:** When you need pre-computed reports (P&L, ФОТ by department) rather than raw documents. OData gives you individual transactions; HTTP services can give you aggregated reports.

### C. SOAP Web Services (1С: Веб-сервисы)

- Older than HTTP services, available since 8.2
- WSDL-based, XML-heavy
- Still works but HTTP services are strictly better for new integrations
- Skip this.

### D. COM/Automation Connection (External Connection)

- Windows-only (requires COM infrastructure)
- Runs in-process — fast but tightly coupled
- Used for 1C-to-1C data exchange primarily
- **Not suitable for remote/cloud integration** — requires running on the same Windows machine as 1C
- Skip this for your use case.

### E. File-Based Exchange (XML/CSV/Excel)

- 1C can export to Excel, CSV, XML natively
- Can be automated via scheduled tasks inside 1C ("Рассылка отчётов")
- Configure in: НСИ и Администрирование > Печатные формы, отчеты и обработки > Рассылки отчетов
- Set "Выполнять по расписанию" + target folder (local, network share, or FTP)
- `extract_1c.py` already handles this — parses Excel/CSV exports

**This is the fallback.** If OData setup proves difficult, Natalia can configure scheduled Excel exports from each 1C instance to a shared folder, and `extract_1c.py` processes them.

---

## 2. OData Deep Dive — What You Need for Kamarooms

### Endpoint Names (Cyrillic — this is standard)

Your `pull_1c.py` already maps these correctly:

| Data | OData Entity | 1C Object |
|------|-------------|-----------|
| Revenue | `Document_РеализацияТоваровУслуг` | Sales documents |
| Purchases | `Document_ПоступлениеТоваровУслуг` | Purchase receipts |
| Payments out | `Document_ПлатежноеПоручение` | Payment orders |
| Payments in | `Document_ПоступлениеНаРасчетныйСчет` | Bank receipts |
| Counterparties | `Catalog_Контрагенты` | Customer/vendor directory |
| Chart of accounts | `ChartOfAccounts_Хозрасчетный` | Account chart |
| Employees | `Catalog_Сотрудники` | Staff directory |

### Missing Endpoints You Probably Need

| Data | OData Entity | Why |
|------|-------------|-----|
| Payroll | `Document_НачислениеЗарплаты` | ФОТ breakdown |
| Cost items | `Catalog_СтатьиЗатрат` | Expense categorization |
| Departments | `Catalog_Подразделения` | P&L by department |
| Account balances | `AccumulationRegister_ВзаиморасчетыСПоставщиками` | A/R and A/P |
| Cash register | `Document_ПриходныйКассовыйОрдер` | Cash receipts |

**Important:** The exact entity names depend on which 1C configuration is installed (1C:Бухгалтерия 3.0, 1C:Hotel, etc.). Dmitry needs to look at the OData metadata endpoint (`$metadata`) to get the real list.

### Discovering Available Entities

Once OData is published, hit:
```
GET http://<server>:<port>/<database>/odata/standard.odata/$metadata
```
This returns an XML document listing every available entity, its fields, and types. This is the first thing to do after setup.

### Filtering

OData v3 filter syntax:
```
$filter=Date ge datetime'2026-01-01T00:00:00' and Date lt datetime'2026-02-01T00:00:00'
$orderby=Date desc
$top=100
$select=Date,СуммаДокумента,Комментарий
```

### Authentication

- **Default:** HTTP Basic Auth using 1C user credentials
- The 1C user needs "External connection" rights enabled
- If published on IIS: can also use Windows/NTLM authentication
- **No token-based auth out of the box** — Basic Auth over HTTPS is the standard approach
- Create a dedicated 1C user (e.g., `api_user`) with read-only access to needed data
- Right checks happen server-side — the user only sees what their 1C role allows

---

## 3. Setup Steps for Dmitry

### Prerequisites

1. **Web server** on the 1C machine: Apache 2.4 (Linux) or IIS (Windows). Most Russian 1C installations run on Windows Server.
2. **1C web extension module** installed (selected during 1C platform installation as "Модули расширения веб-сервера")
3. **Tailscale** on the 1C server for secure remote access (already planned)

### Step-by-Step

For EACH of the 3 databases (Hotel, Бухгалтерия, SPA):

1. **Open 1C Designer** for that database
2. **Administration > Publish to Web Server**
3. Set publication name (Latin characters only, e.g., `KamaroomsHotel`, `KamaroomsBuh`, `KamaroomsSPA`)
4. Check **"Publish standard OData interface"** (Публиковать стандартный интерфейс OData)
5. Specify the web directory (e.g., `C:\inetpub\wwwroot\KamaroomsHotel`)
6. Click Publish, confirm web server restart

### Create API User

In each database:
1. Administration > Users
2. Create user `api_reader` with a strong password
3. Assign role with read-only access to needed objects
4. Enable "External connection" flag

### Test

```bash
curl -u api_reader:PASSWORD "http://localhost:8080/KamaroomsHotel/odata/standard.odata/$metadata"
```

If this returns XML — OData is working.

### Connect via Tailscale

Once Tailscale is running on both the 1C server and Ed's server:
```bash
curl -u api_reader:PASSWORD "http://100.x.x.x:8080/KamaroomsHotel/odata/standard.odata/Catalog_Контрагенты?$format=json&$top=5"
```

---

## 4. Python/Node.js Client Options

### Python (what you're already using)

| Library | Notes |
|---------|-------|
| `requests` (stdlib-adjacent) | What `pull_1c.py` uses. Direct HTTP. Simple and sufficient. |
| [belov38/1c-odata](https://github.com/belov38/1c-odata) | 1C-specific OData v3 wrapper. Handles Cyrillic entity names, auth, pagination. Worth evaluating. |
| [SAP/pyodata](https://github.com/SAP/python-pyodata) | Enterprise OData client. More mature but OData v2 focused. May have v3 quirks. |
| [OData/odatapy-client](https://github.com/OData/odatapy-client) | Official OData Python client. OData v4 focused — may not work with 1C's v3. |

**Recommendation:** Stick with raw `requests` (current approach). 1C's OData is simple enough that a wrapper adds complexity without much benefit. The 1C-specific wrapper (belov38/1c-odata) is worth a look if you hit pagination or encoding issues.

### Node.js

No 1C-specific Node.js libraries exist. Use `axios` or `node-fetch` with Basic Auth. Same HTTP approach as Python.

---

## 5. File-Based Integration (Fallback Path)

If OData setup is blocked (e.g., no web server, no Dmitry bandwidth), the fallback is already built:

### What 1C Supports

| Format | Quality | Notes |
|--------|---------|-------|
| Excel (XLSX) | Best | Native 1C export. Structured headers. `extract_1c.py` handles this. |
| CSV | Good | Encoding can be tricky (Windows-1251 vs UTF-8). |
| XML | Verbose | Native format for 1C data exchange. Overkill for reports. |
| PDF | Worst | Only for human reading. Avoid. |

### Automating Exports Inside 1C

1C can schedule automatic report exports:
1. Go to НСИ и Администрирование > Печатные формы, отчеты и обработки > Рассылки отчетов
2. Select the report to export
3. Set format (Excel)
4. Set schedule (e.g., daily at 06:00)
5. Set destination: network folder, FTP, or email

Then `pull_1c.py --fallback` picks up the files from Google Drive (via rclone), or from a local/network path.

### Effort Comparison

| Path | Setup Time | Maintenance | Data Freshness |
|------|-----------|-------------|----------------|
| OData API | 2-4 hours (Dmitry) | Low — set and forget | Real-time |
| Scheduled Excel exports | 30 min (Natalia) | Medium — breaks when 1C updates | Daily |
| Manual Excel exports | 5 min (Natalia) | High — human in the loop | On request |

---

## 6. 1C:Fresh (Cloud) vs On-Premise

Kamarooms runs on-premise (local server). But worth knowing the differences:

| Aspect | On-Premise | 1C:Fresh (Cloud) |
|--------|-----------|------------------|
| OData | Must publish manually (Designer) | Published automatically by default |
| HTTP Services | Full control, any customization | Limited — extensions only, by agreement with 1C |
| COM Connection | Available (Windows) | Not available |
| Web Server | You manage (IIS/Apache) | 1C manages |
| Updates | Manual | Automatic |
| Custom Code | Full access to configuration | Extensions only |
| Network Access | Direct (Tailscale/VPN) | Via 1C's cloud infrastructure |

**For Kamarooms:** On-premise is actually better for integration — you have full control over OData publication and can put Tailscale directly on the server.

---

## 7. 1C:Hotel Specifically

### What 1C:Hotel Is

1C:Отель is a PMS built on the 1C:Enterprise 8.3 platform. It handles:
- Room inventory and reservations
- Guest check-in/check-out
- Billing and folios
- Integration with electronic locks, passport scanners, channel managers
- Data exchange with 1C:Бухгалтерия, 1C:ERP, 1C:Restaurant

### Integration Points

1. **Standard OData** — same as any 1C application. All catalogs and documents accessible.
2. **REST API** — starting from version 9.1.2.69, 1C:Hotel supports REST API for lock system integration (HSU protocol). This is device-focused, not financial-data-focused.
3. **Built-in exchange with 1C:Бухгалтерия** — invoices and payments automatically sync between Hotel and Accounting. This means the Бухгалтерия instance may already contain all hotel financial data.
4. **TravelLine integration** — 1C:Hotel has a native connector to TravelLine (Kamarooms uses TravelLine as channel manager).

### What This Means for Your Integration

**You may not need to pull from 1C:Hotel directly.** If 1C:Hotel syncs its financials to 1C:Бухгалтерия (which is standard), then pulling from Бухгалтерия gives you everything. Hotel-specific data (occupancy, guest count, room status) is better sourced from PMS/TravelLine anyway.

Ask Dmitry: "Does 1C:Hotel exchange data with 1C:Бухгалтерия? What's the sync frequency?"

---

## 8. Integration Middleware Options

| Platform | 1C Support | Cost | Notes |
|----------|-----------|------|-------|
| **Albato** | Yes — 1C:Бухгалтерия, 1C:УНФ connectors | ~2,000 RUB/mo | Russian-made, no-code. Good for simple CRM/1C sync. Not ideal for complex financial data. |
| **APIX-Drive** | Limited 1C support | ~1,500 RUB/mo | More basic than Albato. |
| **n8n** (self-hosted) | No native 1C node | Free (self-hosted) | Would use HTTP Request node to hit OData. You'd basically be rewriting `pull_1c.py` in n8n. Already planned in your architecture. |
| **Make/Zapier** | No 1C connectors | N/A | Not relevant. |

**Recommendation:** Skip middleware for the 1C integration. `pull_1c.py` + systemd timer is simpler, more debuggable, and already built. Use n8n for orchestration later (e.g., "run pull_1c.py, then update dashboard, then post to Discord if anomaly detected").

---

## 9. Security Considerations

### Authentication
- HTTP Basic Auth over HTTPS (standard approach)
- Create dedicated `api_reader` user per database with read-only role
- Never use admin credentials for API access
- HTTPS is critical — Basic Auth sends credentials in base64 (not encrypted without TLS)

### Network
- Tailscale provides encrypted mesh networking (WireGuard-based) — solves the "no public IP" problem
- 1C server should NOT be exposed to public internet
- Tailscale ACLs can restrict which devices can reach the 1C port

### 1C-Side
- OData respects 1C's role-based access — the api_reader user should only have read access
- All data access goes through standard 1C permission checks
- No need for separate API keys or tokens — 1C handles auth through its user system

---

## 10. Recommended Integration Path

### Phase 0: Manual (CURRENT — working now)
- Natalia exports Excel from 1C
- Ed runs `extract_1c.py` manually
- Status: Data request sent (`1c-data-request.md`), waiting for Chelny visit

### Phase 1: Automated File Exchange (LOW EFFORT)
- Natalia configures scheduled Excel exports from each 1C instance
- Files land on a shared folder or Google Drive
- `pull_1c.py --fallback` picks them up via rclone
- Effort: 30 min for Natalia, 0 for Dmitry
- Data freshness: Daily

### Phase 2: OData API (TARGET — discuss with Dmitry)
- Dmitry publishes OData on each 1C instance
- Installs Tailscale on 1C server
- Creates api_reader user
- `pull_1c.py` pulls directly via OData
- Effort: 2-4 hours for Dmitry
- Data freshness: Real-time (pulled daily by timer, but can go on-demand)

### Phase 3: Custom HTTP Services (FUTURE — if needed)
- If OData doesn't give you the aggregated reports you need (P&L by department, ФОТ breakdown)
- Dmitry or a 1C developer writes custom HTTP endpoints in 1C
- Returns pre-calculated JSON (instead of you computing from raw documents)
- Only worth doing if Phase 2 OData requires too much client-side aggregation

---

## Questions for Dmitry

1. Which web server is on the 1C machine — IIS or Apache? Or neither (needs installation)?
2. Are the 1C web extension modules ("Модули расширения веб-сервера") installed?
3. Does 1C:Hotel sync financial data to 1C:Бухгалтерия? How often?
4. What 1C platform version is installed? (Need 8.3.5+ for OData, 8.3.9+ for HTTP services)
5. Can we install Tailscale on the 1C server? Who manages that server?
6. Are there any existing external integrations that use OData or web services? (e.g., TravelLine, Bitrix)
7. What's the 1C:Hotel version? (Need 9.1.2.69+ for native REST API)
8. Is there a test/dev copy of any of the 3 databases we can experiment with safely?

---

## Sources

- [1C REST Interface Documentation](https://1c-dn.com/1c_enterprise/rest_interface/)
- [Publishing OData for 1C Infobase](https://kb.1ci.com/1C_Enterprise_Platform/FAQ/Development/Integration/Publishing_standard_REST_API_for_your_infobase/)
- [1C OData Integration Methods](https://1c-dn.com/blog/methods-of-integration-with-1c-enterprise-applications/)
- [1C:Enterprise OData on odata.org](https://www.odata.org/ecosystem/producers/1C-Enterprise-built-in-odata-service/)
- [HTTP Services in 1C (Russian)](https://1c-programmer-blog.ru/programmirovanie/http-servisy-v-1s.html)
- [1C HTTP Service Tutorial (Russian)](https://infostart.ru/1c/articles/1293341/)
- [1C External Connection/COM (Russian)](https://v8.1c.ru/platforma/vneshnee-soedinenie/)
- [1C:Hotel Features](https://solutions.1c.ru/catalog/hotel/features)
- [1C:Hotel REST API (HSU)](https://hsu.systems/news/1c-hotel/)
- [1C:Fresh OData Integration](https://1cfresh.com/articles/data_odata)
- [1C OData Protocol Tutorial (Russian)](https://infostart.ru/1c/articles/1570140/)
- [1C Scheduled Report Export (Russian)](https://www.koderline.ru/expert/instruktsii/article-rassylka-otchetov-v-1s-kompleksnaya-avtomatizatsiya-2-4/)
- [belov38/1c-odata Python wrapper](https://github.com/belov38/1c-odata)
- [SAP/python-pyodata](https://github.com/SAP/python-pyodata)
- [Albato 1C Integration (Russian)](https://albato.ru/apps-accounts)
- [1C Web Server Publishing (Russian)](https://efsol.ru/manuals/web-1c/)
