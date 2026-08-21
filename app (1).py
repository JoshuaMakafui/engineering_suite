"""
Fluid Flow & Heat Transfer Engineering Suite
Capstone Project — PE 262
Streamlit multi-page engineering application.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math, io, os

from engineering import Fluid, Pipe, HeatExchanger

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLE
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PE 262 Engineering Suite",
page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Fonts & base ───────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0d1b2a;
    border-right: 2px solid #1a3a5c;
}
[data-testid="stSidebar"] * { color: #c8d8e8 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 6px 0; }

/* ── Page background ────────────────────────────────── */
.main { background: #f0f4f8; }

/* ── Module header ──────────────────────────────────── */
.module-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a3a5c 100%);
    color: white;
    padding: 28px 32px 20px;
    border-radius: 12px;
    margin-bottom: 24px;
    border-left: 5px solid #00b4d8;
}
.module-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; color: white; }
.module-header p  { margin: 6px 0 0; color: #90c4e0; font-size: 0.95rem; }

/* ── Result cards ───────────────────────────────────── */
.result-card {
    background: white;
    border-radius: 10px;
    padding: 18px 22px;
    margin: 8px 0;
    border-left: 4px solid #00b4d8;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.result-label { font-size: 0.78rem; color: #6b7a8d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.result-value { font-size: 1.55rem; font-weight: 700; color: #0d1b2a; font-family: 'JetBrains Mono', monospace; }
.result-unit  { font-size: 0.85rem; color: #6b7a8d; margin-left: 4px; }

/* ── Regime badge ───────────────────────────────────── */
.badge-laminar     { background:#d1fae5; color:#065f46; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }
.badge-transitional{ background:#fef3c7; color:#92400e; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }
.badge-turbulent   { background:#fee2e2; color:#991b1b; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }

/* ── Section divider ────────────────────────────────── */
.section-title {
    font-size: 1.05rem; font-weight: 700; color: #1a3a5c;
    border-bottom: 2px solid #00b4d8; padding-bottom: 6px; margin: 20px 0 14px;
}

/* ── Input panel ────────────────────────────────────── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engineering Suite")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🔩 Pipe Flow Analyser", "🌡️ Heat Transfer Calculator", "📊 Rock & Fluid Dashboard"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#607080; line-height:1.6'>"
        "PE 258 Capstone<br>Fluid Flow & Heat Transfer Suite<br>"
        "Peng-Robinson · Darcy-Weisbach · Fourier</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div class="module-header">
        <h1>Fluid Flow & Heat Transfer Engineering Suite</h1>
        <p>A professional multi-module engineering calculator — PE 258 Capstone</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="result-card">
            <div class="result-label">Module A</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0d1b2a; margin:6px 0">🔩 Pipe Flow Analyser</div>
            <div style="font-size:0.85rem; color:#6b7a8d">Reynolds number, friction factor, pressure drop, ΔP vs Q plot, CSV export.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="result-card">
            <div class="result-label">Module B</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0d1b2a; margin:6px 0">🌡️ Heat Transfer</div>
            <div style="font-size:0.85rem; color:#6b7a8d">Fourier conduction, Newton cooling, interactive temperature-time curve.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="result-card">
            <div class="result-label">Module C</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0d1b2a; margin:6px 0">📊 Rock & Fluid Dashboard</div>
            <div style="font-size:0.85rem; color:#6b7a8d">Upload CSV, filter samples, porosity histogram, porosity-permeability crossplot.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Select a module from the sidebar to begin.")

# ─────────────────────────────────────────────────────────────
# MODULE A — PIPE FLOW ANALYSER
# ─────────────────────────────────────────────────────────────
elif page == "🔩 Pipe Flow Analyser":
    st.markdown("""
    <div class="module-header">
        <h1>🔩 Pipe Flow Analyser</h1>
        <p>Darcy-Weisbach equation · Colebrook-White friction factor · Pressure drop analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar inputs ────────────────────────────────────
    with st.sidebar:
        st.markdown("### Fluid Selection")
        st.caption("Properties auto-populated for preset fluids.")
        presets = Fluid.presets()
        fluid_name = st.selectbox("Fluid type", list(presets.keys()))
        fluid = presets[fluid_name]

        if fluid_name == "User-Defined":
            fluid.density   = st.number_input("Density (kg/m³)", value=1000.0, min_value=0.1)
            fluid.viscosity = st.number_input("Dynamic viscosity (Pa·s)", value=1e-3, format="%.2e", min_value=1e-8)

        st.markdown("### Pipe Geometry")
        D = st.number_input("Internal diameter D (m)", value=0.05, min_value=0.001, format="%.4f",
                            help="Internal pipe diameter in metres")
        L = st.number_input("Pipe length L (m)", value=100.0, min_value=0.1,
                            help="Total pipe length in metres")
        eps = st.number_input("Wall roughness ε (m)", value=4.6e-5, min_value=0.0, format="%.2e",
                              help="Absolute roughness: commercial steel ≈ 4.6×10⁻⁵ m")

        st.markdown("### Operating Conditions")
        Q = st.number_input("Flow rate Q (m³/s)", value=0.005, min_value=1e-6, format="%.5f",
                            help="Volumetric flow rate in cubic metres per second")

        st.markdown("### Sweep Range (for plot)")
        Q_min = st.number_input("Q min (m³/s)", value=0.001, min_value=1e-6, format="%.5f")
        Q_max = st.number_input("Q max (m³/s)", value=0.02,  min_value=1e-6, format="%.5f")

    # ── Compute ───────────────────────────────────────────
    try:
        pipe = Pipe(D, L, eps, fluid)
        v    = pipe.velocity(Q)
        Re   = pipe.reynolds(Q)
        f    = pipe.friction_factor(Q)
        dP   = pipe.pressure_drop(Q)
        reg  = pipe.flow_regime(Q)
        qs, dps = pipe.sweep(Q_min, Q_max)

        # ── Results grid ──────────────────────────────────
        st.markdown('<div class="section-title">Flow Results</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="result-card">
                <div class="result-label">Mean Velocity</div>
                <div class="result-value">{v:.3f}<span class="result-unit">m/s</span></div>
            </div>""", unsafe_allow_html=True)
        with c2:
            badge_cls = f"badge-{reg.lower()}"
            st.markdown(f"""<div class="result-card">
                <div class="result-label">Reynolds Number</div>
                <div class="result-value">{Re:,.0f}</div>
                <span class="{badge_cls}">{reg}</span>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="result-card">
                <div class="result-label">Friction Factor (Darcy)</div>
                <div class="result-value">{f:.5f}</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="result-card">
                <div class="result-label">Pressure Drop</div>
                <div class="result-value">{dP/1000:.3f}<span class="result-unit">kPa</span></div>
                <div style="font-size:0.8rem;color:#6b7a8d">{dP:.1f} Pa</div>
            </div>""", unsafe_allow_html=True)

        # ── Fluid info ────────────────────────────────────
        st.markdown('<div class="section-title">Fluid Properties</div>', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns(3)
        fc1.metric("Fluid", fluid.name)
        fc2.metric("Density", f"{fluid.density:.1f} kg/m³")
        fc3.metric("Viscosity", f"{fluid.viscosity:.2e} Pa·s")

        # ── Plot ΔP vs Q ─────────────────────────────────
        st.markdown('<div class="section-title">Pressure Drop vs Flow Rate</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=qs * 1000, y=dps / 1000,
            mode="lines", name="ΔP",
            line=dict(color="#00b4d8", width=3),
            fill="tozeroy", fillcolor="rgba(0,180,216,0.08)"
        ))
        fig.add_vline(x=Q * 1000, line_dash="dash", line_color="#e63946",
                      annotation_text=f"Q = {Q*1000:.3f} L/s", annotation_position="top right")
        fig.update_layout(
            xaxis_title="Flow Rate Q (L/s)",
            yaxis_title="Pressure Drop ΔP (kPa)",
            template="plotly_white",
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family="Inter", size=13),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── CSV Export ────────────────────────────────────
        st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)
        result_df = pd.DataFrame({
            "Flow Rate Q (m³/s)": qs,
            "Flow Rate Q (L/s)":  qs * 1000,
            "Pressure Drop (Pa)": dps,
            "Pressure Drop (kPa)": dps / 1000,
        })
        csv_bytes = result_df.to_csv(index=False).encode()
        st.download_button(
            "⬇ Download ΔP vs Q as CSV",
            data=csv_bytes,
            file_name="pipe_flow_results.csv",
            mime="text/csv"
        )

        # ── Verification ──────────────────────────────────
        with st.expander("📐 Hand-Calculation Verification"):
            area = math.pi * (D/2)**2
            st.markdown(f"""
            **Step-by-step check at Q = {Q:.5f} m³/s:**

            | Step | Formula | Result |
            |---|---|---|
            | Cross-sectional area | A = π(D/2)² = π({D/2:.4f})² | **{area:.6f} m²** |
            | Mean velocity | v = Q/A = {Q}/{area:.6f} | **{v:.4f} m/s** |
            | Reynolds number | Re = ρvD/μ = {fluid.density}×{v:.4f}×{D}/{fluid.viscosity:.2e} | **{Re:,.1f}** |
            | Friction factor | Colebrook-White (ε/D = {eps/D:.2e}) | **{f:.5f}** |
            | Pressure drop | ΔP = f(L/D)(ρv²/2) = {f:.5f}×{L/D:.1f}×{0.5*fluid.density*v**2:.2f} | **{dP:.2f} Pa** |
            """)

    except Exception as e:
        st.error(f"Calculation error: {e}")

# ─────────────────────────────────────────────────────────────
# MODULE B — HEAT TRANSFER CALCULATOR
# ─────────────────────────────────────────────────────────────
elif page == "🌡️ Heat Transfer Calculator":
    st.markdown("""
    <div class="module-header">
        <h1>🌡️ Heat Transfer Calculator</h1>
        <p>Fourier's Law (steady-state conduction) · Newton's Law of Cooling</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🧱 Fourier Conduction", "❄️ Newton Cooling"])

    # ── TAB 1: Fourier Conduction ─────────────────────────
    with tab1:
        with st.sidebar:
            st.markdown("### Wall Conduction Inputs")
            k_cond   = st.number_input("Thermal conductivity k (W/m·K)",  value=50.0, min_value=0.001,
                                       help="Steel ≈ 50, concrete ≈ 1.7, glass ≈ 1.0 W/m·K")
            L_wall   = st.number_input("Wall thickness L (m)",             value=0.05, min_value=0.001,
                                       help="Physical thickness of the wall or slab")
            area_w   = st.number_input("Wall area A (m²)",                 value=1.0,  min_value=0.001,
                                       help="Cross-sectional area perpendicular to heat flow")
            T_H_cond = st.number_input("Hot side temperature T_H (°C)",    value=200.0,
                                       help="Temperature on the hot face of the wall")
            T_C_cond = st.number_input("Cold side temperature T_C (°C)",   value=25.0,
                                       help="Temperature on the cold face of the wall")

        try:
            hx = HeatExchanger(k_cond, L_wall, area_w, T_H_cond, T_C_cond)
            q_flux = hx.heat_flux()
            Q_rate = hx.heat_flow_rate()

            st.markdown('<div class="section-title">Conduction Results</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="result-card">
                    <div class="result-label">Temperature Difference</div>
                    <div class="result-value">{T_H_cond - T_C_cond:.1f}<span class="result-unit">°C</span></div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="result-card">
                    <div class="result-label">Heat Flux q</div>
                    <div class="result-value">{q_flux/1000:.3f}<span class="result-unit">kW/m²</span></div>
                    <div style="font-size:0.8rem;color:#6b7a8d">{q_flux:.1f} W/m²</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="result-card">
                    <div class="result-label">Heat Flow Rate Q</div>
                    <div class="result-value">{Q_rate/1000:.3f}<span class="result-unit">kW</span></div>
                    <div style="font-size:0.8rem;color:#6b7a8d">{Q_rate:.1f} W</div>
                </div>""", unsafe_allow_html=True)

            # Temperature gradient plot
            st.markdown('<div class="section-title">Linear Temperature Profile Through Wall</div>', unsafe_allow_html=True)
            x_wall = np.linspace(0, L_wall * 100, 100)
            T_wall = T_H_cond + (T_C_cond - T_H_cond) * (x_wall / (L_wall * 100))
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=x_wall, y=T_wall, mode="lines",
                                      line=dict(color="#e63946", width=3), name="T(x)",
                                      fill="tozeroy", fillcolor="rgba(230,57,70,0.07)"))
            fig2.update_layout(
                xaxis_title="Position through wall (cm)",
                yaxis_title="Temperature (°C)",
                template="plotly_white", height=320,
                margin=dict(l=20, r=20, t=10, b=20),
                font=dict(family="Inter", size=13)
            )
            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("📐 Hand-Calculation Verification"):
                st.markdown(f"""
                **Fourier's Law: q = k(T_H − T_C)/L**

                | Parameter | Value |
                |---|---|
                | k = {k_cond} W/m·K, L = {L_wall} m, ΔT = {T_H_cond-T_C_cond} °C | |
                | q = {k_cond} × {T_H_cond-T_C_cond} / {L_wall} | **{q_flux:.2f} W/m²** |
                | Q = q × A = {q_flux:.2f} × {area_w} | **{Q_rate:.2f} W** |
                """)
        except Exception as e:
            st.error(f"Error: {e}")

    # ── TAB 2: Newton Cooling ─────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Cooling Parameters</div>', unsafe_allow_html=True)
        nc1, nc2 = st.columns(2)
        with nc1:
            T0_cool     = st.number_input("Initial object temperature T₀ (°C)", value=300.0,
                                          help="Temperature of the object at t = 0")
            T_inf_cool  = st.number_input("Ambient temperature T∞ (°C)",        value=20.0,
                                          help="Surrounding environment temperature")
            T_target_cool = st.number_input("Target temperature (°C)",           value=50.0,
                                            help="Temperature to find the cooling time for")
        with nc2:
            k_cool_val  = st.slider("Cooling constant k (min⁻¹)", 0.001, 0.5, 0.03, 0.001,
                                    help="Higher k = faster cooling. Depends on surface area, material, and fluid.")
            t_max_show  = st.slider("Plot duration (minutes)", 10, 500, 120)

        try:
            t_arr, T_arr = HeatExchanger.cooling_curve(T0_cool, T_inf_cool, k_cool_val, t_max_show)
            t_reach = HeatExchanger.cooling_time(T0_cool, T_inf_cool, T_target_cool, k_cool_val)

            st.markdown('<div class="section-title">Cooling Results</div>', unsafe_allow_html=True)
            rc1, rc2 = st.columns(2)
            with rc1:
                st.markdown(f"""<div class="result-card">
                    <div class="result-label">Time to reach {T_target_cool:.1f} °C</div>
                    <div class="result-value">{t_reach:.2f}<span class="result-unit">min</span></div>
                    <div style="font-size:0.8rem;color:#6b7a8d">{t_reach*60:.1f} seconds</div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                T_at_half = T_inf_cool + (T0_cool - T_inf_cool) * math.exp(-k_cool_val * t_max_show/2)
                st.markdown(f"""<div class="result-card">
                    <div class="result-label">Temperature at {t_max_show//2} min</div>
                    <div class="result-value">{T_at_half:.1f}<span class="result-unit">°C</span></div>
                </div>""", unsafe_allow_html=True)

            # Cooling curve plot
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=t_arr, y=T_arr, mode="lines",
                                      line=dict(color="#00b4d8", width=3), name="T(t)"))
            fig3.add_hline(y=T_inf_cool,     line_dash="dot",  line_color="#6b7a8d",
                           annotation_text=f"T∞ = {T_inf_cool} °C")
            fig3.add_hline(y=T_target_cool,  line_dash="dash", line_color="#e63946",
                           annotation_text=f"Target = {T_target_cool} °C")
            fig3.add_vline(x=t_reach,        line_dash="dash", line_color="#e63946",
                           annotation_text=f"t = {t_reach:.1f} min")
            fig3.update_layout(
                xaxis_title="Time (minutes)",
                yaxis_title="Temperature (°C)",
                template="plotly_white", height=380,
                margin=dict(l=20, r=20, t=10, b=20),
                font=dict(family="Inter", size=13)
            )
            st.plotly_chart(fig3, use_container_width=True)

            with st.expander("📐 Hand-Calculation Verification"):
                ratio = (T_target_cool - T_inf_cool) / (T0_cool - T_inf_cool)
                st.markdown(f"""
                **Newton's Law of Cooling: T(t) = T∞ + (T₀ − T∞)·e^(−kt)**

                Rearranged for time:  **t = −ln[(T_target − T∞)/(T₀ − T∞)] / k**

                | Step | Calculation | Result |
                |---|---|---|
                | Ratio | ({T_target_cool} − {T_inf_cool}) / ({T0_cool} − {T_inf_cool}) | {ratio:.6f} |
                | ln(ratio) | ln({ratio:.6f}) | {math.log(ratio):.6f} |
                | t | −({math.log(ratio):.6f}) / {k_cool_val} | **{t_reach:.4f} min** |
                """)
        except ValueError as e:
            st.warning(f"⚠️ {e}")

