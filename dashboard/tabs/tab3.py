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
        "BATTERY_5_VOLTAGE",
    ]


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
        "Metrics",
        get_columns(),
    )

    df_ts = load_ts(st.session_state["shared_df"])

    fig = px.line(
        df_ts,
        x="TIMESTAMP_TRUNC",
        y=parameter,
        markers=True,
        facet_row="VEHICLE_ID",
        render_mode="svg",
    )
    # free scale on y axis
    fig.update_yaxes(matches=None, showticklabels=True)

    # Show plot
    st.plotly_chart(fig, use_container_width=True)
