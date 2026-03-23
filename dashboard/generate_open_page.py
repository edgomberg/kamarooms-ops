#!/usr/bin/env python3
"""
Kamarooms /Open Page Generator

Generates a multi-page static HTML site from scorecard.json data
using Jinja2 templates. Russian-first. Buffer-style transparency.

Usage:
    python generate_open_page.py                    # generates to dist/
    python generate_open_page.py --output /path/    # custom output directory
"""

import json
import os
import shutil
import sys
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARCH_DIR = os.path.join(SCRIPT_DIR, "..", "architecture")
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "templates")
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "dist")

MONTH_NAMES_RU = {
    "01": "январь", "02": "февраль", "03": "март", "04": "апрель",
    "05": "май", "06": "июнь", "07": "июль", "08": "август",
    "09": "сентябрь", "10": "октябрь", "11": "ноябрь", "12": "декабрь",
}

MONTH_LABELS_RU = {
    "01": "Янв", "02": "Фев", "03": "Мар", "04": "Апр",
    "05": "Май", "06": "Июн", "07": "Июл", "08": "Авг",
    "09": "Сен", "10": "Окт", "11": "Ноя", "12": "Дек",
}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def fmt_rub(value):
    """Format as Russian rubles with space thousands separator."""
    if value is None:
        return "—"
    return f"{value:,.0f}".replace(",", " ") + " ₽"


def prepare_data(scorecard):
    """Extract and compute all data needed by templates."""
    data_year = max(scorecard["historical_monthly"].keys())
    monthly = scorecard["historical_monthly"][data_year]
    annual = scorecard["historical_annual"]
    months_sorted = sorted(monthly.keys())

    # Chart data arrays
    labels_ru = [MONTH_LABELS_RU[m] for m in months_sorted]
    occupancy_data = [monthly[m]["occupancy"] for m in months_sorted]
    revpar_data = [monthly[m]["revpar"] for m in months_sorted]
    adr_data = [monthly[m]["adr"] for m in months_sorted]
    revenue_data = [round(monthly[m]["revenue"] / 1_000_000, 1) for m in months_sorted]

    # Averages
    avg_occupancy = round(
        sum(monthly[m]["occupancy"] for m in months_sorted) / len(months_sorted), 1
    )
    avg_adr = round(
        sum(monthly[m]["adr"] for m in months_sorted) / len(months_sorted), 0
    )
    avg_revpar = round(
        sum(monthly[m]["revpar"] for m in months_sorted) / len(months_sorted), 0
    )

    # Latest month + MoM changes
    latest_month = months_sorted[-1]
    latest = monthly[latest_month]
    if len(months_sorted) >= 2:
        prev = monthly[months_sorted[-2]]
        revpar_change = round(
            (latest["revpar"] - prev["revpar"]) / prev["revpar"] * 100, 1
        ) if prev["revpar"] else 0
        occ_change = round(latest["occupancy"] - prev["occupancy"], 1)
        adr_change = round(
            (latest["adr"] - prev["adr"]) / prev["adr"] * 100, 1
        ) if prev["adr"] else 0
    else:
        revpar_change = occ_change = adr_change = 0

    # Historical annual data
    hist_years = [str(h["year"]) for h in annual]
    hist_margins = [h["margin"] for h in annual]
    hist_revenue = [round(h["revenue"] / 1_000_000, 1) for h in annual]

    # Ratings — lookup by ID, not positional index
    ratings = next(
        kpi["current"] for kpi in scorecard["core_kpis"] if kpi["id"] == "guest_rating"
    )

    # Data freshness
    data_month_ru = MONTH_NAMES_RU.get(latest_month, latest_month)

    # Fun facts (placeholder data for launch)
    fun_facts = [
        {
            "emoji": "🛏️",
            "value": "Люкс Бизнес",
            "label": "Самый популярный тип номера",
            "context": "42% бронирований",
        },
        {
            "emoji": "🥐",
            "value": "Блины",
            "label": "Самый заказываемый завтрак",
            "context": "Каждое утро. Без исключений.",
        },
        {
            "emoji": "📦",
            "value": "—",
            "label": "Забытых вещей вернули",
            "context": "Считаем с апреля 2026",
        },
        {
            "emoji": "⏰",
            "value": "6:00",
            "label": "Самый ранний чекин",
            "context": "Потому что почему бы и нет",
        },
        {
            "emoji": "🧹",
            "value": "~2 км",
            "label": "Коридоров убираем ежедневно",
            "context": "5 этажей, 108 номеров",
        },
        {
            "emoji": "🛋️",
            "value": "—",
            "label": "Подушек взбито в этом месяце",
            "context": "Считаем с апреля 2026",
        },
    ]

    # Monthly updates (placeholder for launch)
    updates = []

    return {
        # Global
        "data_year": data_year,
        "data_month_ru": data_month_ru,
        "months_count": len(months_sorted),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        # Ratings
        "ratings": ratings,
        # WiFi (hardcoded for launch)
        "wifi_speed": "120",
        # Averages
        "occupancy_avg": avg_occupancy,
        "adr_avg": fmt_rub(avg_adr),
        "revpar_avg": fmt_rub(avg_revpar),
        "avg_revpar": avg_revpar,
        # Latest month
        "latest_occupancy": latest["occupancy"],
        "latest_revpar": fmt_rub(latest["revpar"]),
        "latest_adr": fmt_rub(latest["adr"]),
        "occ_change": occ_change,
        "revpar_change": revpar_change,
        "adr_change": adr_change,
        # Chart data (JSON-safe)
        "labels_ru": labels_ru,
        "occupancy_data": occupancy_data,
        "revpar_data": revpar_data,
        "adr_data": adr_data,
        "revenue_data": revenue_data,
        # Historical
        "hist_years": hist_years,
        "hist_margins": hist_margins,
        "hist_revenue": hist_revenue,
        # Fun facts
        "fun_facts": fun_facts,
        # Updates
        "updates": updates,
        # Formula definitions (for performance page)
        "formulas": {
            "revpar": "RevPAR = Выручка номерного фонда ÷ Доступные номеро-ночи",
            "adr": "ADR = Выручка номерного фонда ÷ Проданные номеро-ночи",
            "occupancy": "Загрузка = Проданные номеро-ночи ÷ Доступные номеро-ночи × 100%",
        },
    }


