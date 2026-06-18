# Task 03 Descriptive Stats

This repository contains Research Task 3 / Milestone B: a generalized descriptive-statistics system applied to the 2024 Facebook political ads dataset.

## Datasets

Source: Google Drive link provided in the iSchool OPT task description.

Dataset used for this submission:

```text
fb_ads_president_scored_anon.csv
```

Do not commit the dataset file. Place the downloaded CSV at:

```text
data/facebook_ads.csv
```

The local file used for this run was:

```text
C:\Users\rojab\MyData\Research Analyst\fb_ads_president_scored_anon (1)\fb_ads_president_scored_anon.csv
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Individual Dataset Analysis

```powershell
python pure_python_stats.py data/facebook_ads.csv --group page_id --group page_id,ad_id
python pandas_stats.py data/facebook_ads.csv --group page_id --group page_id,ad_id
python polars_stats.py data/facebook_ads.csv --group page_id --group page_id,ad_id
```

The scripts accept any CSV path, so the same system can be reused for other datasets later.

## Run Cross-Dataset Comparison

```powershell
python cross_dataset.py data/facebook_ads.csv
```

If additional social-media datasets are added later, pass all paths to `cross_dataset.py` to compare their schemas.

## Findings

This system is designed to reveal both dataset-level patterns and grouped patterns. Dataset-level statistics show missingness, inferred numeric fields, categorical modes, and outliers. Grouped analysis shows which pages and ads dominate the data.

Using the available Facebook Ads file, the dataset contains `246,745` rows, `40` columns, and `246,745` unique `ad_id` values. The largest page groups are:

- Kamala Harris: `55,503` ads
- Donald J. Trump: `23,988` ads
- Joe Biden: `14,822` ads
- The Daily Scroll: `10,461` ads
- Kamala HQ: `9,851` ads by `page_id`
- Tim Walz: `6,581` ads

The `page_id,ad_id` grouped analysis showed one row per pair, confirming that `ad_id` behaves as a unique record identifier in the available ads file.

The generalized scripts are not hardcoded to this file. They can be pointed at additional CSVs by changing the command-line path.

## Reflection

The main design change from Tasks 01 and 02 is removing hardcoded assumptions. Each script accepts a file path and dynamically inspects the schema. This makes the scripts reusable for new CSV files, but it also means that meaningful grouped analysis still requires the researcher to choose sensible grouping columns for each dataset.

Pure Python remains useful for understanding mechanics. Pandas is concise for mixed exploratory work. Polars is strict, fast, and well suited to repeated processing once the desired expressions are clear.
