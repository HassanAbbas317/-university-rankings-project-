# ==========================================================
#           WORLD UNIVERSITY RANKINGS ANALYSIS
# ==========================================================
# Project Title : WORLD UNIVERSITY RANKINGS - DATA CLEANING
#                  & ANALYSIS (2018-2019)
#
# Student Name : Your Name
# Batch        : Batch XXX
#
# Technology Used:
# • Python
# • Pandas
# • NumPy
#
# Dataset Name:
# eighteen_nineteen_university_datasets.csv
#
# Developed By:
# Your Name
#
# Description:
# This script cleans and analyzes the 2018-2019 world
# university rankings dataset. It handles messy headers,
# text placeholders ("-", "> 1000") in ranking columns,
# missing values, and duplicates, then generates useful
# analysis columns (performance category, rank buckets,
# top 10/50/100 flags) and summary statistics by country.
# Cleaned output is exported for use in a dashboard,
# to be built separately.
# ==========================================================

# STEP 1 - IMPORT LIBRARIES
import pandas as pd
import numpy as np


# STEP 2 - LOAD DATASET
df = pd.read_csv(
    "eighteen_nineteen_university_datasets.csv",
    encoding="latin1"
)


# STEP 3 - DISPLAY FIRST 5 ROWS
print("\n===== FIRST 5 ROWS =====")
print(df.head())


# STEP 4 - DISPLAY LAST 5 ROWS
print("\n===== LAST 5 ROWS =====")
print(df.tail())


# STEP 5 - CHECK NUMBER OF ROWS AND COLUMNS
print("\n===== DATASET SHAPE =====")
print(df.shape)


# STEP 6 - CHECK COLUMN NAMES
print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())


# STEP 7 - CHECK DATA TYPES
print("\n===== DATA TYPES =====")
print(df.dtypes)


# STEP 8 - DATASET INFORMATION
print("\n===== DATASET INFORMATION =====")
df.info()


# STEP 9 - STATISTICAL SUMMARY
print("\n===== STATISTICAL SUMMARY =====")
print(df.describe(include="all"))


# STEP 10 - CHECK MISSING VALUES
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# STEP 11 - CHECK MISSING VALUE PERCENTAGE
print("\n===== MISSING VALUE PERCENTAGE =====")
missing_percentage = (
    df.isnull().sum() / len(df) * 100
)

print(missing_percentage)


# STEP 12 - CHECK DUPLICATE RECORDS
print("\n===== DUPLICATE RECORDS =====")
print(df.duplicated().sum())


# STEP 13 - CHECK UNIQUE VALUES
print("\n===== UNIQUE VALUES =====")
print(df.nunique())


# STEP 14 - CHECK SAMPLE RECORDS
print("\n===== RANDOM SAMPLE =====")
print(df.sample(10))


# ============================================================
# DATA CLEANING
# ============================================================


# STEP 15 - MAKE A COPY OF ORIGINAL DATA
clean_df = df.copy()


# STEP 16 - CLEAN COLUMN NAMES
# NOTE: the raw file uses a non-breaking space (\xa0) inside
# "Quality of Education" and "Quality of Faculty" headers.
# This still needs to run BEFORE anything else touches columns.
clean_df.columns = (
    clean_df.columns
    .str.replace("\xa0", " ", regex=False)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)


# STEP 17 - DISPLAY CLEAN COLUMN NAMES
print("\n===== CLEAN COLUMN NAMES =====")
print(clean_df.columns.tolist())


# STEP 18 - CHECK COMPLETELY EMPTY ROWS
print("\n===== COMPLETELY EMPTY ROWS =====")
print(
    clean_df.isnull().all(axis=1).sum()
)


# STEP 19 - REMOVE COMPLETELY EMPTY ROWS
clean_df.dropna(
    how="all",
    inplace=True
)


# STEP 20 - CHECK DUPLICATES BEFORE REMOVING
print("\n===== DUPLICATES BEFORE REMOVING =====")
print(clean_df.duplicated().sum())


# STEP 21 - REMOVE DUPLICATES
clean_df.drop_duplicates(
    inplace=True
)


# STEP 22 - RESET INDEX
clean_df.reset_index(
    drop=True,
    inplace=True
)


# STEP 23 - DISPLAY TEXT COLUMNS
print("\n===== TEXT COLUMNS =====")

# NOTE: at this point almost every column is still text,
# because the ranking metrics contain "-" and "> 1000".
# We fix that further down before re-checking dtypes.
text_columns_raw = clean_df.select_dtypes(
    include=["object"]
).columns

print(text_columns_raw.tolist())


# STEP 24 - REMOVE EXTRA SPACES FROM TEXT
for column in text_columns_raw:
    clean_df[column] = (
        clean_df[column]
        .astype(str)
        .str.strip()
    )


