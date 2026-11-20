# AutoValue AI

An educational used-car listing valuation and decision-support app built with Python, pandas, scikit-learn, Streamlit and ReportLab.

## Run on Windows

1. Install Python 3.11–3.12 and ensure the Python launcher is available.
2. Keep `work/source_data/carsdekho.csv` in place.
3. Double-click `run_windows.bat`. It creates a local virtual environment, installs dependencies, trains/evaluates candidates, then launches the app in your browser.

For manual setup: `py -3 -m venv .venv`, activate it, run `pip install -r requirements.txt`, `python train_model.py`, then `streamlit run app.py`.

## What it includes

- Random 80/20 held-out evaluation of Ridge, Random Forest, and Extra Trees; winner selected by held-out MAE. The preprocessing is inside the training pipeline to prevent leakage.
- Valuation range based on the 80th percentile of absolute errors on the holdout.
- Searchable supplied listings, side-by-side model summaries, budget shortlists, transparent inspection checklist, running-cost inputs and scenario-only depreciation.
- Downloadable PDF valuation summary and a data/model dashboard.

## Data and limitations

The supplied file has 2,059 rows and 20 columns. Its publisher, collection date, and listing URLs were not included. The target is `Price`, treated as an asking/listing price; sale prices are not verified. The range is a simple empirical error band for this held-out sample, not a guaranteed or conditional prediction interval. Sparse variants, cities, and market shifts may have larger errors. The inspection score is a user checklist, not an AI or mechanical assessment. Cost and depreciation tools are user-defined scenarios. External listings were researched but excluded because their source details, market coverage, and row-level comparability could not be established sufficiently for safe training-data combination.

## Online deployment

Commit this project and `work/source_data/carsdekho.csv` to a GitHub repository. Deploy `app.py` through Streamlit Community Cloud. Include `requirements.txt`; on first start, generate `artifacts/model.joblib` and `artifacts/metrics.json` by running `python train_model.py` locally and commit those artifacts, or adjust the cloud startup flow to train during app startup. Never publish private vehicle or personal data. Streamlit Community Cloud is intended for educational/personal apps; another Python host can run the same app with `streamlit run app.py`.

## Practical viva / demo

1. Explain the target (`Price`) and why this is regression.
2. Show the dataset columns and missing values; explain median/mode imputation and one-hot encoding.
3. Explain train/test separation and why preprocessing lives in a pipeline.
4. Compare MAE (average rupee error), RMSE (penalizes large misses), and R² (variance fit indicator); do not describe R² as accuracy percentage.
5. Demonstrate a valuation, then explain the error band and market-data limitations.
6. Show that inspection checklist, ownership costs, and future depreciation are transparent rules/scenarios, not learned predictions.

## Tests

Run `python -m unittest discover -s tests`. The environment that prepared these files lacked scikit-learn and Streamlit and could not reach the package index, so model training and app execution were not verified here. Run the Windows launcher on a connected machine before the practical.
