# AirSense India --- Project Report

## Abstract

AirSense India analyses modelled daily air-quality estimates for 50
Indian cities using data from 1 January 2025 to 27 October 2026. The
project applies data cleaning, exploratory data analysis, city-level
comparisons, monthly trend analysis and pollutant relationship analysis
to examine variations in PM2.5 concentrations. A Random Forest
regression model is evaluated against a persistence baseline for
next-day PM2.5 prediction. Delhi recorded the highest mean PM2.5
concentration among the analysed cities at 81.3 µg/m³. The Random Forest
model achieved an MAE of 5.617 µg/m³, an RMSE of 8.520 µg/m³ and an R²
of 0.829, slightly outperforming the persistence baseline. These
findings are limited to modelled estimates and the selected evaluation
period; they do not represent official CPCB monitoring-station
measurements.

## 1. Introduction

PM2.5 refers to fine airborne particles with an aerodynamic diameter of
2.5 micrometres or less. Analysing PM2.5 can help describe differences
in air-quality estimates across locations and time periods. AirSense
India uses Python-based data analysis and visualisation to explore these
patterns across 50 Indian cities and evaluates a machine learning model
for next-day PM2.5 prediction.

This is an educational data science project, not a regulatory
air-quality assessment or an official pollution-warning system.

## 2. Objectives

1.  Clean and validate recent city-level air-quality data.
2.  Compare average PM2.5 concentrations across cities.
3.  Explore monthly PM2.5 patterns and relationships between pollutants.
4.  Visualise available air-quality fields and dataset-derived categories.
5.  Train and evaluate a next-day PM2.5 prediction model against a simple baseline.
6.  Communicate findings, limitations and appropriate interpretations.

## 3. Dataset

**Dataset:** AkshayKarthick, *India Daily Weather & Air Quality
(Auto-Updated)*.

-   **Hugging Face:**
    https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality
-   **Kaggle:**
    https://www.kaggle.com/datasets/akshaykarthickms007/india-daily-weather-and-air-quality
-   **Date coverage used in this project:** 1 January 2025 to 27 October 2026.
-   **Records after cleaning and filtering:** 33,250.
-   **Cities analysed:** 50.
-   **Main variables:** Date, city, PM2.5, PM10, weather variables, India AQI-related fields and pollutant categories.

The dataset provides model-derived air-quality estimates rather than
direct measurements from official CPCB monitoring stations. Results
therefore describe the dataset analysed and should not be presented as
official station readings. The number of records and date coverage above
refer to the project's filtered dataset, not necessarily the full
upstream dataset.

## 4. Tools and Technologies

-   **Programming language:** Python
-   **Data manipulation:** Pandas, NumPy
-   **Visualisation:** Matplotlib, Seaborn
-   **Machine learning:** Scikit-learn
-   **Analysis environment:** Jupyter Notebook
-   **Interactive dashboard:** Streamlit

## 5. Methodology

### 5.1 Data preparation

The dataset was imported and inspected to understand its structure,
columns and data types. Date values were converted to a consistent date
format, and the analysis was filtered to the selected period. Duplicate
records and records with invalid dates or unusable PM2.5 values were
handled during cleaning.

### 5.2 Exploratory data analysis

City-level averages were calculated to compare PM2.5 concentrations
across the 50 cities. Monthly averages were used to explore how PM2.5
varied by calendar month. The Pearson correlation coefficient was
calculated to examine the linear association between PM2.5 and PM10.

### 5.3 Next-day prediction

The modelling workflow sorted observations by city and date and created
historical PM2.5 lag features and rolling statistics, along with
calendar features. A persistence baseline was used for comparison: it
predicts the next day's PM2.5 using the previous day's value. A Random
Forest regressor was then evaluated against that baseline.

The notebook used a chronological holdout based on the latest 20% of
unique dates. The displayed test period began on 18 June 2026 and
continued through 27 October 2026. This preserves time order better than
a random split, although the evaluation period covers only part of the
year.

**Verification note:** Before submitting, confirm in the notebook that
every lag, rolling statistic and other feature uses information
available at prediction time only, and that the target is the intended
next-day PM2.5 value. Also verify that train and test target dates do
not overlap.

## 6. Results and Discussion

### 6.1 Cities with the highest average PM2.5