# ─────────────────────────────────────────────────────────────
# MODULE C — ROCK & FLUID DASHBOARD
# ─────────────────────────────────────────────────────────────
elif page == "📊 Rock & Fluid Dashboard":
    st.markdown("""
    <div class="module-header">
        <h1>📊 Rock & Fluid Data Dashboard</h1>
        <p>Upload · Filter · Visualise · Download — petrophysical sample analysis</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload a CSV file of rock or fluid sample data",
        type="csv",
        help="Expected columns: porosity (%), permeability (mD), and any other numeric properties."
    )

    # Generate sample data if no upload
    if uploaded is None:
        st.info("No file uploaded — showing a sample dataset of 120 reservoir core samples.")
        np.random.seed(42)
        n = 120
        por = np.random.beta(3, 7, n) * 35 + 5
        perm = 10 ** (0.18 * por - 1.2 + np.random.normal(0, 0.4, n))
        df = pd.DataFrame({
            "sample_id":   [f"S{i+1:03d}" for i in range(n)],
            "depth_m":     np.random.uniform(1800, 3200, n).round(1),
            "porosity_pct": por.round(2),
            "permeability_md": perm.round(3),
            "water_saturation_pct": np.random.beta(2, 5, n) * 60 + 10,
            "lithology":   np.random.choice(["Sandstone", "Limestone", "Dolomite"], n, p=[0.6, 0.3, 0.1])
        })
    else:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns.")

    # ── Summary stats ─────────────────────────────────────
    st.markdown('<div class="section-title">Dataset Summary</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Total Samples", f"{len(df):,}")
    sc2.metric("Columns", len(df.columns))
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if "porosity_pct" in df.columns:
        sc3.metric("Mean Porosity", f"{df['porosity_pct'].mean():.1f} %")
    if "permeability_md" in df.columns:
        sc4.metric("Median Perm", f"{df['permeability_md'].median():.2f} mD")

    st.dataframe(df.head(10), use_container_width=True)

    # ── Filtering ─────────────────────────────────────────
    st.markdown('<div class="section-title">Filter Samples</div>', unsafe_allow_html=True)
    if "porosity_pct" in df.columns:
        por_min = st.slider(
            "Minimum porosity (%)",
            float(df["porosity_pct"].min()),
            float(df["porosity_pct"].max()),
            float(df["porosity_pct"].quantile(0.25)),
            help="Show only samples with porosity above this threshold"
        )
        df_filt = df[df["porosity_pct"] >= por_min]
    else:
        df_filt = df
        st.info("No 'porosity_pct' column found — showing all rows.")

    st.markdown(f"**{len(df_filt):,} samples** match the filter (porosity ≥ {por_min:.1f} %).")

    # ── Charts ────────────────────────────────────────────
    st.markdown('<div class="section-title">Visualisations</div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    with ch1:
        if "porosity_pct" in df_filt.columns:
            fig_hist = px.histogram(
                df_filt, x="porosity_pct", nbins=25,
                title="Porosity Distribution",
                labels={"porosity_pct": "Porosity (%)"},
                color_discrete_sequence=["#00b4d8"],
                template="plotly_white"
            )
            fig_hist.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=10),
                                   font=dict(family="Inter", size=12))
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Add a 'porosity_pct' column to see histogram.")

    with ch2:
        if "porosity_pct" in df_filt.columns and "permeability_md" in df_filt.columns:
            color_col = "lithology" if "lithology" in df_filt.columns else None
            fig_cross = px.scatter(
                df_filt, x="porosity_pct", y="permeability_md",
                color=color_col,
                log_y=True,
                title="Porosity–Permeability Crossplot",
                labels={"porosity_pct": "Porosity (%)", "permeability_md": "Permeability (mD)"},
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_cross.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=10),
                                    font=dict(family="Inter", size=12))
            fig_cross.update_traces(marker=dict(size=7, opacity=0.75))
            st.plotly_chart(fig_cross, use_container_width=True)
        else:
            st.info("Add 'porosity_pct' and 'permeability_md' columns to see crossplot.")

    # ── Download ──────────────────────────────────────────
    st.markdown('<div class="section-title">Download Filtered Data</div>', unsafe_allow_html=True)
    csv_out = df_filt.to_csv(index=False).encode()
    st.download_button(
        "⬇ Download Filtered Samples as CSV",
        data=csv_out,
        file_name="filtered_samples.csv",
        mime="text/csv"
    )
