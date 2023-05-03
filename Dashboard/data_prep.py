import numpy as np
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="2022 Forbes Billionaires Analysis",
    page_icon="random",
    layout="wide",
    menu_items={'Get Help': "mailto:regansomi@gmail.com"},
    initial_sidebar_state="collapsed"
)
df = pd.read_csv("./forbes_billionaires_2022.csv")


@st.cache_data
def clean_data(data):
    """Takes in the billionaires dataframes and returns a clean dataframe ready for analysis"""
    # Let's just replace rows with zero in the Age column with NaN
    data["Age"] = data["Age"].apply(lambda x: np.nan if x == 0 else x)
    # Clean up the Networth column and convert it to a numeric data type
    data["Networth"] = data["Networth"].apply(lambda x: float(x.split(" ")[0].replace("$", "").strip()))
    return data


clean_df = clean_data(df)


# GROUPs the data by country then count the number of billionaires for each.
countries = clean_df.groupby("Country").size().reset_index(name="Number of Billionaires")\
    .sort_values(by="Number of Billionaires", ascending=False)
countries.reset_index(drop=True, inplace=True)

# Select Female Billionaires
female = clean_df[clean_df["Gender"] == "F"]
category_female = female.groupby("Industries").size().reset_index(name="count").sort_values(by="count", ascending=False)
category_female.reset_index(drop=True, inplace=True)
category_female = category_female.iloc[:10, :]

female_by_country = female.groupby("Country").size().reset_index(name="Female Billionaires")\
    .sort_values(by="Female Billionaires", ascending=False)
female_by_country.reset_index(drop=True, inplace=True)
female_by_country["Percentage"] = round((female_by_country["Female Billionaires"] /
                                         female_by_country["Female Billionaires"].sum()) * 100, 1)


# Combine the countries and females by country dataframes
combined = countries.merge(female_by_country, on="Country", how="left")
combined.fillna(value=0, inplace=True)
combined.isnull().sum()


# Industry with the highest number of Billionaires
categories = clean_df.groupby("Industries").size().reset_index(name="count").sort_values(by="count", ascending=False)
categories.reset_index(drop=True, inplace=True)
top_10_categories = categories.head(10)


@st.cache_data
def aggregate_countries(row):
    if row["Number of Billionaires"] < 112:
        return "Other"
    else:
        return row["Country"]


# Aggregate countries with most billionaires
countries_agg = countries.copy()
countries_agg["Country"] = countries_agg.apply(aggregate_countries, axis=1)
countries_agg = countries_agg.groupby("Country")["Number of Billionaires"].sum().reset_index()
countries_agg = countries_agg.iloc[[4, 0, 2, 1, 3], :].reset_index(drop=True)
countries_agg["Percentage"] = round((countries_agg["Number of Billionaires"] / countries_agg["Number of Billionaires"]
                                     .sum()) * 100, 1)
countries_agg["Percentage"] = countries_agg["Percentage"].apply(lambda x: f"{x}%")


# FEMALE vs MALE BILLIONAIRES
by_gender = clean_df.groupby("Gender").size().reset_index(name="count")
by_gender["Gender"] = by_gender["Gender"].map({"F": "Female", "M": "Male"})
