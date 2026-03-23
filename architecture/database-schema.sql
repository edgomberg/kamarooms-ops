-- Kamarooms Analytical Database Schema
-- Target: PostgreSQL on Yandex Cloud
-- Purpose: Single source of truth for all KPIs

-- ============================================================
-- CORE TABLES
-- ============================================================

CREATE TABLE daily_performance (
    date            DATE PRIMARY KEY,
    rooms_available INTEGER NOT NULL DEFAULT 108,
    rooms_sold      INTEGER NOT NULL,
    revenue         NUMERIC(12,2) NOT NULL,
    adr             NUMERIC(10,2) GENERATED ALWAYS AS (
                        CASE WHEN rooms_sold > 0 THEN revenue / rooms_sold ELSE 0 END
                    ) STORED,
    revpar          NUMERIC(10,2) GENERATED ALWAYS AS (
                        CASE WHEN rooms_available > 0 THEN revenue / rooms_available ELSE 0 END
                    ) STORED,
    occupancy_pct   NUMERIC(5,2) GENERATED ALWAYS AS (
                        CASE WHEN rooms_available > 0 THEN (rooms_sold::NUMERIC / rooms_available) * 100 ELSE 0 END
                    ) STORED,
    source          VARCHAR(50) DEFAULT 'pms_export',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE monthly_financials (
    year_month      VARCHAR(7) PRIMARY KEY,  -- '2025-01'
    revenue         NUMERIC(14,2) NOT NULL,
    opex            NUMERIC(14,2) NOT NULL,
    ebitda          NUMERIC(14,2) GENERATED ALWAYS AS (revenue - opex) STORED,
    margin_pct      NUMERIC(5,2) GENERATED ALWAYS AS (
                        CASE WHEN revenue > 0 THEN ((revenue - opex) / revenue) * 100 ELSE 0 END
                    ) STORED,
    capex           NUMERIC(14,2) DEFAULT 0,
    net_owner_profit NUMERIC(14,2),
    payroll         NUMERIC(14,2),        -- ФОТ
    utilities       NUMERIC(14,2),        -- Коммунальные
    headcount       INTEGER DEFAULT 125,
    source          VARCHAR(50) DEFAULT '1c_export',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE booking_channels (
    year_month      VARCHAR(7) NOT NULL,
    channel         VARCHAR(100) NOT NULL, -- 'booking_com', 'ostrovok', 'direct', etc.
    bookings_count  INTEGER,
    revenue         NUMERIC(14,2),
    commission      NUMERIC(14,2),
    commission_pct  NUMERIC(5,2),
    PRIMARY KEY (year_month, channel)
);

CREATE TABLE guest_ratings (
    date            DATE NOT NULL,
    platform        VARCHAR(50) NOT NULL,  -- 'booking_com', 'yandex', '2gis'
    rating          NUMERIC(3,1) NOT NULL,
    review_count    INTEGER,
    snapshot_type   VARCHAR(20) DEFAULT 'monthly', -- 'daily' or 'monthly'
    PRIMARY KEY (date, platform)
);

-- ============================================================
-- OPERATIONAL TABLES
-- ============================================================

CREATE TABLE department_costs (
    year_month      VARCHAR(7) NOT NULL,
    department      VARCHAR(100) NOT NULL, -- 'rooms', 'restaurant', 'spa', 'admin', 'maintenance'
    cost            NUMERIC(14,2) NOT NULL,
    cost_type       VARCHAR(50),           -- 'payroll', 'supplies', 'utilities', 'other'
    PRIMARY KEY (year_month, department, cost_type)
);

CREATE TABLE competitor_rates (
    date            DATE NOT NULL,
    competitor      VARCHAR(200) NOT NULL,
    platform        VARCHAR(50) NOT NULL,  -- 'booking_com', 'ostrovok'
    room_type       VARCHAR(100),
    rate            NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (date, competitor, platform, room_type)
);

CREATE TABLE ai_operations_log (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMPTZ DEFAULT NOW(),
    agent_type      VARCHAR(50) NOT NULL,  -- 'revenue', 'guest_comms', 'ops'
    action          TEXT NOT NULL,
    details         JSONB,
    impact_metric   VARCHAR(50),           -- which KPI affected
    impact_value    NUMERIC(12,2),
    human_approved  BOOLEAN DEFAULT FALSE,
    public_summary  TEXT                   -- sanitized version for public dashboard
);

-- ============================================================
-- VIEWS
-- ============================================================

CREATE VIEW v_monthly_kpis AS
SELECT
    mf.year_month,
    mf.revenue,
    mf.opex,
    mf.ebitda,
    mf.margin_pct,
    mf.capex,
    mf.payroll,
    CASE WHEN mf.revenue > 0 THEN (mf.payroll / mf.revenue) * 100 END AS labor_cost_pct,
    CASE WHEN mf.revenue > 0 AND mf.headcount > 0 THEN mf.revenue / mf.headcount END AS revenue_per_employee,
    CASE WHEN mf.utilities > 0 THEN mf.utilities / 108 END AS energy_cost_per_room,
    dp.avg_occupancy,
    dp.avg_adr,
    dp.avg_revpar,
    CASE WHEN dp.avg_occupancy > 0 THEN mf.ebitda / (108 * 30) END AS goppar
FROM monthly_financials mf
LEFT JOIN (
    SELECT
        TO_CHAR(date, 'YYYY-MM') AS year_month,
        AVG(occupancy_pct) AS avg_occupancy,
        AVG(adr) AS avg_adr,
        AVG(revpar) AS avg_revpar
    FROM daily_performance
    GROUP BY TO_CHAR(date, 'YYYY-MM')
) dp ON dp.year_month = mf.year_month;

CREATE VIEW v_channel_mix AS
SELECT
    year_month,
    channel,
    bookings_count,
    revenue,
    commission,
    commission_pct,
    CASE WHEN SUM(bookings_count) OVER (PARTITION BY year_month) > 0
         THEN (bookings_count::NUMERIC / SUM(bookings_count) OVER (PARTITION BY year_month)) * 100
    END AS channel_share_pct
FROM booking_channels;

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_daily_perf_month ON daily_performance (DATE_TRUNC('month', date));
CREATE INDEX idx_ai_ops_agent ON ai_operations_log (agent_type, timestamp);
CREATE INDEX idx_competitor_date ON competitor_rates (date);
CREATE INDEX idx_ratings_platform ON guest_ratings (platform, date);

-- ============================================================
-- SEED DATA (from s1-hotel-financials-extracted.md)
-- ============================================================

INSERT INTO monthly_financials (year_month, revenue, opex, capex, net_owner_profit) VALUES
('2025-01', 11900000, 10000000, 3200000, -1400000),
('2025-02', 14400000, 10400000, 100000, 3900000),
('2025-03', 15900000, 13100000, 500000, 2300000),
('2025-04', 13300000, 12000000, 1200000, 100000),
('2025-05', 13900000, 11200000, 4000000, -1400000),
('2025-06', 16000000, 13600000, 700000, 1700000),
('2025-07', 16800000, 13400000, 900000, 2400000),
('2025-08', 17600000, 13400000, 200000, 4000000),
('2025-09', 18300000, 13400000, 50000, 4900000),
('2025-10', 18500000, 13300000, 0, 5200000),
('2025-11', 16100000, 12600000, 0, 3500000);

INSERT INTO guest_ratings (date, platform, rating, review_count) VALUES
('2026-03-01', 'booking_com', 9.4, NULL),
('2026-03-01', 'yandex', 5.0, NULL),
('2026-03-01', '2gis', 4.8, 392);
