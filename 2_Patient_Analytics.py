import io
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PCOS Patient Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME — CSS ONLY FOR STYLING; ALL VISIBLE CONTENT IS NATIVE
# STREAMLIT COMPONENTS, SO RAW <div> HTML CANNOT APPEAR.
# ============================================================
st.markdown(
    """
    <style>
        .stApp {
            background: #07182d;
            color: #f4f7fb;
        }

        [data-testid="stHeader"] {
            background: #07182d;
        }

        [data-testid="stSidebar"] {
            background: #061329;
            border-right: 1px solid #1e426d;
        }

        [data-testid="stSidebar"] * {
            color: #f4f7fb !important;
        }

        .block-container {
            max-width: 1500px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        h1 {
            color: #ffffff !important;
            font-size: 2rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.15rem !important;
        }

        h2, h3 {
            color: #ffffff !important;
        }

        [data-testid="stMetric"] {
            background: #0d2747;
            border: 1px solid #24527f;
            border-radius: 14px;
            padding: 14px;
            min-height: 125px;
        }

        [data-testid="stMetricLabel"] {
            color: #d8e7f8 !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }

        [data-testid="stMetricDelta"] {
            color: #b8d8f5 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #0b2340;
            border: 1px solid #24527f;
            border-radius: 14px;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stLinkButton > a {
            border-radius: 10px !important;
            border: 1px solid #3b6590 !important;
            background: #101f35 !important;
            color: #ffffff !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stLinkButton > a:hover {
            border-color: #63aaf5 !important;
            color: #ffffff !important;
        }

        [data-testid="stCaptionContainer"] {
            color: #a9c8e8 !important;
        }

        hr {
            border-color: #24486f !important;
        }

        .small-note {
            color: #9fc3e8;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data

def load_data():
    df = pd.read_csv("PCOS_data.csv")
    df.columns = [str(c).strip() for c in df.columns]

    # Convert numeric fields safely.
    numeric_columns = [
        " Age (yrs)", "Weight (Kg)", "Height(Cm)", "BMI",
        "Pulse rate(bpm)", "FSH(mIU/mL)", "LH(mIU/mL)",
        "Follicle No. (L)", "Follicle No. (R)", "Endometrium (mm)",
        "BP _Systolic (mmHg)", "BP _Diastolic (mmHg)",
        "Avg. F size (L) (mm)", "Avg. F size (R) (mm)",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "PCOS (Y/N)" in df.columns:
        df["PCOS Label"] = df["PCOS (Y/N)"].map({1: "PCOS Positive", 0: "PCOS Negative"})
        df["PCOS Label"] = df["PCOS Label"].fillna(
            df["PCOS (Y/N)"].astype(str).str.strip().map({
                "1": "PCOS Positive", "0": "PCOS Negative",
                "Y": "PCOS Positive", "N": "PCOS Negative"
            })
        )
    else:
        df["PCOS Label"] = "Unknown"

    # Standardized helper columns.
    if "LH(mIU/mL)" in df.columns and "FSH(mIU/mL)" in df.columns:
        fsh = df["FSH(mIU/mL)"].replace(0, np.nan)
        df["LH_FSH_Ratio"] = df["LH(mIU/mL)"] / fsh

    symptom_columns = {
        "Weight Gain": "Weight gain(Y/N)",
        "Hair Growth (Hirsutism)": "hair growth(Y/N)",
        "Skin Darkening": "Skin darkening (Y/N)",
        "Hair Loss": "Hair loss(Y/N)",
        "Pimples (Acne)": "Pimples(Y/N)",
        "Fast Food Consumption": "Fast food (Y/N)",
    }

    return df, symptom_columns


df, symptom_columns = load_data()

# ============================================================
# HELPERS
# ============================================================
def yes_mask(series):
    s = series.astype(str).str.strip().str.upper()
    return s.isin(["Y", "YES", "1", "TRUE"])


def make_empty_figure(title, message="Not enough data"):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=15, color="#b8d8f5"),
    )
    fig.update_layout(
        title=title,
        height=300,
        paper_bgcolor="#0b2340",
        plot_bgcolor="#0b2340",
        font=dict(color="#f4f7fb"),
        margin=dict(l=20, r=20, t=55, b=20),
    )
    return fig


def style_fig(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor="#0b2340",
        plot_bgcolor="#0b2340",
        font=dict(color="#f4f7fb"),
        margin=dict(l=45, r=20, t=55, b=45),
        legend=dict(font=dict(color="#e9f2fb")),
    )
    fig.update_xaxes(gridcolor="#294867", zerolinecolor="#294867")
    fig.update_yaxes(gridcolor="#294867", zerolinecolor="#294867")
    return fig


# ============================================================
# HEADER — NATIVE STREAMLIT, NO VISIBLE HTML
# ============================================================
header_left, header_right = st.columns([7.5, 2.0], vertical_alignment="center")

with header_left:
    st.title("📊 PCOS Patient Analytics Dashboard")
    st.caption("Comprehensive analysis of PCOS patient dataset")

with header_right:
    st.link_button(
        "📊 Open in Power BI ↗",
        "https://app.powerbi.com/groups/me/reports/9001922a-00a3-431a-9f8b-8ca8ad7a6e6c/5e101a4200c909238e53?experience=power-bi",
        use_container_width=True,
    )

st.divider()

# ============================================================
# FILTER + DATA RANGE SETUP
# ============================================================
age_series = df["Age (yrs)"] if "Age (yrs)" in df.columns else pd.Series([0])
bmi_series = df["BMI"] if "BMI" in df.columns else pd.Series([0])
weight_series = df["Weight (Kg)"] if "Weight (Kg)" in df.columns else pd.Series([0])

age_min, age_max = int(np.nanmin(age_series)), int(np.nanmax(age_series))
bmi_min = float(np.nanmin(bmi_series))
bmi_max = float(np.nanmax(bmi_series))
weight_min, weight_max = int(np.nanmin(weight_series)), int(np.nanmax(weight_series))

# ============================================================
# FILTERS + PATIENT OVERVIEW
# ============================================================
filter_col, dashboard_col = st.columns([1.15, 4.85], gap="medium")

with filter_col:
    st.subheader("🔍 Filters")

    age_range = st.slider(
        "Age Range",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
        step=1,
    )

    bmi_range = st.slider(
        "BMI Range",
        min_value=float(np.floor(bmi_min)),
        max_value=float(np.ceil(bmi_max)),
        value=(float(np.floor(bmi_min)), float(np.ceil(bmi_max))),
        step=0.5,
    )

    weight_range = st.slider(
        "Weight Range (kg)",
        min_value=weight_min,
        max_value=weight_max,
        value=(weight_min, weight_max),
        step=1,
    )

    pcos_options = ["All", "PCOS Positive", "PCOS Negative"]
    pcos_status = st.selectbox("PCOS Status", pcos_options)

    reset = st.button("🔄 Reset Filters", use_container_width=True)
    if reset:
        st.rerun()

    st.divider()

    st.caption(
        "* All visuals are interactive.\n\n"
        "Use filters to explore data."
    )

    with st.container(border=True):
        st.markdown("**♡ Early Detection.**")
        st.markdown("**Better Care.**")
        st.markdown("**Healthier Lives.**")
        st.caption("Every woman's health matters.")

# Apply filters.
filtered = df.copy()

if "Age (yrs)" in filtered.columns:
    filtered = filtered[filtered["Age (yrs)"].between(age_range[0], age_range[1])]
if "BMI" in filtered.columns:
    filtered = filtered[filtered["BMI"].between(bmi_range[0], bmi_range[1])]
if "Weight (Kg)" in filtered.columns:
    filtered = filtered[filtered["Weight (Kg)"].between(weight_range[0], weight_range[1])]
if pcos_status != "All":
    filtered = filtered[filtered["PCOS Label"] == pcos_status]

# ============================================================
# PATIENT OVERVIEW
# ============================================================
with dashboard_col:
    st.subheader("👥 Patient Overview")

    total = len(filtered)
    positive = int((filtered["PCOS Label"] == "PCOS Positive").sum())
    negative = int((filtered["PCOS Label"] == "PCOS Negative").sum())
    avg_bmi = filtered["BMI"].mean() if not filtered.empty else np.nan
    avg_age = filtered["Age (yrs)"].mean() if not filtered.empty else np.nan
    avg_weight = filtered["Weight (Kg)"].mean() if not filtered.empty else np.nan

    m1, m2, m3, m4, m5, m6 = st.columns(6, gap="small")

    m1.metric("👥 Total Patients", f"{total:,}", "Filtered patients")
    m2.metric("👩 PCOS Positive", f"{positive:,}", f"{positive / total * 100:.2f}% of filtered" if total else "0%")
    m3.metric("🛡️ PCOS Negative", f"{negative:,}", f"{negative / total * 100:.2f}% of filtered" if total else "0%")
    m4.metric("⚖️ Average BMI", f"{avg_bmi:.2f}" if pd.notna(avg_bmi) else "—", "kg/m²")
    m5.metric("📈 Average Age", f"{avg_age:.2f}" if pd.notna(avg_age) else "—", "Years")
    m6.metric("👜 Average Weight", f"{avg_weight:.2f}" if pd.notna(avg_weight) else "—", "kg")

    st.caption(f"Showing {total:,} filtered patients out of {len(df):,} total patients.")

    # ========================================================
    # 3 x 3 VISUAL GRID
    # ========================================================
    c1, c2, c3 = st.columns(3, gap="small")

    # --------------------------------------------------------
    # 1. AGE DISTRIBUTION
    # --------------------------------------------------------
    with c1:
        if not filtered.empty:
            fig = px.histogram(
                filtered,
                x="Age (yrs)",
                nbins=15,
                title="📈 Age Distribution",
                labels={"Age (yrs)": "Age (Years)", "count": "Patients"},
            )
            fig.update_traces(marker_color="#64a8f0")
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("📈 Age Distribution"), use_container_width=True)

    # --------------------------------------------------------
    # 2. BMI DISTRIBUTION
    # --------------------------------------------------------
    with c2:
        if not filtered.empty:
            fig = px.histogram(
                filtered,
                x="BMI",
                nbins=15,
                title="⚖️ BMI Distribution",
                labels={"BMI": "BMI (kg/m²)", "count": "Patients"},
            )
            fig.update_traces(marker_color="#e14b91")
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("⚖️ BMI Distribution"), use_container_width=True)

    # --------------------------------------------------------
    # 3. PCOS VS NON-PCOS
    # --------------------------------------------------------
    with c3:
        status_df = pd.DataFrame({"Status": ["PCOS Positive", "PCOS Negative"], "Patients": [positive, negative]})
        fig = px.pie(
            status_df,
            names="Status",
            values="Patients",
            hole=0.55,
            title="🩺 PCOS vs Non-PCOS",
            color="Status",
            color_discrete_map={"PCOS Positive": "#e14b91", "PCOS Negative": "#58b47a"},
        )
        fig.update_traces(textinfo="percent", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    c4, c5, c6 = st.columns(3, gap="small")

    # --------------------------------------------------------
    # 4. BMI BY PCOS STATUS
    # --------------------------------------------------------
    with c4:
        if not filtered.empty:
            fig = px.box(
                filtered,
                x="PCOS Label",
                y="BMI",
                color="PCOS Label",
                title="⚖️ BMI by PCOS Status",
                color_discrete_map={"PCOS Positive": "#e14b91", "PCOS Negative": "#58b47a"},
                labels={"PCOS Label": "PCOS Status", "BMI": "BMI (kg/m²)"},
            )
            fig.update_layout(showlegend=False)
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("⚖️ BMI by PCOS Status"), use_container_width=True)

    # --------------------------------------------------------
    # 5. WEIGHT BY PCOS STATUS
    # --------------------------------------------------------
    with c5:
        if not filtered.empty:
            fig = px.box(
                filtered,
                x="PCOS Label",
                y="Weight (Kg)",
                color="PCOS Label",
                title="👜 Weight by PCOS Status",
                color_discrete_map={"PCOS Positive": "#e14b91", "PCOS Negative": "#58b47a"},
                labels={"PCOS Label": "PCOS Status", "Weight (Kg)": "Weight (kg)"},
            )
            fig.update_layout(showlegend=False)
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("👜 Weight by PCOS Status"), use_container_width=True)

    # --------------------------------------------------------
    # 6. SYMPTOMS FREQUENCY
    # --------------------------------------------------------
    with c6:
        symptom_counts = []
        for label, col in symptom_columns.items():
            if col in filtered.columns:
                symptom_counts.append({"Symptom": label, "Patients": int(yes_mask(filtered[col]).sum())})

        symptom_df = pd.DataFrame(symptom_counts).sort_values("Patients", ascending=True).tail(6)

        if not symptom_df.empty:
            fig = px.bar(
                symptom_df,
                x="Patients",
                y="Symptom",
                orientation="h",
                title="📊 Symptoms Frequency (Top 6)",
                text="Patients",
            )
            fig.update_traces(marker_color="#a968d5", textposition="outside")
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("📊 Symptoms Frequency (Top 6)"), use_container_width=True)

    c7, c8, c9 = st.columns(3, gap="small")

    # --------------------------------------------------------
    # 7. HORMONE ANALYSIS
    # --------------------------------------------------------
    with c7:
        if not filtered.empty:
            grouped = (
                filtered.groupby("PCOS Label")[["FSH(mIU/mL)", "LH(mIU/mL)"]]
                .mean()
                .reset_index()
            )
            long_hormone = grouped.melt(
                id_vars="PCOS Label",
                value_vars=["FSH(mIU/mL)", "LH(mIU/mL)"],
                var_name="Hormone",
                value_name="Average Value",
            )
            long_hormone["Hormone"] = long_hormone["Hormone"].map({
                "FSH(mIU/mL)": "FSH (mIU/mL)",
                "LH(mIU/mL)": "LH (mIU/mL)",
            })
            fig = px.line(
                long_hormone,
                x="PCOS Label",
                y="Average Value",
                color="Hormone",
                markers=True,
                title="🧪 Hormone Analysis",
                color_discrete_map={"FSH (mIU/mL)": "#64a8f0", "LH (mIU/mL)": "#e14b91"},
            )
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("🧪 Hormone Analysis"), use_container_width=True)

    # --------------------------------------------------------
    # 8. LH/FSH RATIO
    # --------------------------------------------------------
    with c8:
        ratio_df = filtered[["PCOS Label", "LH_FSH_Ratio"]].dropna() if "LH_FSH_Ratio" in filtered.columns else pd.DataFrame()
        if not ratio_df.empty:
            fig = px.box(
                ratio_df,
                x="PCOS Label",
                y="LH_FSH_Ratio",
                color="PCOS Label",
                title="📊 LH/FSH Ratio",
                color_discrete_map={"PCOS Positive": "#e14b91", "PCOS Negative": "#58b47a"},
                labels={"PCOS Label": "PCOS Status", "LH_FSH_Ratio": "LH/FSH Ratio"},
            )
            fig.update_layout(showlegend=False)
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("📊 LH/FSH Ratio"), use_container_width=True)

    # --------------------------------------------------------
    # 9. FOLLICLE COUNT ANALYSIS
    # --------------------------------------------------------
    with c9:
        follicle_cols = ["Follicle No. (L)", "Follicle No. (R)"]
        follicle_df = filtered[["PCOS Label"] + follicle_cols].dropna()
        if not follicle_df.empty:
            fig = px.scatter(
                follicle_df,
                x="Follicle No. (L)",
                y="Follicle No. (R)",
                color="PCOS Label",
                title="🌸 Follicle Count Analysis",
                color_discrete_map={"PCOS Positive": "#e14b91", "PCOS Negative": "#58b47a"},
                labels={
                    "Follicle No. (L)": "Left Ovary Follicle Count",
                    "Follicle No. (R)": "Right Ovary Follicle Count",
                    "PCOS Label": "PCOS Status",
                },
                opacity=0.75,
            )
            style_fig(fig)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.plotly_chart(make_empty_figure("🌸 Follicle Count Analysis"), use_container_width=True)

# ============================================================
# DOWNLOAD REPORT — AI INSIGHTS AND CORRELATION HEATMAP REMOVED
# ============================================================
# ============================================================
# DOWNLOAD REPORT
# ============================================================
with st.container(border=True):
    st.subheader("📥 Download Report")
    st.caption("Export filtered patient analytics.")

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📄 Download CSV",
        data=csv_bytes,
        file_name="PCOS_filtered_patient_analytics.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # Create a lightweight PDF without any extra PDF library.
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        fig_pdf = plt.figure(figsize=(8.27, 11.69))
        fig_pdf.patch.set_facecolor("white")
        fig_pdf.text(0.08, 0.94, "PCOS Patient Analytics Report", fontsize=20, weight="bold")
        fig_pdf.text(0.08, 0.915, "Filtered dashboard summary", fontsize=11)

        report_lines = [
            f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
            f"Total patients: {total}",
            f"PCOS positive: {positive}",
            f"PCOS negative: {negative}",
            f"Average BMI: {avg_bmi:.2f}" if pd.notna(avg_bmi) else "Average BMI: —",
            f"Average age: {avg_age:.2f} years" if pd.notna(avg_age) else "Average age: —",
            f"Average weight: {avg_weight:.2f} kg" if pd.notna(avg_weight) else "Average weight: —",
            "",
            "Filters",
            f"Age: {age_range[0]}–{age_range[1]}",
            f"BMI: {bmi_range[0]:.1f}–{bmi_range[1]:.1f}",
            f"Weight: {weight_range[0]}–{weight_range[1]} kg",
            f"PCOS status: {pcos_status}",
        ]

        y = 0.86
        for line in report_lines:
            fig_pdf.text(0.08, y, line, fontsize=11)
            y -= 0.035

        fig_pdf.text(0.08, 0.12, "Source: PCOS Dataset", fontsize=10, color="gray")
        fig_pdf.text(0.08, 0.09, "This report is for analytics and educational purposes.", fontsize=9, color="gray")
        pdf.savefig(fig_pdf, bbox_inches="tight")
        plt.close(fig_pdf)

    pdf_buffer.seek(0)

    st.download_button(
        "📕 Download PDF",
        data=pdf_buffer.getvalue(),
        file_name="PCOS_patient_analytics_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("Source: PCOS Dataset  |  PCOS Patient Analytics Dashboard")