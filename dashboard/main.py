import streamlit as st
from tabs import tab1, tab2, tab3, tab4, tab5
from load_data import load_data
from datetime import datetime, timedelta


def main():
    st.set_page_config(page_title="Charged", layout="wide")
    st.title("Charged - Battery Monitoring")

    # Create date selector with default values (today and 7 days ago)
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=7)

    # Function to update shared dataframe when date changes
    def update_filtered_dataframe():
        if len(st.session_state.date_range) == 2:
            start_date, end_date = st.session_state.date_range
            df = load_data(start_date=start_date, end_date=end_date)        
            st.session_state["shared_df"] = df
    
    # Create two columns for date picker and tabs
    date_col, _ = st.columns([1, 3])

    with date_col:
        st.date_input(
            "Select Date Range", 
            value=(default_start, default_end), 
            key="date_range",
            on_change=update_filtered_dataframe
        )
    
    # Initialize shared dataframe in session state if not present
    if "shared_df" not in st.session_state:
        update_filtered_dataframe()
    tabs = st.tabs(["Overview", "Map", "Time Series", "Errors", "Capacity"])
    mapping = {
        "Overview": "KPI overview",
        "Map": "Map",
        "TimeSeries": "Time Series",
        "Errors": "Errors",
        "Capacity": "Capacity",
    }
    with tabs[0]:
        st.subheader(mapping["Overview"])
        tab1.render()
    with tabs[1]:
        st.subheader(mapping["Map"])
        tab2.render()
    with tabs[2]:
        st.subheader(mapping["TimeSeries"])
        tab3.render()
    with tabs[3]:
        st.subheader(mapping["Errors"])
        tab4.render()
    with tabs[4]:
        st.subheader(mapping["Capacity"])
        tab5.render()


if __name__ == "__main__":
    main()
