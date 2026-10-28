# AirSense India — Air Quality Trends & Next-Day PM2.5 Prediction

A data science project exploring modelled air-quality estimates across 50 Indian cities, with exploratory data analysis (EDA), an interactive Streamlit dashboard, and a next-day PM2.5 prediction experiment.

> **Important:** This is an educational project based on modelled estimates. It is not an official CPCB monitoring report, health advisory, or operational air-quality forecast.

## Project Overview

AirSense India investigates how PM2.5 concentrations vary across cities and calendar months, explores the relationship between PM2.5 and PM10, and compares a simple persistence baseline with a Random Forest regressor for next-day PM2.5 prediction.

- **Project type:** Data Science, EDA, time-series machine learning
- **Geography:** 50 Indian cities
- **Analysis period:** 1 January 2025–27 October 2026
- **Primary target:** Next-day PM2.5 concentration
- **Dashboard:** Streamlit

## Key Findings

Results currently recorded from the analysis notebook:

- **Highest city-level mean PM2.5:** Delhi, 81.3 µg/m³, followed by Agra (77.1), Ludhiana (72.8), Amritsar (69.2), and Patna (60.9).
- **Monthly pattern:** January had the highest monthly average (approximately 63 µg/m³) and August the lowest (approximately 22 µg/m³) in the available-data aggregation. The 2026 period is incomplete, so this should be treated as a descriptive pattern rather than a confirmed seasonal rule.
- **PM2.5–PM10 correlation:** Pearson correlation of 0.604.
- **Persistence baseline:** MAE 5.712 µg/m³, RMSE 8.783 µg/m³, R² 0.818.
- **Random Forest:** MAE 5.617 µg/m³, RMSE 8.520 µg/m³, R² 0.829.

The Random Forest showed a modest improvement over the persistence baseline on the reported chronological test set. Rerun the notebook before final submission to confirm these metrics still match.

## Data Source and Provenance

- **Hugging Face dataset:** [India Daily Weather & Air Quality (Auto-Updated)](https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality)
- **Kaggle mirror:** [India Daily Weather & Air Quality](https://www.kaggle.com/datasets/akshaykarthickms007/india-daily-weather-and-air-quality)
- **Air-quality source information:** The dataset describes model-based estimates associated with Open-Meteo and the Copernicus Atmosphere Monitoring Service (CAMS).
- **API documentation:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)

The analysis uses a filtered project dataset containing 33,250 records across 50 cities from 1 January 2025 through 27 October 2026. These are model-derived estimates, not direct readings from individual Central Pollution Control Board (CPCB) monitoring stations.

The `india_aqi_pm` field is a PM-only derived index; it should not be described as the official full CPCB AQI. Recent source data may be provisional or revised. Check the dataset card and applicable licence terms for current attribution and reuse requirements.

## Project Structure

```text
AirSense_India/
├── README.md
├── PROJECT_REPORT.md
├── AirSense_India_Analysis.ipynb
├── app.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── air_quality_daily.csv
│   ├── cities.csv
│   └── weather_daily.csv
└── outputs/
    ├── 01_city_pm25_ranking.png
    ├── 02_monthly_seasonality.png
    ├── 03_delhi_mumbai_trends.png
    ├── 04_pm25_pm10_scatter.png
    ├── 05_pm_category_counts.png
    ├── 06_actual_vs_predicted.png
    ├── 07_feature_importance.png
    ├── model_metrics.csv
    └── test_predictions.csv
```

This structure reflects the files visible in the project workspace; filenames may differ if you rename or regenerate outputs. The CSV datasets are not required to be committed to GitHub if they are large; document how to download them instead.

## Tools and Technologies

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Jupyter Notebook
- Streamlit

## Methodology

1. Load, inspect, clean and filter the source data to the selected date range.
2. Explore city-level PM2.5 averages, monthly patterns, Delhi and Mumbai trends, PM2.5–PM10 association, and available PM-derived categories.
3. Sort observations by city and date and create historical PM2.5 lag features and rolling statistics, plus calendar features.
4. Build a persistence baseline using the previous day's PM2.5 value.
5. Train a Random Forest regressor for next-day PM2.5 prediction.
6. Evaluate both approaches using a chronological holdout and compare MAE, RMSE and R².

**Validation reminder:** Make sure every lag and rolling feature uses information available before the prediction time, and verify that train/test target dates do not overlap.

## Quick Start — Windows PowerShell

### 1. Open the project directory

```powershell
cd path\to\AirSense_India
```

Replace the example path with the actual location of your project folder.

### 2. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 3. Run the notebook

```powershell
jupyter notebook AirSense_India_Analysis.ipynb
```

Run the notebook cells from top to bottom. The notebook may download source CSV files into `data/`, so an internet connection is required if the files are not already present. If automatic download fails, follow the dataset source instructions and place the required files in the paths expected by the notebook.

### 4. Launch the dashboard

```powershell
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## Model Evaluation

| Metric | Persistence baseline | Random Forest |
|---|---:|---:|
| MAE (µg/m³) | 5.712 | 5.617 |
| RMSE (µg/m³) | 8.783 | 8.520 |
| R² | 0.818 | 0.829 |

MAE and RMSE measure prediction error, so lower values are better. R² is dimensionless, and higher values are generally better for the same evaluation setup. These scores describe the reported test period only and do not guarantee performance in other seasons or future data.

## Limitations

- The dataset contains model-derived estimates, not direct CPCB station observations.
- Modelled spatial estimates may not represent roadside hotspots or every local variation.
- The analysis period ends on 27 October 2026, so 2026 is incomplete.
- Monthly aggregation combines observations from available years; late-year comparisons are not complete across all years.
- The model uses historical pollution and calendar-related features and may not capture sudden events or all meteorological influences.
- Correlation does not establish causation.
- This project does not provide an official AQI assessment or operational public-health forecast.

## Detailed Report

See [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for the full methodology, results, interpretation, limitations and references.

## Suggested CV Bullet

Built AirSense India, a Python data science project analysing modelled air-quality estimates across 50 Indian cities, with exploratory visualisations and next-day PM2.5 prediction evaluated against a persistence baseline using a chronological test split.

## Acknowledgements

Credit the original dataset creator and consult the dataset card and applicable source/API licences for the required attribution and reuse terms.
