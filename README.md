# Task 03 Descriptive Stats

This repository contains Research Task 3 / Milestone B: a generalized descriptive-statistics system for multiple 2024 election social media datasets.

## Datasets

Source: Google Drive link provided in the iSchool OPT task description.

Expected local files:

```text
data/facebook_ads.csv
data/facebook_posts.csv
data/twitter_posts.csv
```

Do not commit dataset files.

Current local data status:

- Facebook Ads is available locally as `C:\Users\rojab\MyData\Research Analyst\fb_ads_president_scored_anon (1)\fb_ads_president_scored_anon.csv`.
- Facebook Posts is not currently available in the workspace.
- Twitter/X Posts is not currently available in the workspace.

The scripts are ready for all three files, but the full cross-dataset comparison requires the missing Facebook Posts and Twitter/X Posts CSVs.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Individual Dataset Analysis

```powershell
python pure_python_stats.py data/facebook_ads.csv --group page_id --group page_id,ad_id
python pandas_stats.py data/facebook_posts.csv --group page_id
python polars_stats.py data/twitter_posts.csv --group account_id
```

The grouping columns are optional and should be adjusted to the actual columns present in each file.

## Run Cross-Dataset Comparison

```powershell
python cross_dataset.py data/facebook_ads.csv data/facebook_posts.csv data/twitter_posts.csv
```

## Findings

This system is designed to reveal both within-dataset patterns and cross-platform differences. Dataset-level statistics show missingness, inferred numeric fields, categorical modes, and outliers. Grouped analysis shows which pages, accounts, ads, or posts dominate the data. Cross-dataset comparison identifies shared columns and columns unique to each platform, which is necessary before comparing engagement or activity metrics across Facebook Ads, Facebook Posts, and Twitter/X Posts.

Using the available Facebook Ads file, the dataset contains `246,745` rows, `40` columns, and `246,745` unique `ad_id` values. The largest page groups are:

- Kamala Harris: `55,503` ads
- Donald J. Trump: `23,988` ads
- Joe Biden: `14,822` ads
- The Daily Scroll: `10,461` ads
- Kamala HQ: `9,851` ads by `page_id`
- Tim Walz: `6,581` ads

The `page_id,ad_id` grouped analysis showed one row per pair, confirming that `ad_id` behaves as a unique record identifier in the available ads file.

The full Task 03 cross-platform findings should be completed after placing the missing files at `data/facebook_posts.csv` and `data/twitter_posts.csv`, then running `cross_dataset.py`.

## Reflection

The main design change from Tasks 01 and 02 is removing hardcoded assumptions. Each script accepts a file path and dynamically inspects the schema. This makes the scripts reusable for new CSV files, but it also means that meaningful grouped analysis still requires the researcher to choose sensible grouping columns for each dataset.

Pure Python remains useful for understanding mechanics. Pandas is concise for mixed exploratory work. Polars is strict, fast, and well suited to repeated processing once the desired expressions are clear.
