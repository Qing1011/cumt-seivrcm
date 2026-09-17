# CUMT SEIVR-CM: race/ethnicity-stratified SEIVR model with contact matrices

Code, notebooks and intermediate data used by the Columbia University Modelling Team
(`cumt`, model `seivrcm`) for the COVID-19 Scenario Modeling Hub *Disparities* round
(California = location `06`, North Carolina = location `37`).

* **Model**: Susceptible-Exposed-Infected-Vaccinated-Recovered (SEIVR) compartments per
  race/ethnicity, coupled through a normalised contact matrix. Transmission rates (beta) vary by
  race/ethnicity and by 28-day window; the initial seeds and the betas are fitted to weekly deaths
  with a Metropolis-Hastings MCMC. Deaths are simulated from infections through a
  gamma-distributed delay and a smoothed daily infection-fatality rate (IFR) built from serology
  and death data.
* **Phase 1** (submitted 2024-06-25): calibration to 2020-03-28 – 2020-11-14, projection of
  Scenario A to 2020-11-15 – 2021-04-03 with a humidity (seasonal) factor and an NPI factor.
* **Phase 2** (submitted 2024-07-16): calibration over the whole period with 14 windows and
  Scenarios A (as fitted), B (non-White betas capped at the White beta), C (non-White
  age-adjusted IFR capped at the White IFR), D (both).

## Repository layout

```
codes/        Python modules imported (via %run) by the notebooks
notebook/     pipeline notebooks (numbered in run order) + the intermediate files they read/write
data/         raw inputs: SMH coordination-team data (data/github), humidity, OxCGRT stringency
```

The notebooks keep the original working convention: they are run from `notebook/`, import
modules with `%run ../codes/<module>.py`, read raw data from `../data/github/` and read/write
their intermediate CSV/NPY files in the current directory.

## Environment

Python 3.11 was used originally. Install with:

```bash
pip install -r requirements.txt
```

## Pipeline

| Step | Notebook (this repo) | Original notebook | Main inputs | Outputs |
|---|---|---|---|---|
| 01 | `01_contact_matrix.ipynb` | `Contact_matrix.ipynb` | `data/github/contact_matrix/*/contact_matrix/full_matrix_pandemic_*.csv` | `CM_06_normalised.csv`, `CM_37_normalised.csv` (row-normalised, rows = race of the individual) |
| 02 | `02_target_data.ipynb` | `1_Target_data.ipynb` | `data/github/target-data/target_data_phase2.csv` | weekly `cases_06/37.csv`, `deaths_06/37_phase2_v3.csv` (deaths adjusted by adding `min_suppressed`) |
| 03 | `03_serology_rates.ipynb` | `0_serology_complete.ipynb` | `data/github/serology/serology_data_complete.csv` | monotone, CI-clipped monthly infection rates `serology_rates_06/37.csv` |
| 04a | `04a_ifr_phase1_CA.ipynb` | `smooth_curve_06.ipynb` | `deaths_06_phase2_v2.csv`, `serology_infections_06_complete.csv` | Phase 1 daily IFR `my_ifr_ts-v4_06.csv` |
| 04b | `04b_ifr_phase1_NC.ipynb` | `2_smooth_curve_37.ipynb` | `deaths_37_phase2_v2.csv`, `serology_infections_37_complete.csv` | Phase 1 daily IFR `my_ifr_ts-v4_37.csv` |
| 05 | `05_ifr_phase2.ipynb` | `Phase2_smooth_v2.ipynb` | `deaths_*_phase2_v3.csv`, `serology_rates_*.csv` | Phase 2 daily IFR `my_ifr_ts-v6_06.csv`, `my_ifr_ts-v6_37.csv` |
| 06 | `06_vaccination_rate.ipynb` | `vaccination.ipynb` | `data/github/vaccination/vaccination_data.csv`, `serology_rates_*.csv` | daily vaccination rate `M_eta_06_v2.csv`, `M_eta_37_v2.csv` |
| 07 | `07_npi_stringency.ipynb` | `NPI.ipynb` | `data/OxCGRT_USA_differentiated_withnotes_2020/2021.csv` | weekly `stringency_wk_ca.csv`, `stringency_wk_nc.csv` |
| 08a | `08a_phase1_projection_CA.ipynb` | `forward_predition.ipynb` | `M_trace_06_v2.npy`, IFR, eta, `data/abshumidity.csv`, stringency | Phase 1 samples `output_06_phase1.csv`; susceptibility histogram (`beta06.png`) |
| 08b | `08b_phase1_projection_NC.ipynb` | `forward_projection_37.ipynb` | `M_trace_37_v2.npy`, IFR, eta, humidity, stringency | Phase 1 samples `output_37_v2.csv`; susceptibility histogram (`beta07.png`) |
| 09a | `09a_phase2_mcmc_scenarios_CA.ipynb` | `SEIRV_MCMC-V6.ipynb` | `deaths_06_phase2_v3.csv`, `my_ifr_ts-v6_06.csv`, `M_eta_06_v2.csv` | MCMC trace `M_trace_06_phase1.npy`, `beta_06_phase2_A.csv`, Scenarios A–D `output_06_phase2.csv` |
| 09b | `09b_phase2_mcmc_scenarios_NC.ipynb` | `SEIRV_MCM-V6_37.ipynb` | `deaths_37_phase2_v3.csv`, `my_ifr_ts-v6_37.csv`, `M_eta_37_v2.csv` | MCMC trace `M_trace_37_phase2.npy`, `beta_37_phase2_A.csv`, Scenarios A–D `output_37_phase2.csv` |
| 10 | `10_phase2_scenario_adjustment.ipynb` | `phase2_scenario.ipynb` | `my_ifr_ts-v6_*.csv`, `beta_*_phase2_A.csv` | `my_ifr_ts-v6_*_adj.csv` (Scenario C), `beta_*_phase2_A_adj.csv` (Scenario B); prints the severity-reduction table of the Phase 2 abstract |
| 11 | `11_submission_output.ipynb` | `output.ipynb` | `output_*` CSVs and `2023-11-12-Ensemble.parquet` as a schema reference | Combines the state-level Phase 1 and Phase 2 samples and writes Scenario Modeling Hub-format parquet output |

