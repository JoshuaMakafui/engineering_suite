"""
engineering.py — Core OOP module for the Fluid Flow & Heat Transfer Engineering Suite.
All physics classes live here; imported by the Streamlit app.
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────────────────────
# FLUID CLASS
# ─────────────────────────────────────────────────────────────
@dataclass
class Fluid:
    """
    Represents a fluid with physical properties.

    Attributes:
        name        : Human-readable fluid name.
        density     : Fluid density (kg/m³).
        viscosity   : Dynamic viscosity (Pa·s).
        description : Optional description string.
    """
    name: str
    density: float       # kg/m³
    viscosity: float     # Pa·s
    description: str = ""

    @classmethod
    def presets(cls) -> dict:
        """Return a dict of common fluids by name."""
        return {
            "Water (20 °C)":    cls("Water (20 °C)",    998.2,  1.002e-3, "Standard liquid water at 20 °C"),
            "Air (20 °C)":      cls("Air (20 °C)",       1.204,  1.825e-5, "Dry air at 20 °C, 1 atm"),
            "Crude Oil":        cls("Crude Oil",          870.0,  5.00e-3,  "Medium crude oil, ~30 API"),
            "User-Defined":     cls("User-Defined",       1000.0, 1.00e-3,  "Enter your own properties"),
        }


# ─────────────────────────────────────────────────────────────
# PIPE CLASS
# ─────────────────────────────────────────────────────────────
class Pipe:
    """
    Models pipe flow using the Darcy-Weisbach equation and Colebrook friction factor.

    Parameters:
        diameter   : Internal pipe diameter (m).
        length     : Pipe length (m).
        roughness  : Absolute pipe roughness (m). Default 4.6e-5 m (commercial steel).
        fluid      : A Fluid instance describing the flowing fluid.
    """

    def __init__(self, diameter: float, length: float, roughness: float, fluid: Fluid):
        if diameter <= 0 or length <= 0 or roughness < 0:
            raise ValueError("Diameter and length must be positive; roughness must be non-negative.")
        self.diameter  = diameter
        self.length    = length
        self.roughness = roughness
        self.fluid     = fluid

    def velocity(self, flow_rate_m3s: float) -> float:
        """
        Calculate mean flow velocity.

        Parameters:
            flow_rate_m3s : Volumetric flow rate (m³/s).

        Returns:
            float: Mean velocity (m/s).
        """
        area = math.pi * (self.diameter / 2) ** 2
        return flow_rate_m3s / area

    def reynolds(self, flow_rate_m3s: float) -> float:
        """
        Calculate Reynolds number (dimensionless).

        Parameters:
            flow_rate_m3s : Volumetric flow rate (m³/s).

        Returns:
            float: Reynolds number Re = ρvD/μ.
        """
        v = self.velocity(flow_rate_m3s)
        return (self.fluid.density * v * self.diameter) / self.fluid.viscosity

    def flow_regime(self, flow_rate_m3s: float) -> str:
        """Return flow regime string based on Reynolds number."""
        Re = self.reynolds(flow_rate_m3s)
        if Re < 2300:
            return "Laminar"
        elif Re < 4000:
            return "Transitional"
        return "Turbulent"

    def friction_factor(self, flow_rate_m3s: float) -> float:
        """
        Calculate Darcy friction factor.
        Uses analytical formula for laminar; Colebrook-White iteration for turbulent.

        Parameters:
            flow_rate_m3s : Volumetric flow rate (m³/s).

        Returns:
            float: Darcy friction factor f.
        """
        Re = self.reynolds(flow_rate_m3s)
        if Re < 2300:
            return 64 / Re  # Laminar — exact analytical result
        # Swamee-Jain approximation (explicit, accurate to < 3% of Colebrook)
        rr = self.roughness / self.diameter
        f = 0.25 / (math.log10(rr / 3.7 + 5.74 / Re ** 0.9)) ** 2
        # Colebrook-White Newton refinement (3 iterations)
        for _ in range(3):
            lhs = -2 * math.log10(rr / 3.7 + 2.51 / (Re * math.sqrt(f)))
            f = (1 / lhs) ** 2
        return f

    def pressure_drop(self, flow_rate_m3s: float) -> float:
        """
        Calculate pressure drop along the pipe (Pa) using Darcy-Weisbach.

        Parameters:
            flow_rate_m3s : Volumetric flow rate (m³/s).

        Returns:
            float: Pressure drop ΔP (Pa).
        """
        f = self.friction_factor(flow_rate_m3s)
        v = self.velocity(flow_rate_m3s)
        return f * (self.length / self.diameter) * 0.5 * self.fluid.density * v ** 2

    def sweep(self, q_min: float, q_max: float, n: int = 60):
        """
        Sweep flow rate over a range and return arrays of (Q, ΔP).

        Parameters:
            q_min, q_max : Flow rate range (m³/s).
            n            : Number of points.

        Returns:
            tuple: (Q_array, dP_array) as numpy arrays.
        """
        qs = np.linspace(q_min, q_max, n)
        dps = np.array([self.pressure_drop(q) for q in qs])
        return qs, dps


# ─────────────────────────────────────────────────────────────
# HEAT EXCHANGER / COOLING CLASS
# ─────────────────────────────────────────────────────────────
class HeatExchanger:
    """
    Models steady-state heat conduction and Newton's Law of Cooling.

    Parameters:
        k      : Thermal conductivity of wall material (W/m·K).
        L      : Wall thickness (m).
        area   : Wall cross-sectional area (m²).
        T_H    : Hot-side temperature (°C).
        T_C    : Cold-side temperature (°C).
    """

    def __init__(self, k: float, L: float, area: float, T_H: float, T_C: float):
        if L <= 0 or area <= 0 or k <= 0:
            raise ValueError("k, L, and area must all be positive.")
        self.k    = k
        self.L    = L
        self.area = area
        self.T_H  = T_H
        self.T_C  = T_C

    def heat_flux(self) -> float:
        """
        Calculate heat flux using Fourier's Law: q = k(T_H - T_C)/L.

        Returns:
            float: Heat flux q (W/m²).
        """
        return self.k * (self.T_H - self.T_C) / self.L

    def heat_flow_rate(self) -> float:
        """
        Calculate total heat flow rate: Q = q × A.

        Returns:
            float: Heat flow rate Q (W).
        """
        return self.heat_flux() * self.area

    @staticmethod
    def cooling_time(T0: float, T_inf: float, T_target: float, k_cool: float) -> float:
        """
        Time for object to cool from T0 to T_target (Newton's Law of Cooling).
        T(t) = T_inf + (T0 - T_inf) * exp(-k * t)

        Parameters:
            T0       : Initial temperature (°C).
            T_inf    : Ambient temperature (°C).
            T_target : Target temperature (°C).
            k_cool   : Cooling constant (min⁻¹).

        Returns:
            float: Time in minutes.

        Raises:
            ValueError: If T_target is not between T_inf and T0.
        """
        if not (T_inf < T_target < T0):
            raise ValueError(
                f"T_target ({T_target} °C) must be strictly between "
                f"T_inf ({T_inf} °C) and T0 ({T0} °C)."
            )
        ratio = (T_target - T_inf) / (T0 - T_inf)
        return -math.log(ratio) / k_cool

    @staticmethod
    def cooling_curve(T0: float, T_inf: float, k_cool: float, t_max: float, n: int = 200):
        """
        Generate temperature vs time curve for Newton's Law of Cooling.

        Parameters:
            T0     : Initial temperature (°C).
            T_inf  : Ambient temperature (°C).
            k_cool : Cooling constant (min⁻¹).
            t_max  : Maximum time (minutes).
            n      : Number of points.

        Returns:
            tuple: (t_array, T_array) as numpy arrays.
        """
        t = np.linspace(0, t_max, n)
        T = T_inf + (T0 - T_inf) * np.exp(-k_cool * t)
        return t, T