The five highest city-level mean PM2.5 concentrations in the analysed
dataset were:

    Rank City         Mean PM2.5 (µg/m³)
  ------ ---------- --------------------
       1 Delhi                      81.3
       2 Agra                       77.1
       3 Ludhiana                   72.8
       4 Amritsar                   69.2
       5 Patna                      60.9

These are averages calculated from the selected dataset and period. They
should not be interpreted as official CPCB station averages or as a
ranking of current air quality.

### 6.2 Monthly PM2.5 pattern

In the notebook's available-data monthly aggregation, January had the
highest average PM2.5 concentration at approximately 63 µg/m³, while
August had the lowest at approximately 22 µg/m³. The plotted averages
increased again towards the end of the calendar year.

These figures are descriptive rather than proof of a stable seasonal
pattern. The aggregation combines observations from different years, and
2026 is incomplete. November and December values are based on available
2025 observations, so the comparison is not based on complete
observations for those months across both years.

### 6.3 Relationship between PM2.5 and PM10

The Pearson correlation between PM2.5 and PM10 was **0.604**, indicating
a positive linear association in the analysed data. This correlation
does not establish that one pollutant causes changes in the other.

### 6.4 Model evaluation

The notebook reported the following evaluation metrics:

  Model                       MAE (µg/m³)   RMSE (µg/m³)      R²
  ------------------------- ------------- -------------- -------
  Persistence baseline              5.712          8.783   0.818
  Random Forest regressor           5.617          8.520   0.829

Lower MAE and RMSE indicate smaller prediction errors, while a higher R²
indicates that the model explains more variation in the test targets
under the metric's definition. The Random Forest performed slightly
better than the persistence baseline on all three reported metrics. The
improvement was modest and does not establish that a more complex model
will always perform better.

The reported test results apply to the notebook's chronological test
period, from 18 June to 27 October 2026. Performance may differ in other
periods, locations or conditions.

**Metric note:** MAE and RMSE are expressed in µg/m³ because the target
is PM2.5 concentration. R² is dimensionless.

## 7. Conclusion

AirSense India combines data cleaning, exploratory data analysis,
geographic comparisons, monthly trend analysis and next-day PM2.5
prediction in an interactive air-quality analytics project. In the
analysed dataset, Delhi had the highest mean PM2.5 concentration among
the 50 cities, at 81.3 µg/m³. The monthly aggregation showed lower
averages around the middle of the year and higher averages towards the
end, although the incomplete 2026 coverage means this pattern should be
interpreted cautiously.

The Random Forest regressor achieved an MAE of 5.617 µg/m³, an RMSE of
8.520 µg/m³ and an R² of 0.829 on the chronological test set. It
slightly outperformed the persistence baseline, which achieved an MAE of
5.712 µg/m³, an RMSE of 8.783 µg/m³ and an R² of 0.818. Overall, the
project demonstrates how Python, data visualisation and scikit-learn can
be used to analyse environmental data and build a baseline prediction
workflow.

## 8. Limitations

-   **Modelled data:** The dataset contains model-derived estimates, not
    direct CPCB monitoring-station observations.
-   **Incomplete period:** Data for 2026 ends on 27 October in this
    analysis. Monthly comparisons for the final months of the year are
    therefore incomplete.
-   **Limited evaluation window:** The test set covers 18 June to 27
    October 2026, so results may not generalise to every season or
    future period.
-   **Feature limitations:** The model relies on historical PM2.5 and
    calendar-related features as implemented in the notebook. It may not
    directly capture all meteorological influences, emissions changes or
    sudden pollution events.
-   **No causal claims:** Correlations and observed differences describe
    associations in the dataset; they do not establish causes.
-   **Not an official AQI assessment:** Dataset-derived AQI-related
    fields or categories should not be described as official CPCB AQI
    readings unless their calculation and provenance have been
    independently verified.

## 9. References

1.  AkshayKarthick. *India Daily Weather & Air Quality (Auto-Updated).*
    Hugging Face Datasets.
    https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality
2.  AkshayKarthick. *India Daily Weather & Air Quality.* Kaggle.
    https://www.kaggle.com/datasets/akshaykarthickms007/india-daily-weather-and-air-quality
3.  Open-Meteo. *Air Quality API Documentation.*
    https://open-meteo.com/en/docs/air-quality-api
4.  Central Pollution Control Board (CPCB). *National Air Quality Index
    (AQI) guidance.* https://app.cpcbccr.com/ccr_docs



