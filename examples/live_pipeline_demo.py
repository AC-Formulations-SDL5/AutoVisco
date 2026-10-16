"""Run the platform's physics-constrained rheology pipeline on a published descent dataset.

Each sample (``Cell_Label``) is passed through ``predict_cell_rheology`` -- the same routine the web
interface uses: one regularized-hyperbola fit D(h) = A/(h + h_c) + B per spindle speed, followed by
three-pathway characterization (Newtonian / mild / strong shear-thinning / thickening).

This demonstrates the live characterization engine shipped with the current software. The values
reported in the manuscript come from the offline analysis in analysis/figure8_material_rheology.ipynb,
which reproduces data/06_materials/rheology_pipeline_summary.csv exactly.

Usage:
    python examples/live_pipeline_demo.py data/06_materials/sepineo.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from viscometry.rheology.live_adapter import predict_cell_rheology  # noqa: E402


def to_measurements(sample: pd.DataFrame) -> list:
    """Rows in the measurement-record format the live engine consumes."""
    return [
        {"cell_id": 1, "rpm": float(rpm), "height": float(z), "rotational_drag": float(d),
         "torque_percent": float(t), "timestamp": float(i)}
        for i, (rpm, z, d, t) in enumerate(
            zip(sample["RPM"], sample["Z_Height_mm"], sample["Rotational_Drag"], sample["Torque_%"]))
    ]


def analyze(csv_path: Path, torque_floor_pct: float = 0.0) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["Cell_Label", "Z_Height_mm", "RPM", "Torque_%", "Rotational_Drag"])
    df = df[df["RPM"] > 0]
    rows = []
    for label, sample in df.groupby("Cell_Label", sort=False):
        rpms = sorted(sample["RPM"].unique())
        _, s = predict_cell_rheology(1, rpms, to_measurements(sample), torque_floor_pct=torque_floor_pct)
        rows.append({
            "sample": label,
            "n_rpms": len(rpms),
            "pathway": s.get("pathway"),
            "regime": s.get("regime"),
            "n": s.get("n"),
            "K_Pa_s^n": s.get("K_Pas_n"),
            "mu_app_cP": s.get("mu_app_cP"),
            "R2_powerlaw": s.get("R2_powerlaw"),
        })
    out = pd.DataFrame(rows)
    return out.round({"n": 3, "K_Pa_s^n": 3, "mu_app_cP": 1, "R2_powerlaw": 3})


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "06_materials" / "sepineo.csv"
    with pd.option_context("display.width", 160, "display.max_columns", 10):
        print(analyze(path).to_string(index=False))
