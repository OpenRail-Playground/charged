import streamlit as st
from tabs import tab1, tab2
from load_data import load_data


def main():
    st.set_page_config(page_title="Charged", layout="wide")
    st.title("Hello World Streamlit App")
    # Initialize shared dataframe in session state if not present
    if "shared_df" not in st.session_state:
        st.session_state["shared_df"] = load_data()
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
        tab2.render()
    with tabs[3]:
        st.subheader(mapping["Errors"])
        tab2.render()
    with tabs[4]:
        st.subheader(mapping["Capacity"])
        tab2.render()


if __name__ == "__main__":
    main()