# STEP 25 - CHECK UNIQUE LOCATIONS
# NOTE: "location" in this dataset is actually the country,
# not a city — kept the original column name for consistency.
print("\n===== LOCATIONS (COUNTRIES) =====")
print(
    clean_df["location"].unique()
)


# STEP 26 - CHECK NUMBER OF LOCATIONS
print("\n===== NUMBER OF LOCATIONS =====")
print(
    clean_df["location"].nunique()
)


# STEP 27 - CHECK INSTITUTION NAMES
print("\n===== SAMPLE INSTITUTIONS =====")
print(
    clean_df["institution"].head(20)
)


# STEP 28 - STANDARDIZE LOCATION VALUES
clean_df["location"] = (
    clean_df["location"]
    .str.strip()
    .str.upper()
)


# ============================================================
# NUMERIC DATA CLEANING
# ============================================================


# STEP 29 - DEFINE NUMERIC COLUMNS
numeric_columns = [
    "world_rank",
    "national_rank",
    "quality_of_education",
    "alumni_employment",
    "quality_of_faculty",
    "research_output",
    "quality_publications",
    "influence",
    "citations",
    "score"
]

# These specific rank columns use "> 1000" as a text placeholder
# meaning "ranked beyond 1000th place" rather than a missing value.
capped_rank_columns = [
    "quality_of_education",
    "alumni_employment",
    "quality_of_faculty",
    "research_output",
    "quality_publications",
    "influence",
    "citations",
]


# STEP 29b - REPLACE "> 1000" PLACEHOLDER WITH A REAL NUMBER
# We convert it to 1001 so it stays numerically worse than any
# real rank (1-1000), instead of collapsing into a missing value.
for column in capped_rank_columns:
    clean_df[column] = (
        clean_df[column]
        .astype(str)
        .str.strip()
        .replace("> 1000", "1001")
    )


# STEP 30 - CONVERT NUMERIC COLUMNS
# Any remaining non-numeric text (e.g. "-") becomes NaN here.
for column in numeric_columns:
    clean_df[column] = pd.to_numeric(
        clean_df[column],
        errors="coerce"
    )


# STEP 31 - CHECK NUMERIC DATA TYPES
print("\n===== NUMERIC DATA TYPES =====")
print(
    clean_df[numeric_columns].dtypes
)


# STEP 32 - CHECK MISSING NUMERIC VALUES
print("\n===== MISSING NUMERIC VALUES (AFTER '> 1000' FIX) =====")
print(
    clean_df[numeric_columns].isnull().sum()
)


# STEP 33 - CHECK MISSING TEXT VALUES
text_columns = clean_df.select_dtypes(
    include=["object"]
).columns

print("\n===== MISSING TEXT VALUES =====")
print(
    clean_df[text_columns].isnull().sum()
)


# ============================================================
# MISSING VALUE HANDLING
# ============================================================


# STEP 34 - FILL MISSING TEXT VALUES
for column in text_columns:
    clean_df[column] = (
        clean_df[column]
        .fillna("Unknown")
    )


# STEP 35 - FILL MISSING NUMERIC VALUES
# The remaining NaNs in the capped_rank_columns come from "-",
# which (like "> 1000") signals the university did not place
# in that metric's ranking — so we fill with 1001 (worst rank),
# NOT the column median, to avoid implying average performance.
for column in capped_rank_columns:
    if clean_df[column].isnull().sum() > 0:
        clean_df[column] = clean_df[column].fillna(1001)

# For any other genuinely numeric columns (world_rank, national_rank,
# score) that still have gaps, median fill is reasonable since those
# don't use text placeholders.
other_numeric_columns = [
    col for col in numeric_columns
    if col not in capped_rank_columns
]

for column in other_numeric_columns:
    if clean_df[column].isnull().sum() > 0:
        median_value = clean_df[column].median()
        clean_df[column] = clean_df[column].fillna(median_value)


# STEP 36 - CHECK MISSING VALUES AFTER CLEANING
print("\n===== MISSING VALUES AFTER CLEANING =====")
print(
    clean_df.isnull().sum()
)


# ============================================================
# DATA VALIDATION
# ============================================================


# STEP 37 - CHECK WORLD RANK
print("\n===== WORLD RANK CHECK =====")

print(
    clean_df["world_rank"].describe()
)


# STEP 38 - CHECK NATIONAL RANK
print("\n===== NATIONAL RANK CHECK =====")

print(
    clean_df["national_rank"].describe()
)


# STEP 39 - CHECK SCORE
print("\n===== SCORE CHECK =====")

print(
    clean_df["score"].describe()
)


# STEP 40 - CHECK INVALID SCORE VALUES
print("\n===== INVALID SCORE VALUES =====")

invalid_scores = clean_df[
    (clean_df["score"] < 0) |
    (clean_df["score"] > 100)
]

print(invalid_scores)


