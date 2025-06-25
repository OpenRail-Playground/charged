import streamlit as st
import plotly.graph_objects as go


def load_capacity(df):
    df_result = (
        df.groupby("VEHICLE_ID")
        .agg(BATTERY_SOH_AVG=("BATTERY_SOH", "mean"), SOC=("BATTERY_SOC", "mean"))
        .assign(
            CAPACITY=lambda x: x["BATTERY_SOH_AVG"].apply(lambda soh: soh * 1.056),
        )
    )
    df_result["AVAILABLE"] = df_result["SOC"] * df_result["CAPACITY"] / 100

    df_result = df_result.reset_index()[["VEHICLE_ID", "CAPACITY", "SOC", "AVAILABLE"]]

    df_result.columns = {
        "Vehicle ID": df_result["VEHICLE_ID"],
        "Capacity": df_result["CAPACITY"],
        "SOC": df_result["SOC"],
        "Available": df_result["AVAILABLE"],
    }
    return df_result


def render():
    # load data for capacity overview
    df_capacity = load_capacity(st.session_state["shared_df"])
    st.write(df_capacity)

    fig = go.Figure(
        go.Indicator(
            mode="number+delta+gauge",
            value=433,
            delta={"reference": 431},
            gauge={"axis": {"visible": False}},
            domain={"row": 0, "column": 0},
        )
    )

    # Show plot
    st.plotly_chart(fig, use_container_width=True)
