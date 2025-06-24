"""Battery dashboard."""

from typing import Dict
from datetime import date, timedelta
import snowflake.snowpark.functions as F
import pandas as pd
import plotly.express as px
import streamlit as st
from charged.snowflake_utils import create_session


# Config
table = "BATTERIELOK_DATA"
columns = [
    "VEHICLE_OUTSIDE_TEMP",
    "BATTERY_SOC",
    "BATTERY_SOH",
    "BATTERY_COOLING_TEMP",
    "BATTERY_1_TEMP",
    "BATTERY_1_VOLTAGE",
    "BATTERY_1_CURRENT",
    "BATTERY_2_TEMP",
    "BATTERY_2_VOLTAGE",
    "BATTERY_2_CURRENT",
    "BATTERY_3_TEMP",
    "BATTERY_3_VOLTAGE",
    "BATTERY_3_CURRENT",
    "BATTERY_4_TEMP",
    "BATTERY_4_VOLTAGE",
    "BATTERY_4_CURRENT",
    "BATTERY_5_VOLTAGE",
]


# Functions
def set_page_config():
    st.set_page_config(
        page_title="Charged",
        layout="wide",
    )
    st.sidebar.title("Charged")

    # Display info
    st.sidebar.write("""Battery monitoring and management""")


# Timeseries tab #########################3
@st.cache_data()
def load_timeseries_data(date_range: Dict) -> pd.DataFrame:
    """Filter raw table."""
    _session = create_session()

    # prepare for aggregation
    aggregations = []
    for column in columns:
        aggregations.append(F.avg(F.col(column)).alias(f"{column}_AVG"))

    sdf = (
        _session.table(table)
        .filter(F.to_date(F.col("TIMESTAMP_VEHICLE")) >= date_range["date_from"])
        .filter(F.to_date(F.col("TIMESTAMP_VEHICLE")) <= date_range["date_to"])
        .filter(F.col("VEHICLE_ID").isNotNull())
        .with_column(
            "TIMESTAMP_TRUNC",
            F.from_unixtime(
                F.round(F.unix_timestamp(F.col("TIMESTAMP_VEHICLE")) / 60) * 60
            ).cast("TIMESTAMP"),
        )
        .group_by(["VEHICLE_ID", "TIMESTAMP_TRUNC"])
        .agg(*aggregations)
        .order_by(["VEHICLE_ID", "TIMESTAMP_TRUNC"], ascending=[True, True])
    )
    return sdf.to_pandas()


def render_timeseries(df, parameter):
    """Render time series plot per vehicle."""
    fig = px.line(
        df,
        x="TIMESTAMP_TRUNC",
        y=f"{parameter}_AVG",
        markers=True,
        facet_row="VEHICLE_ID",
        render_mode="svg",
    )
    # free scale on y axis
    fig.update_yaxes(matches=None, showticklabels=True)

    # Show plot
    st.plotly_chart(fig, use_container_width=True)


# Maps tab ########################
@st.cache_data()
def load_map_data():
    pass


def render_map():
    pass


# Overview tab ###################
@st.cache_data()
def load_overview_data(date_range: Dict):
    """Filter raw table."""
    _session = create_session()

    # prepare for aggregation
    aggregations = []
    for column in columns:
        aggregations.append(F.avg(F.col(column)).alias(f"{column}_AVG"))

    # get pandas dataframe
    df = (
        _session.table(table)
        .filter(F.to_date(F.col("TIMESTAMP_VEHICLE")) >= date_range["date_from"])
        .filter(F.to_date(F.col("TIMESTAMP_VEHICLE")) <= date_range["date_to"])
        .filter(F.col("VEHICLE_ID").isNotNull())
        .with_column(
            "TIMESTAMP_TRUNC",
            F.from_unixtime(
                F.round(F.unix_timestamp(F.col("TIMESTAMP_VEHICLE")) / 60) * 60
            ).cast("TIMESTAMP"),
        )
        .with_column(
            "DATE",
            F.date_trunc("DAY", "TIMESTAMP_VEHICLE").cast("DATE"),
        )
        .with_column("ERROR_SIZE", F.size(F.col("ERRORS")))
        .to_pandas()
    )

    # pandas df for
    # Assuming `df` is your Pandas DataFrame equivalent to `sdf`
    df_result = (
        df.groupby("VEHICLE_ID")
        .agg(BATTERY_SOH_AVG=("BATTERY_SOH", "mean"), ERROR_COUNT=("ERROR_SIZE", "sum"))
        .assign(
            ERROR_STATE=lambda x: x["ERROR_COUNT"].apply(
                lambda count: 1 if count > 0 else 0
            ),
            SOH_STATE=lambda x: x["BATTERY_SOH_AVG"].apply(
                lambda soh: 0 if soh > 95 else (0.5 if soh > 50 else 0)
            ),
        )
    )

    df_result["KPI"] = df_result["ERROR_STATE"] + df_result["SOH_STATE"]

    df_result = df_result.sort_values("KPI", ascending=False)

    return df_result.reset_index()[
        ["VEHICLE_ID", "KPI", "BATTERY_SOH_AVG", "ERROR_COUNT"]
    ]


# def color_row(row):
# if row['KPI'] > 1:
#     return ['background-color: red'] * len(row)
# elif row['KPI'] < 0.5:
#     return ['background-color: green'] * len(row)
# else:
#     return ['background-color: orange'] * len(row)


def color_value(val):
    if val > 1:
        return "background-color: red"
    elif val < 0.5:
        return "background-color: green"
    else:
        return "background-color: orange"


def render_overview(df):
    # st.write(df.style.apply(color_value, subset=['KPI'], axis=1))
    st.write(df.style.applymap(color_value, subset=["KPI"]))


# Error tab ###################
@st.cache_data()
def load_error_data():
    pass


def render_error():
    pass


# Main ###
def main():
    """Main function to build the Streamlit dashboard"""
    # Set page configuration and title
    set_page_config()

    # Get parameters. Default date range: current day.
    date_range = {
        "date_from": st.sidebar.date_input("From", date.today() - timedelta(days=7)),
        "date_to": st.sidebar.date_input("To", date.today()),
    }

    # setup tabs
    tab_ts, tab_overview, tab_map, tab_error = st.tabs(
        ["Time Series", "Overview", "Map", "Errors"]
    )

    # Check validity of date range
    if date_range["date_from"] > date_range["date_to"]:
        st.error("The 'From' date cannot be greater than the 'To' date.")
    else:
        with tab_ts:
            # parameter dropdown
            parameter = st.selectbox(
                "Metrics",
                columns,
            )
            # load raw data as Pandas DF
            df = load_timeseries_data(date_range)
            # display time series
            render_timeseries(df, parameter)
        with tab_map:
            df = load_map_data()
            render_map()
        with tab_overview:
            df = load_overview_data(date_range)
            render_overview(df)
        with tab_error:
            df = load_error_data()
            render_error()


if __name__ == "__main__":
    main()
