# Fluid Flow & Heat Transfer Engineering Suite

A professional multi-module engineering web application built with Streamlit.

## Live App
Deploy to Streamlit Community Cloud — see below.

## Modules
- **Module A — Pipe Flow Analyser**: Reynolds number, Colebrook-White friction factor, Darcy-Weisbach pressure drop, ΔP vs Q plot, CSV export.
- **Module B — Heat Transfer Calculator**: Fourier conduction (flat wall), Newton's Law of Cooling with interactive cooling curve.
- **Module C — Rock & Fluid Dashboard**: Upload CSV, filter by porosity, porosity histogram, porosity-permeability crossplot, download filtered data.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## AI Usage Documentation
**Prompt 1:** "Build a Pipe class implementing Darcy-Weisbach with Colebrook-White friction factor. Include velocity(), reynolds(), friction_factor(), and pressure_drop() methods with full docstrings."
*Verified:* Colebrook-White Newton refinement loop and Swamee-Jain initialisation checked against hand calculations for water at Re = 10,000 (f = 0.03085 — matches tabulated value).

**Prompt 2:** "Add a HeatExchanger class with Fourier's Law (heat_flux, heat_flow_rate) and static Newton cooling methods (cooling_time, cooling_curve). Include ValueError for invalid T_target."
*Verified:* cooling_time formula −ln(ratio)/k verified analytically. heat_flux = k·ΔT/L verified for steel (k=50, ΔT=175, L=0.05 → q = 175,000 W/m²).

**Prompt 3:** "Build the Streamlit UI with sidebar inputs, result cards, Plotly charts, and a CSV export button. Use Inter font and a navy/cyan colour scheme."
*Corrected:* Removed `st.set_theme()` (not a valid Streamlit API); replaced with CSS injection via `st.markdown()`. Fixed Fluid.presets() classmethod — initial version had incorrect self-reference.

## Technical Challenge
Implementing the Colebrook-White equation (implicit in f) required an iterative Newton solver seeded with the explicit Swamee-Jain approximation. Three Newton steps converge f to < 0.0001% error.

## What I Would Add Next
Multi-layer wall conduction (composite walls), pipe network solver (Hardy Cross method), and a PVT flash module integrated with the Peng-Robinson EOS from PE 258.
