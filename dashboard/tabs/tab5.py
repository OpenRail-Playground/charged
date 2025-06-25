import streamlit as st
import plotly.graph_objects as go


def load_capacity(df):
    df_result = df.drop_duplicates(subset=["VEHICLE_ID"], keep="last")
    df_result["AVAILABLE"] = df_result["BATTERY_SOC"] * 1.056

    df_result = df_result.reset_index()[["VEHICLE_ID", "AVAILABLE"]]

    df_result.columns = {
        "Vehicle ID": df_result["VEHICLE_ID"],
        "Available energy [kWh]": df_result["AVAILABLE"],
    }
    return df_result


def sum_capacity(df):
    return df["Available energy [kWh]"].sum()


def render():
    # load data for capacity overview
    df_capacity = load_capacity(st.session_state["shared_df"])
    df_overall_capacitiy = sum_capacity(df_capacity)

    fig = go.Figure(
        go.Indicator(
            mode="number+gauge",
            value=df_overall_capacitiy,
            gauge={"axis": {"visible": False}},
            domain={"row": 0, "column": 0},
            title="Available fleet energy [kWh]",
        )
    )

    # Show plot
    st.plotly_chart(fig, use_container_width=True)

    # Show table
    st.write(df_capacity)
