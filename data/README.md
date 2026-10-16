# AutoVisco data

All data supporting *AutoVisco: Physics-Informed Autonomous Rheometry of Liquids, Gels, and Pastes for Self-Driving Laboratories* are provided here as CSV files and
released under [CC BY 4.0](LICENSE.md).

Units unless stated otherwise: heights and Z positions in **mm**, spindle speed in **rpm**, torque in
**percent of full scale** (100% = 7,187.0 dyne·cm), viscosity in **cP**, time in **s**.
Rotational drag is `Torque_% / RPM`.

## Folder guide

| Folder | Files | Description | Manuscript |
| --- | --- | --- | --- |
| `01_manual_descent/` | `manual_vs_auto_drag.csv` | Manual descent (13 µm increments) for 60, 10, and 1 kcP silicone oils, side by side with two automated trials. Two header rows: group (`Manual`, `Auto_trial1`, `Auto_trial2`) and column name. | Fig. 2B–D, Fig. 7K |
| `02_hitpoints/` | `hitpoints.csv` | Detected container-contact Z height for each of 18 cells across repeated runs. | Fig. 4B |
| `03_silicone_calibration/` | `calibration_*.csv`, `full_run_*.csv`, `silicone_10kcP_*.csv`, `silicone_60kcP_*.csv`, `height_normalized.csv` | Automated descents on silicone standards (1–125 kcP) with live feedback diagnostics; `height_normalized.csv` holds per-oil drag versus re-zeroed height used for the calibration. | Fig. 4, Fig. 7A–G |
| `04_reproducibility/` | `silicone_12p5kcP_*.csv`, `silicone_37kcP_*.csv` | Repeat runs of one oil across cells and washing protocols. | Robustness |
| `05_time_series/` | `torque_time_series_v2.csv`, `torque_time_series_v3.csv` | Torque versus elapsed time at each Z height for every silicone standard (columns encode oil and rpm). | Fig. 7 |
| `06_materials/` | `silicone.csv`, `peg.csv`, `peg2.csv`, `sepineo.csv`, `sepineo2.csv`, `solagum.csv`, `solagum2.csv`, `carbopol.csv`, `syy.csv`, `sekisui_b41.csv`, `hy500.csv`, `tims.csv`, `rheology_pipeline_summary.csv` | Multi-rpm descents for every material family and the per-sample rheology summary (regime, flow index, apparent viscosity). | Fig. 8, Fig. 9A |
| `07_reference_viscometry/` | `manual_reference_readings.csv` | Manual reference readings (rpm, shear rate, viscosity, torque, shear stress, accuracy). | Reference rheology |
| `08_analysis_outputs/` | `sweep_*.csv`, `model_comparison_*.csv`, `params_*`, `metrics_*`, `bootstrap_*`, `loo_cv.csv`, `master_curve*.csv`, `per_fluid_fits.csv`, `amplitudes.csv`, `normalized_drag_summary.csv`, `nonnewtonian_predictions.csv` | Model selection, fitted parameters, 500-iteration bootstrap, leave-one-out validation, and master-curve analysis. | Fig. 4, Fig. 7H–J, Fig. S2 |
| `09_simulation/` | `torque_vs_h.csv` | Lubrication-model torque versus gap (header lines start with `#` and give μ and cone angle). | Model validation |
| `calibration/` | `discovery_bulk_calibration.json` | Bulk calibration used by the software's discovery mode. | Software |

## Column dictionary

**Descent records** (`03_*`, `04_*`, `06_*`). Some files start with `#` metadata lines; the table starts at the
row beginning `row,cell`.

| Column | Meaning |
| --- | --- |
| `row`, `cell` | Deck row and cell index |
| `Cell_Label` | Sample label (e.g. `l10000_sl_a11860` = nominal 10,000 cP, reference 11,860 cP; `2%sep_50110` = 2% Sepineo, reference 50,110 cP) |
| `Z_Height_mm` | Spindle Z coordinate (more negative = closer to the container floor) |
| `RPM` | Spindle speed |
| `Elapsed_Time_s` | Time since the speed step began |
| `Torque_%` | Torque, percent of full scale |
| `Rotational_Drag` | `Torque_% / RPM` |
| `CV`, `R2`, `Trend_Slope`, `Second_derivative*`, `R2_*` | Windowed feedback diagnostics used for contact detection |
| `Hit_*`, `Hit_Point_Confidence`, `Hit_Detected`, `Hit_Reasons` | Contact-detection flags, composite confidence (hit at ≥ 0.8), and reason |

**Rheology summary** (`06_materials/rheology_pipeline_summary.csv`): `sample`, `label`, reference viscosity
`true_mu_cP`, number of speeds `n_rpms`, `regime`, flow index `n_idx`, apparent viscosity `mu_app_cP`,
mean drag-fit `R2_drag_mean`, and power-law `R2_powerlaw`.

## Reproducing results

`analysis/figure8_material_rheology.ipynb` reads `06_materials/` and `03_silicone_calibration/height_normalized.csv`
and regenerates `rheology_pipeline_summary.csv` and the stress-based flow curves. See the main
[README](../README.md#reproducing-the-paper) for the figure scripts.
