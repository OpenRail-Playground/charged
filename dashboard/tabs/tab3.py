import streamlit as st
import plotly.express as px


def get_columns():
    return [
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
    ]


def get_labels():
    return {
        "VEHICLE_OUTSIDE_TEMP": "Vehicle outside temperature [°C]",
        "TIMESTAMP_TRUNC": "Date",
        "ERRORS": "Errors",
        "BATTERY_SOC": "Battery SOC [%]",
        "BATTERY_SOH": "Battery SOH [%]",
        "BATTERY_COOLING_TEMP": "Battery cooling liquid temperature [°C]",
        "VEHICLE_ID": "Vehicle Id",
        "BATTERY_1_TEMP": "Battery 1 temperature [°C]",
        "BATTERY_1_VOLTAGE": "Battery 1 voltage [V]",
        "BATTERY_1_CURRENT": "Battery 1 current [A]",
        "BATTERY_2_TEMP": "Battery 2 temperature [°C]",
        "BATTERY_2_VOLTAGE": "Battery 2 voltage [V]",
        "BATTERY_2_CURRENT": "Battery 2 current [A]",
        "BATTERY_3_TEMP": "Battery 3 temperature [°C]",
        "BATTERY_3_VOLTAGE": "Battery 3 voltage [V]",
        "BATTERY_3_CURRENT": "Battery 3 current [A]",
        "BATTERY_4_TEMP": "Battery 4 temperature [°C]",
        "BATTERY_4_VOLTAGE": "Battery 4 voltage [V]",
        "BATTERY_4_CURRENT": "Battery 4 current [A]",
    }


def load_ts(df):
    columns = get_columns()
    aggregations = {f"{column}": "mean" for column in columns}

    df_grouped = df.groupby(["VEHICLE_ID", "TIMESTAMP_TRUNC"]).agg(aggregations)

    # Order the DataFrame by 'VEHICLE_ID' and 'TIMESTAMP_TRUNC'
    df_ordered = df_grouped.sort_values(
        by=["VEHICLE_ID", "TIMESTAMP_TRUNC"], ascending=[True, True]
    )

    # Display the first few rows of the resulting DataFrame
    return df_ordered.reset_index()


def render():
    # parameter dropdown
    parameter = st.selectbox(
        "Metrics", get_columns(), format_func=lambda x: f"{get_labels()[x]}"
    )

    df_ts = load_ts(st.session_state["shared_df"])

    fig = px.line(
        df_ts,
        x="TIMESTAMP_TRUNC",
        y=parameter,
        markers=True,
        color="VEHICLE_ID",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        render_mode="svg",
        labels=get_labels(),
    )

    # Show plot
    st.plotly_chart(fig, use_container_width=True)