# STEP 41 - CHECK INVALID WORLD RANK
print("\n===== INVALID WORLD RANK =====")

invalid_world_rank = clean_df[
    clean_df["world_rank"] <= 0
]

print(invalid_world_rank)


# STEP 42 - CHECK INVALID NATIONAL RANK
print("\n===== INVALID NATIONAL RANK =====")

invalid_national_rank = clean_df[
    clean_df["national_rank"] <= 0
]

print(invalid_national_rank)


# ============================================================
# CREATE USEFUL ANALYSIS COLUMNS
# ============================================================


# STEP 43 - CREATE PERFORMANCE CATEGORY

def performance_category(score):

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Very Good"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Below Average"


clean_df["performance_category"] = (
    clean_df["score"]
    .apply(performance_category)
)


# STEP 44 - CREATE TOP 10 CATEGORY
clean_df["top_10"] = np.where(
    clean_df["world_rank"] <= 10,
    "Top 10",
    "Outside Top 10"
)


# STEP 45 - CREATE TOP 50 CATEGORY
clean_df["top_50"] = np.where(
    clean_df["world_rank"] <= 50,
    "Top 50",
    "Outside Top 50"
)


# STEP 46 - CREATE TOP 100 CATEGORY
clean_df["top_100"] = np.where(
    clean_df["world_rank"] <= 100,
    "Top 100",
    "Outside Top 100"
)


# STEP 47 - CREATE RANK CATEGORY

def rank_category(rank):

    if rank <= 10:
        return "1-10"

    elif rank <= 50:
        return "11-50"

    elif rank <= 100:
        return "51-100"

    elif rank <= 500:
        return "101-500"

    else:
        return "501+"


clean_df["rank_category"] = (
    clean_df["world_rank"]
    .apply(rank_category)
)


# ============================================================
# FINAL CHECKS
# ============================================================


# STEP 48 - FINAL SHAPE
print("\n===== FINAL DATASET SHAPE =====")
print(clean_df.shape)


# STEP 49 - FINAL COLUMN NAMES
print("\n===== FINAL COLUMNS =====")
print(clean_df.columns.tolist())


# STEP 50 - FINAL DATA TYPES
print("\n===== FINAL DATA TYPES =====")
print(clean_df.dtypes)


# STEP 51 - FINAL MISSING VALUES
print("\n===== FINAL MISSING VALUES =====")
print(
    clean_df.isnull().sum()
)


# STEP 52 - FINAL DUPLICATES
print("\n===== FINAL DUPLICATES =====")
print(
    clean_df.duplicated().sum()
)


# STEP 53 - FINAL DATA PREVIEW
print("\n===== CLEANED DATA =====")
print(
    clean_df.head(10)
)


# STEP 54 - FINAL STATISTICS
print("\n===== FINAL STATISTICS =====")
print(
    clean_df.describe()
)


# ============================================================
# BASIC ANALYSIS
# ============================================================


# STEP 55 - TOP 10 UNIVERSITIES
print("\n===== TOP 10 UNIVERSITIES =====")

top_10 = (
    clean_df
    .sort_values("world_rank")
    .head(10)
)

print(
    top_10[
        [
            "world_rank",
            "institution",
            "location",
            "score"
        ]
    ]
)


# STEP 56 - TOP 10 COUNTRIES BY UNIVERSITY COUNT
print(
    "\n===== TOP COUNTRIES ====="
)

country_count = (
    clean_df["location"]
    .value_counts()
    .head(10)
)

print(country_count)


# STEP 57 - AVERAGE SCORE BY COUNTRY
print(
    "\n===== AVERAGE SCORE BY COUNTRY ====="
)

country_score = (
    clean_df
    .groupby("location")["score"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print(country_score)


# STEP 58 - HIGHEST SCORE
print(
    "\n===== HIGHEST SCORE ====="
)

print(
    clean_df["score"].max()
)


# STEP 59 - LOWEST SCORE
print(
    "\n===== LOWEST SCORE ====="
)

print(
    clean_df["score"].min()
)


# STEP 60 - AVERAGE SCORE
print(
    "\n===== AVERAGE SCORE ====="
)

print(
    clean_df["score"].mean()
)


# STEP 61 - BEST UNIVERSITY
print(
    "\n===== BEST UNIVERSITY ====="
)

best_university = (
    clean_df
    .sort_values("world_rank")
    .iloc[0]
)

print(
    best_university[
        [
            "institution",
            "location",
            "world_rank",
            "score"
        ]
    ]
)


# STEP 62 - SAVE CLEANED DATA
clean_df.to_csv(
    "cleaned_university_dataset.csv",
    index=False
)


# STEP 63 - CONFIRM FILE
print(
    "\nCleaned dataset saved successfully."
)


# ============================================================
# END OF CLEANING
# Dashboard will be created separately.
# ============================================================