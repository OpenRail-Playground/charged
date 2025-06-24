import streamlit as st
import plotly.express as px


def render():
    df = st.session_state["shared_df"]
    df["min_5"] = df["TIMESTAMP_VEHICLE"].dt.floor("5min")
    df["size"] = 15
    fig = px.scatter_map(
        df.drop_duplicates(subset=["min_5", "VEHICLE_ID"]),
        lon="VEHICLE_GPS_X",
        lat="VEHICLE_GPS_Y",
        color="VEHICLE_ID",
        size="size",
        width=1200,
        height=600,
        zoom=9,
        # hover_data=["xxx", "yyy"],
        # map_style="dark",
        map_style="carto-darkmatter",
        # map_style="open-street-map",
    )
    st.plotly_chart(fig, use_container_width=True)
