import streamlit as st
import plotly.express as px
import pandas as pd


def render():
    sdf: pd.DataFrame = st.session_state["shared_df"]

    dfn = sdf[["VEHICLE_ID", "ERROR_SIZE", "TIMESTAMP_VEHICLE"]]
    # Create a new column with just the date component (without time)
    dfn["DATE"] = dfn["TIMESTAMP_VEHICLE"].dt.date

    # Group by DATE and VEHICLE_ID, summing the ERROR_SIZE
    daily_errors = dfn.groupby(["DATE", "VEHICLE_ID"])["ERROR_SIZE"].sum().reset_index()

    # Convert DATE back to datetime for proper plotting
    daily_errors["DATE"] = pd.to_datetime(daily_errors["DATE"])
    # Create bar chart showing daily error sizes by vehicle
    fig = px.bar(
        daily_errors,
        y="ERROR_SIZE",
        x="DATE",
        color="VEHICLE_ID",
        barmode="stack",
        title="Daily Aggregated Error Size by Vehicle",
        labels={"VEHICLE_ID": "Vehicle Id", "ERROR_SIZE": "Error Size", "DATE": "Date"},
    )
    st.plotly_chart(fig, use_container_width=True)
