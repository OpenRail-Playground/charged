import streamlit as st
import plotly.express as px


def render():
    # Add radio button to select visualization type
    visualization_type = st.radio(
        "Visualization type:", options=["by vehicle", "by errors"], horizontal=True
    )

    # Prepare data
    df = st.session_state["shared_df"]
    df["min_5"] = df["TIMESTAMP_VEHICLE"].dt.floor("5min")
    df["size"] = 15

    # Create the appropriate visualization based on the selected option
    if visualization_type == "by errors":
        color = "ERRORS"
    else:
        color = "VEHICLE_ID"

    fig = px.scatter_map(
        df.drop_duplicates(subset=["min_5", "VEHICLE_ID"]),
        lon="VEHICLE_GPS_X",
        lat="VEHICLE_GPS_Y",
        color=color,
        size="size",
        width=1200,
        height=600,
        zoom=9,
        hover_data=["VEHICLE_GPS_SPEED", "BATTERY_SOC"],
        labels={"min_5": "Min 5", "VEHICLE_ID": "Vehicle Id", "ERRORS": "Errors"},
        # map_style="dark",
        map_style="carto-darkmatter",
        # map_style="open-street-map",
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    st.plotly_chart(fig, use_container_width=True)