def generate(output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT

    os.makedirs(output_dir, exist_ok=True)

    # Load data
    scorecard = load_json(os.path.join(ARCH_DIR, "scorecard.json"))
    data = prepare_data(scorecard)

    # Set up Jinja2
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
    )

    # Pages to generate: (template_name, output_filename, active_page)
    pages = [
        ("hub.html", "index.html", "hub"),
        ("story.html", "story.html", "story"),
        ("performance.html", "performance.html", "performance"),
        ("guests.html", "guests.html", "guests"),
        ("team.html", "team.html", "team"),
        ("pulse.html", "pulse.html", "pulse"),
        ("updates.html", "updates.html", "updates"),
        ("handbook.html", "handbook.html", "handbook"),
    ]

    # Copy static assets
    assets_src = os.path.join(TEMPLATE_DIR, "assets")
    assets_dst = os.path.join(output_dir, "assets")
    if os.path.isdir(assets_src):
        if os.path.isdir(assets_dst):
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
        print(f"  ✓ assets/")

    generated = []
    for template_name, output_name, active_page in pages:
        template = env.get_template(template_name)
        html = template.render(active_page=active_page, **data)

        output_path = os.path.join(output_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        generated.append(output_path)
        print(f"  ✓ {output_name}")

    print(f"\n{len(generated)} pages generated in {output_dir}/")

    # Generate sitemap.xml
    sitemap_pages = ["", "story.html", "performance.html", "guests.html", "team.html", "pulse.html", "updates.html", "handbook.html"]
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in sitemap_pages:
        sitemap_xml += f'  <url><loc>https://open.kamarooms.com/{page}</loc></url>\n'
    sitemap_xml += '</urlset>'
    with open(os.path.join(output_dir, "sitemap.xml"), "w") as f:
        f.write(sitemap_xml)

    # Generate robots.txt
    robots_txt = "User-agent: *\nAllow: /\nSitemap: https://open.kamarooms.com/sitemap.xml\n"
    with open(os.path.join(output_dir, "robots.txt"), "w") as f:
        f.write(robots_txt)

    return generated


if __name__ == "__main__":
    output = None
    if len(sys.argv) > 2 and sys.argv[1] == "--output":
        output = sys.argv[2]

    generate(output)