Run order for Phase 2: 09a/09b up to the cell that saves `beta_*_phase2_A.csv`, then notebook 10,
then the remaining cells of 09a/09b (they load the `_adj` files produced by 10), then 11.

### Modules in `codes/`

| File | Role |
|---|---|
| `data_input.py` | populations, race lists, colours, fixed epidemiological parameters (L=600, Z=5, D=5, P=730, rho_c=0.95), age-specific IFR ratios and 65+ shares used for the Scenario C age adjustment |
| `SEIVR.py` | one daily step of the SEIVR model with the contact matrix (`SEIRV_count`) |
| `mcmc_fun.py` | delay distribution, initial state, simulation over T days, weekly aggregation, likelihood, `para_LKH`, `get_wk_death` (used for NC and Phase 1) |
| `mcmc_fun_06.py` | same as `mcmc_fun.py` but with the likelihood scale used for the California Phase 2 fit (`0.5*obs + 10`) |
| `phase2.py` | `adjust_array` (cap non-White columns at White), `plot_ifr_comparison`, `simulate_scenario` (Scenarios B–D) |
| `full_contact_matrix.py` | `get_CM_normalised` (setting-specific matrices; superseded by the full pandemic matrix in notebook 01) |
| `curve_prepare.py` | helpers for weekly-to-daily distribution and curve fitting |

## Notes and caveats

* **MCMC runtime**: the fitting loops in 09a/09b take many hours. The finished traces are
  included (`M_trace_06_phase1.npy`, `M_trace_37_phase2.npy` for Phase 2; `M_trace_06_v2.npy`,
  `M_trace_37_v2.npy` for Phase 1) so all post-processing cells can be run without refitting.
  Despite its name, `M_trace_06_phase1.npy` is the 14-window Phase 2 trace saved by notebook 09a.
* **Phase 1 traces** were produced by the same MCMC notebooks configured with `n_windows = 9`
  and the Phase 1 inputs (`my_ifr_ts-v4_*`, `M_eta_06.csv`/`M_eta_37.csv`, `deaths_*_phase2_v2.csv`).
  The saved notebooks are configured for Phase 2 (`n_windows = 14`).
* `serology_infections_06/37_complete.csv` (used by 04a/04b) were written by an earlier revision of
  notebook 03; the code that computed them (`N * smoothed rates`) is still present but commented out.
* Some `np.savetxt` lines that write final files (for example `my_ifr_ts-v6_*.csv` in 05,
  `M_eta_06_v2.csv` in 06, `CM_06_normalised.csv` in 01) are commented out in the notebooks to
  avoid accidental overwrites. Uncomment them to regenerate the files.
* Notebook 07 originally read `../Data/...`; the path was changed to `../data/...` so it also
  works on case-sensitive file systems. No other notebook content was modified.
* Notebook 11 loads `2023-11-12-Ensemble.parquet` only as a schema reference for the hub format.
* North Carolina has no Latino group in the hub data; NC uses four groups
  (asian, white, black, other), California five (asian, white, black, latino, other).

## Data sources

* `data/github/`: coordination-team inputs for the SMH disparities round used in this analysis
  (contact matrices, population, serology, target case/death data, vaccination). See
  `data/github/README.md` for the original sources.
* `data/OxCGRT_USA_differentiated_withnotes_2020/2021.csv`: Oxford COVID-19 Government Response
  Tracker (state-level stringency index).
* `data/abshumidity.csv`: daily absolute humidity climatology by US city; the columns are averaged
  to build the seasonal factor in 08a/08b.
