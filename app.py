import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sql_queries import run, summary, core_queries, advanced_queries

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Expense Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #fdf6ff 50%, #f0fbff 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8f0ff 100%);
    border-right: 1px solid #e8e0f0;
}
section[data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif; }

/* KPI Cards */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 24px 20px;
    box-shadow: 0 4px 24px rgba(120, 80, 200, 0.07);
    border: 1px solid rgba(200, 180, 255, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 12px;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(120, 80, 200, 0.13);
}
.kpi-label {
    font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: #9b8ab0; margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Playfair Display', serif; font-size: 28px;
    font-weight: 700; color: #2d1b69; margin: 0;
}
.kpi-icon { font-size: 28px; margin-bottom: 10px; }

/* Colourful Stat Cards */
.stat-card {
    border-radius: 16px;
    padding: 22px 20px;
    margin-bottom: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; opacity: 0.75; margin-bottom: 4px;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 26px; font-weight: 700; margin: 0;
}
.stat-sub { font-size: 12px; opacity: 0.65; margin-top: 4px; }

/* Insight Box */
.insight-box {
    background: linear-gradient(135deg, #f8f5ff 0%, #f0fbff 100%);
    border-left: 4px solid #7c5cbf;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    font-size: 13px; color: #4a3b6e;
    line-height: 1.7; margin-top: 8px;
}

/* Analysis Block */
.analysis-block {
    background: white; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 4px 24px rgba(100, 80, 180, 0.07);
    border: 1px solid rgba(200, 190, 240, 0.2);
    line-height: 1.9; color: #3a2d55; font-size: 15px;
}
.analysis-block h3 {
    font-family: 'Playfair Display', serif; color: #2d1b69;
    font-size: 20px; margin-bottom: 14px;
}
.highlight {
    background: linear-gradient(90deg, #e8d5ff, #d5eeff);
    border-radius: 6px; padding: 2px 8px;
    font-weight: 600; color: #2d1b69;
}

.page-header { padding: 10px 0 4px 0; margin-bottom: 28px; }
.page-header h1 {
    font-family: 'Playfair Display', serif; font-size: 32px;
    font-weight: 700; color: #2d1b69; margin: 0;
}
.page-header p { color: #9b8ab0; font-size: 14px; margin: 4px 0 0 0; }

.footer {
    text-align: center; color: #b0a0c8; font-size: 12px;
    padding: 32px 0 16px 0; border-top: 1px solid #ede8f8; margin-top: 40px;
}

div[data-testid="stMetric"] {
    background: white; border-radius: 12px; padding: 16px;
    border: 1px solid rgba(200, 180, 255, 0.2);
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #7c5cbf, #5ba8d4);
    color: white; border: none; border-radius: 8px;
    font-size: 12px; padding: 6px 16px; font-family: 'DM Sans', sans-serif;
}
.stDownloadButton > button:hover { opacity: 0.88; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
PASTEL_COLORS = [
    "#7c5cbf", "#5ba8d4", "#e88fc7", "#5dcfb0",
    "#f0a070", "#a0c878", "#9b6ec8", "#60b8c8",
    "#d478a0", "#78c8a0", "#f0b060", "#7888d4",
]

CARD_THEMES = [
    {"bg": "linear-gradient(135deg,#ede0ff,#d5eeff)", "color": "#2d1b69"},
    {"bg": "linear-gradient(135deg,#d5f5ec,#a8edea)", "color": "#1a4d3a"},
    {"bg": "linear-gradient(135deg,#ffecd2,#ffb347aa)", "color": "#7a3010"},
    {"bg": "linear-gradient(135deg,#ffd6e7,#ffb3c1)", "color": "#7a1035"},
    {"bg": "linear-gradient(135deg,#d0f0fd,#a8edea)", "color": "#0a4a5e"},
    {"bg": "linear-gradient(135deg,#e0ffe0,#b7f0b7)", "color": "#1a4d1a"},
]

MONTH_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
             7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
QUARTER_MAP = {1:"Q1",2:"Q2",3:"Q3",4:"Q4"}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#3a2d55"),
    margin=dict(t=36, b=30, l=20, r=20),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", borderwidth=0),
)

LABEL_MAP = {
    "total_spent": "Total Spent (₹)", "amount_paid": "Amount Paid (₹)",
    "total_cashback": "Cashback Earned (₹)", "avg_spent": "Avg Spent (₹)",
    "daily_avg": "Daily Avg Spend (₹)", "max_spent": "Max Spend (₹)",
    "min_spent": "Min Spend (₹)", "total_transactions": "No. of Transactions",
    "total_no_cashback": "Transactions Without Cashback",
    "frequency": "No. of Transactions", "total": "Transaction Count",
    "cashback_percent": "Cashback Rate (%)",
    "cashback_efficiency_percent": "Cashback Efficiency (%)",
    "high_value_percent": "High-Value Transactions (%)",
    "percentage": "Share of Total Spend (%)",
    "avg_weekend": "Avg Weekend Spend (₹)",
    "avg_weekday": "Avg Weekday Spend (₹)",
    "range_start": "Spend Range (₹)",
    "day_type": "Day Type", "payment_mode": "Payment Mode",
    "category": "Category", "year": "Year",
    "Month": "Month", "Quarter": "Quarter",
    "cashback": "Cashback (₹)", "id": "Transaction ID",
    "date": "Date",
}

# Queries that return full transaction rows → render as table
TABLE_QUERIES = {
    "cashback transactions",
    "above average transactions",
    "highest cashback transaction",
}


def friendly(col):
    return LABEL_MAP.get(col, col.replace("_", " ").title())


# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────
def styled_bar(df, x, y, title=""):
    str_cols = df.select_dtypes("object").columns.tolist()
    color_col = str_cols[0] if str_cols else x
    fig = px.bar(df, x=x, y=y, title=title,
                 color=color_col,
                 color_discrete_sequence=PASTEL_COLORS,
                 template="plotly_white")
    fig.update_layout(**PLOTLY_LAYOUT,
                      xaxis_title=friendly(x),
                      yaxis_title=friendly(y))
    fig.update_traces(marker_line_width=0, opacity=0.88)
    return fig


def styled_pie(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=PASTEL_COLORS,
                 template="plotly_white", hole=0.38)
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def styled_line(df, x, y, title=""):
    fig = px.line(df, x=x, y=y, title=title,
                  color_discrete_sequence=PASTEL_COLORS,
                  template="plotly_white", markers=True)
    fig.update_layout(**PLOTLY_LAYOUT,
                      xaxis_title=friendly(x),
                      yaxis_title=friendly(y))
    fig.update_traces(line_width=2.5, marker_size=7)
    return fig


def download_btn(df, label="Download CSV", filename="data.csv"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label=f"⬇ {label}", data=csv,
                       file_name=filename, mime="text/csv")


# ─────────────────────────────────────────────
# COLOURFUL STAT CARD HELPER
# ─────────────────────────────────────────────
def stat_card(label, value, sub="", theme_idx=0):
    t = CARD_THEMES[theme_idx % len(CARD_THEMES)]
    sub_html = f"<div class='stat-sub'>{sub}</div>" if sub else ""
    st.markdown(f"""
    <div class='stat-card' style='background:{t["bg"]};color:{t["color"]}'>
        <div class='stat-label'>{label}</div>
        <div class='stat-value'>{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CACHED DATA LOADERS
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_summary():
    return summary()

@st.cache_data(ttl=300)
def load_core(name):
    return run(core_queries[name])

@st.cache_data(ttl=300)
def load_advanced(name):
    return run(advanced_queries[name])

@st.cache_data(ttl=300)
def load_all_expenses():
    return run("SELECT * FROM expenses")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💳 Expense Tracker")
    st.markdown("---")

    nav = st.radio(
        "Navigate",
        ["Financial Performance Overview",
         "Operational Analytics",
         "Strategic Financial Insights"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**🔍 Filters**")

    try:
        df_all = load_all_expenses()
        df_all["date"] = pd.to_datetime(df_all["date"])
        min_d = df_all["date"].min().date()
        max_d = df_all["date"].max().date()
        date_range = st.date_input("Date Range", value=(min_d, max_d),
                                   min_value=min_d, max_value=max_d)
        categories = sorted(df_all["category"].dropna().unique().tolist())
        sel_cat = st.multiselect("Category", categories, default=categories)
        pay_modes = sorted(df_all["payment_mode"].dropna().unique().tolist())
        sel_pay = st.multiselect("Payment Mode", pay_modes, default=pay_modes)
        mask = (
            (df_all["date"].dt.date >= date_range[0]) &
            (df_all["date"].dt.date <= date_range[1]) &
            (df_all["category"].isin(sel_cat)) &
            (df_all["payment_mode"].isin(sel_pay))
        )
        df_filtered = df_all[mask].copy()
    except Exception as e:
        st.error(f"Filter error: {e}")
        df_filtered = pd.DataFrame()

    st.markdown("---")
    st.caption("💡 Filters apply to Financial Performance Overview only.")


# ─────────────────────────────────────────────
# RENDER CHART — smart dispatcher
# ─────────────────────────────────────────────
def render_chart(df, title, theme_idx=0):
    if df is None or df.empty:
        st.info("No data available.")
        return

    title_lower = title.lower()
    df = df.copy()

    # ── Normalise month/quarter numbers → labels ──
    if "month" in df.columns:
        df["month"] = pd.to_numeric(df["month"], errors="coerce").map(MONTH_MAP)
        df.rename(columns={"month": "Month"}, inplace=True)
    if "quarter" in df.columns:
        df["quarter"] = pd.to_numeric(df["quarter"], errors="coerce").map(QUARTER_MAP)
        df.rename(columns={"quarter": "Quarter"}, inplace=True)
    if "year" in df.columns:
        df["year"] = df["year"].astype(int).astype(str)

    cols     = df.columns.tolist()
    num_cols = df.select_dtypes("number").columns.tolist()
    str_cols = df.select_dtypes("object").columns.tolist()

    # ══════════════════════════════════════════
    # 1. TABLE QUERIES (SELECT * multi-row)
    # ══════════════════════════════════════════
    if title_lower in TABLE_QUERIES:
        if "highest cashback transaction" in title_lower and len(df) == 1:
            row     = df.iloc[0]
            date_v  = str(row.get("date",""))[:10]
            cat_v   = row.get("category","N/A")
            amt_v   = float(row.get("amount_paid", 0))
            cb_v    = float(row.get("cashback", 0))
            pay_v   = row.get("payment_mode","N/A")
            stat_card("📅 Transaction Date", date_v, "", theme_idx % 6)
            c1, c2 = st.columns(2)
            with c1: stat_card("🏷️ Category", cat_v, "", (theme_idx+1) % 6)
            with c2: stat_card("💳 Payment Mode", pay_v, "", (theme_idx+2) % 6)
            c3, c4 = st.columns(2)
            with c3: stat_card("💰 Amount Paid", f"₹{amt_v:,.2f}", "", (theme_idx+3) % 6)
            with c4: stat_card("🎁 Cashback Earned", f"₹{cb_v:,.2f}", "Highest cashback in dataset", (theme_idx+4) % 6)
            return
        # Generic table
        display_df = df.copy()
        if "date" in display_df.columns:
            display_df["date"] = pd.to_datetime(display_df["date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        return

    # ══════════════════════════════════════════
    # 2. SPECIAL SINGLE-ROW NAMED QUERIES
    # ══════════════════════════════════════════

    # Highest / Lowest Spending Month
    if ("highest spending month" in title_lower or "lowest spending month" in title_lower) and len(df) <= 2:
        month_v = df["Month"].iloc[0] if "Month" in df.columns else "N/A"
        spent_v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        icon    = "📈" if "highest" in title_lower else "📉"
        lbl     = "Peak Spending Month" if "highest" in title_lower else "Lowest Spending Month"
        stat_card(f"{icon} {lbl}", month_v,
                  f"Total spent: ₹{spent_v:,.2f}", theme_idx % 6)
        return

    # Top Category Share (%)
    if "top category share" in title_lower and len(df) == 1:
        cat_v = df["category"].iloc[0] if "category" in df.columns else "N/A"
        pct_v = float(df["percentage"].iloc[0]) if "percentage" in df.columns else 0
        stat_card("🏆 Top Spending Category", cat_v,
                  f"Accounts for {pct_v:.2f}% of total spending", theme_idx % 6)
        return

    # Most Used Payment Mode
    if "most used payment mode" in title_lower and len(df) == 1:
        mode_v  = df["payment_mode"].iloc[0] if "payment_mode" in df.columns else "N/A"
        count_v = int(df["total"].iloc[0]) if "total" in df.columns else 0
        stat_card("💳 Most Used Payment Mode", mode_v,
                  f"Used in {count_v:,} transactions", theme_idx % 6)
        return

    # Transactions with No Cashback
    if "transactions with no cashback" in title_lower and len(df) == 1:
        col_v = "total_no_cashback" if "total_no_cashback" in df.columns else df.columns[0]
        count_v = int(df[col_v].iloc[0])
        stat_card("🚫 Transactions Without Cashback",
                  f"{count_v:,} transactions",
                  "These transactions earned no cashback reward", theme_idx % 6)
        return

    # Spending Trend by Year (likely single row — use a bar)
    if "spending trend by year" in title_lower:
        if "year" in df.columns and "total_spent" in df.columns:
            fig = styled_bar(df, "year", "total_spent", title)
            st.plotly_chart(fig, use_container_width=True)
            return

    # ══════════════════════════════════════════
    # 3. GENERIC SINGLE-VALUE SCALARS
    # ══════════════════════════════════════════
    if len(df) == 1 and len(df.columns) == 1:
        val      = df.iloc[0, 0]
        col_name = df.columns[0]
        is_pct   = any(k in col_name.lower() for k in
                       ["percent","ratio","efficiency","high_value","percentage"])
        fmt_val  = f"{float(val):.2f}%" if is_pct else f"₹{float(val):,.2f}"
        stat_card(friendly(col_name), fmt_val, "", theme_idx % 6)
        return

    # Weekend / Weekday Average (1 row, 1 numeric)
    if len(df) == 1 and len(num_cols) == 1:
        val      = df[num_cols[0]].iloc[0]
        col_name = num_cols[0]
        is_pct   = any(k in col_name.lower() for k in
                       ["percent","ratio","efficiency","high_value"])
        fmt_val  = f"{float(val):.2f}%" if is_pct else f"₹{float(val):,.2f}"
        stat_card(friendly(col_name), fmt_val, "", theme_idx % 6)
        return

    # ══════════════════════════════════════════
    # 4. CHART ROUTING
    # ══════════════════════════════════════════
    try:
        # PIE
        PIE_KEYS = ["weekday vs weekend", "total spent by payment",
                    "total spent by payment mode", "payment mode cashback",
                    "payment mode efficiency", "cashback by category"]
        if any(k in title_lower for k in PIE_KEYS):
            if str_cols and num_cols:
                fig = styled_pie(df, str_cols[0], num_cols[0], title)
                st.plotly_chart(fig, use_container_width=True)
                return

        # LINE
        LINE_KEYS = ["monthly spending", "monthly cashback", "quarterly spending",
                     "seasonal", "daily average per month"]
        if any(k in title_lower for k in LINE_KEYS):
            x_col = ("Month"   if "Month"   in df.columns else
                     "Quarter" if "Quarter" in df.columns else cols[0])
            y_col = num_cols[0] if num_cols else cols[1]
            fig = styled_line(df, x_col, y_col, title)
            st.plotly_chart(fig, use_container_width=True)
            return

        # BAR (default for everything else)
        if num_cols:
            if str_cols:
                x_col = str_cols[0]
            elif "Month" in df.columns:
                x_col = "Month"
            elif "Quarter" in df.columns:
                x_col = "Quarter"
            elif "year" in df.columns:
                x_col = "year"
            else:
                x_col = cols[0]
            y_col = num_cols[0]
            fig = styled_bar(df, x_col, y_col, title)
            st.plotly_chart(fig, use_container_width=True)
            return

    except Exception:
        pass

    st.dataframe(df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# SMART INSIGHT GENERATOR
# ─────────────────────────────────────────────
def smart_insight(df, title):
    if df is None or df.empty:
        return "No data available."

    title_lower = title.lower()
    df = df.copy()

    # Normalise month/quarter for insight text
    if "month" in df.columns:
        df["month"] = pd.to_numeric(df["month"], errors="coerce").map(MONTH_MAP)
        df.rename(columns={"month": "Month"}, inplace=True)
    if "quarter" in df.columns:
        df["quarter"] = pd.to_numeric(df["quarter"], errors="coerce").map(QUARTER_MAP)
        df.rename(columns={"quarter": "Quarter"}, inplace=True)
    if "year" in df.columns:
        df["year"] = df["year"].astype(str)

    num_cols = df.select_dtypes("number").columns.tolist()
    str_cols = df.select_dtypes("object").columns.tolist()

    # TABLE queries
    if title_lower in TABLE_QUERIES:
        if "highest cashback" in title_lower and len(df) == 1:
            cb_v = float(df.get("cashback", pd.Series([0])).iloc[0])
            return f"Highest cashback of <b>₹{cb_v:,.2f}</b> earned in a single transaction."
        return f"Showing <b>{len(df)}</b> matching transaction records."

    # Highest / Lowest Month
    if "highest spending month" in title_lower and len(df) <= 2:
        m = df["Month"].iloc[0] if "Month" in df.columns else "N/A"
        v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        return f"Spending peaked in <b>{m}</b> at <b>₹{v:,.2f}</b>."

    if "lowest spending month" in title_lower and len(df) <= 2:
        m = df["Month"].iloc[0] if "Month" in df.columns else "N/A"
        v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        return f"Spending was lowest in <b>{m}</b> at <b>₹{v:,.2f}</b>."

    # Top Category Share
    if "top category share" in title_lower and len(df) == 1:
        cat = df["category"].iloc[0] if "category" in df.columns else "N/A"
        pct = float(df["percentage"].iloc[0]) if "percentage" in df.columns else 0
        return f"<b>{cat}</b> leads with <b>{pct:.2f}%</b> of total expenditure."

    # Most Used Payment Mode
    if "most used payment mode" in title_lower and len(df) == 1:
        mode  = df["payment_mode"].iloc[0] if "payment_mode" in df.columns else "N/A"
        count = int(df["total"].iloc[0]) if "total" in df.columns else 0
        return f"<b>{mode}</b> is the most frequently used mode — <b>{count:,}</b> transactions."

    # No Cashback
    if "transactions with no cashback" in title_lower and len(df) == 1:
        v = int(df.iloc[0, 0])
        return f"<b>{v:,}</b> out of 300 transactions had no cashback benefit."

    # Spending Trend by Year
    if "spending trend by year" in title_lower:
        if "total_spent" in df.columns:
            v = float(df["total_spent"].max())
            return f"Total annual expenditure recorded: <b>₹{v:,.2f}</b>."

    if not num_cols:
        return f"Showing {len(df)} records."

    val_col   = num_cols[0]
    col_lower = val_col.lower()

    # ── Strict type detection ──
    # % columns
    is_pct = any(k in col_lower for k in
                 ["percent", "ratio", "efficiency", "high_value", "percentage"])

    # Pure count columns — ONLY exact known count column names
    is_count = col_lower in {
        "total_transactions", "total_no_cashback",
        "frequency", "total", "count"
    }

    # Money columns — anything with these keywords is ₹
    is_money = any(k in col_lower for k in
                   ["spent", "paid", "cashback", "avg", "amount",
                    "max", "min", "daily", "weekly", "weekend", "weekday"])

    def fmt(v):
        if is_pct:              return f"{float(v):.2f}%"
        if is_count:            return f"{int(v):,} transactions"
        if is_money or True:    return f"₹{float(v):,.2f}"  # default to ₹

    # Single-value
    if len(df) == 1:
        v = df[val_col].iloc[0]
        if is_pct:   return f"Overall rate: <b>{float(v):.2f}%</b>."
        if is_count: return f"Total count: <b>{int(v):,}</b> transactions."
        return f"Recorded value: <b>₹{float(v):,.2f}</b>."

    top_val = df[val_col].max()

    # Time series — report peak with correct format
    time_col = next((c for c in ["Month", "Quarter", "year"] if c in df.columns), None)
    if time_col:
        idx      = df[val_col].idxmax()
        peak_lbl = df.loc[idx, time_col]
        return f"Peak in <b>{peak_lbl}</b> with {fmt(top_val)}."

    # Category / label series
    if str_cols:
        idx       = df[val_col].idxmax()
        top_label = df.loc[idx, str_cols[0]]
        col_title = friendly(str_cols[0])
        return f"Highest {col_title}: <b>{top_label}</b> — {fmt(top_val)}."

    return f"Peak value: {fmt(top_val)}."

# ─────────────────────────────────────────────
# PAGE 1 — FINANCIAL PERFORMANCE OVERVIEW
# ─────────────────────────────────────────────
def page_summary():
    st.markdown("""
    <div class='page-header'>
        <h1>Personal Finance Performance Report</h1>
        <p>Data-driven analysis of spending behaviour, category concentration,
           and cashback effectiveness · All figures in ₹</p>
    </div>
    """, unsafe_allow_html=True)

    if df_filtered.empty:
        st.warning("No data matches the selected filters.")
        return

    total_tx    = len(df_filtered)
    total_spent = df_filtered["amount_paid"].sum()
    total_cb    = df_filtered["cashback"].sum()
    avg_tx      = df_filtered["amount_paid"].mean()

    c1, c2, c3, c4 = st.columns(4)
    kpi_cards = [
        (c1, "🧾", "Total Transactions",  f"{total_tx:,}",        "#7c5cbf"),
        (c2, "💰", "Total Expenditure",   f"₹{total_spent:,.2f}", "#5ba8d4"),
        (c3, "🎁", "Total Cashback",      f"₹{total_cb:,.2f}",    "#5dcfb0"),
        (c4, "📊", "Avg Transaction",     f"₹{avg_tx:,.2f}",      "#e88fc7"),
    ]
    for col, icon, label, value, color in kpi_cards:
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='border-top:4px solid {color}'>
                <div class='kpi-icon'>{icon}</div>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        df_month = (
            df_filtered.groupby(df_filtered["date"].dt.month)["amount_paid"]
            .sum().reset_index()
            .rename(columns={"date": "Month", "amount_paid": "Total Spent"})
        )
        df_month["Month"] = df_month["Month"].map(MONTH_MAP)
        fig = px.line(df_month, x="Month", y="Total Spent",
                      title="Monthly Spending Trend",
                      color_discrete_sequence=PASTEL_COLORS,
                      template="plotly_white", markers=True)
        fig.update_layout(**PLOTLY_LAYOUT,
                          xaxis_title="Month",
                          yaxis_title="Total Spent (₹)")
        fig.update_traces(fill="tozeroy",
                          fillcolor="rgba(124,92,191,0.08)",
                          line_color="#7c5cbf",
                          line_width=2.5, marker_size=7)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        df_cat = (
            df_filtered.groupby("category")["amount_paid"]
            .sum().reset_index()
            .rename(columns={"amount_paid": "Total Spent"})
        )
        fig2 = styled_pie(df_cat, "category", "Total Spent", "Spending by Category")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if not df_cat.empty:
        top_cat  = df_cat.loc[df_cat["Total Spent"].idxmax(), "category"]
        low_cat  = df_cat.loc[df_cat["Total Spent"].idxmin(), "category"]
        top_amt  = df_cat["Total Spent"].max()
        low_amt  = df_cat["Total Spent"].min()
        df_m2    = df_filtered.groupby(df_filtered["date"].dt.month)["amount_paid"].sum()
        high_m   = MONTH_MAP.get(int(df_m2.idxmax()), "N/A")
        low_m    = MONTH_MAP.get(int(df_m2.idxmin()), "N/A")
        cb_pct   = (total_cb / total_spent * 100) if total_spent > 0 else 0
        cb_count = (df_filtered["cashback"] > 0).sum()

        st.markdown(f"""
        <div class='analysis-block'>
            <h3>📋 Financial Behaviour Analysis</h3>
            <p>Over the selected period, a total of
            <span class='highlight'>{total_tx:,} transactions</span> were recorded
            amounting to <span class='highlight'>₹{total_spent:,.2f}</span>.
            The average transaction value stood at
            <span class='highlight'>₹{avg_tx:,.2f}</span>, indicating a
            moderate-to-high per-transaction spending pattern consistent with
            regular consumer expenditure across multiple categories.</p>
            <p><strong>Category Insights:</strong> The highest expenditure was
            concentrated in the <span class='highlight'>{top_cat}</span> category,
            totalling ₹{top_amt:,.2f}, suggesting this segment drives the most
            financial outflow. Conversely,
            <span class='highlight'>{low_cat}</span> recorded the lowest spend at
            ₹{low_amt:,.2f}, reflecting either infrequent engagement or lower unit
            costs in that domain.</p>
            <p><strong>Monthly Variation:</strong> Expenditure peaked in
            <span class='highlight'>{high_m}</span> and dipped to its lowest in
            <span class='highlight'>{low_m}</span>. This seasonal variation suggests
            cyclical spending behaviour which may correlate with festive seasons,
            salary cycles, or lifestyle events.</p>
            <p><strong>Cashback Efficiency:</strong> Cashback was earned on
            {cb_count} transactions, yielding a total of
            <span class='highlight'>₹{total_cb:,.2f}</span> — representing a
            <span class='highlight'>{cb_pct:.2f}%</span> effective cashback rate.
            This reflects a disciplined use of reward-driven payment instruments.</p>
        </div>
        """, unsafe_allow_html=True)

    download_btn(df_filtered, "Download Filtered Data", "filtered_expenses.csv")


# ─────────────────────────────────────────────
# PAGE 2 — OPERATIONAL ANALYTICS (Core 15)
# ─────────────────────────────────────────────
def page_core():
    st.markdown("""
    <div class='page-header'>
        <h1>Core Analytical Insights</h1>
        <p>Foundational spending insights across categories, modes &amp; time</p>
    </div>
    """, unsafe_allow_html=True)

    query_names = list(core_queries.keys())
    for i in range(0, len(query_names), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(query_names):
                break
            name = query_names[i + j]
            with col:
                try:
                    df = load_core(name)
                    with st.expander(f"**{name}**", expanded=True):
                        render_chart(df, name, theme_idx=(i + j))
                        insight = smart_insight(df, name)
                        st.markdown(
                            f"<div class='insight-box'>💡 {insight}</div>",
                            unsafe_allow_html=True)
                        download_btn(df, "Download",
                                     f"core_{name.lower().replace(' ','_')}.csv")
                except Exception as e:
                    with st.expander(f"**{name}**", expanded=True):
                        st.error(f"Error loading '{name}': {e}")


# ─────────────────────────────────────────────
# PAGE 3 — STRATEGIC FINANCIAL INSIGHTS (Advanced 15)
# ─────────────────────────────────────────────
def page_advanced():
    st.markdown("""
    <div class='page-header'>
        <h1>Strategic Financial Insights</h1>
        <p>Deep-dive analytical views for advanced understanding of your spending</p>
    </div>
    """, unsafe_allow_html=True)

    query_names = list(advanced_queries.keys())
    for i in range(0, len(query_names), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(query_names):
                break
            name = query_names[i + j]
            with col:
                try:
                    df = load_advanced(name)
                    with st.expander(f"**{name}**", expanded=True):
                        render_chart(df, name, theme_idx=(i + j))
                        insight = smart_insight(df, name)
                        st.markdown(
                            f"<div class='insight-box'>💡 {insight}</div>",
                            unsafe_allow_html=True)
                        download_btn(df, "Download",
                                     f"adv_{name.lower().replace(' ','_')}.csv")
                except Exception as e:
                    with st.expander(f"**{name}**", expanded=True):
                        st.error(f"Error loading '{name}': {e}")


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if nav == "Financial Performance Overview":
    page_summary()
elif nav == "Operational Analytics":
    page_core()
elif nav == "Strategic Financial Insights":
    page_advanced()

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    Financial Analytics Dashboard &nbsp;·&nbsp;
    Built using Python · MySQL · Streamlit · Plotly<br>
</div>
""", unsafe_allow_html=True)