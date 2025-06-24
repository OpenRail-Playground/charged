def render():
    import streamlit as st
    import pandas as pd

    sdf: pd.DataFrame = st.session_state["shared_df"]

    filtered_df = sdf[sdf["ERROR_SIZE"] > 0]
    grouped_df = (
        filtered_df.groupby(["VEHICLE_ID", "DATE"]).size().reset_index(name="count")
    )
    ordered_df = grouped_df.sort_values(
        by=["VEHICLE_ID", "DATE"], ascending=[True, True]
    )

    st.bar_chart(
        ordered_df, x="DATE", y="count", x_label="Number of Errors", y_label="Date"
    )

    st.write(ordered_df)
