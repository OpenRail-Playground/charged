import streamlit as st
import pandas as pd
from tabs import tab1, tab2
from load_data import load_data

def main():
    st.set_page_config(page_title="Hello World Streamlit App", layout="wide")
    st.title("Hello World Streamlit App")
    # Initialize shared dataframe in session state if not present
    if "shared_df" not in st.session_state:
        st.session_state["shared_df"] = load_data()
    tabs = st.tabs(["Tab 1", "Tab 2"])
    with tabs[0]:
        st.subheader("Tab 1: Full DataFrame")
        st.dataframe(st.session_state["shared_df"])
        tab1.render()
    with tabs[1]:
        st.subheader("Tab 2: First 2 Rows of DataFrame")
        st.dataframe(st.session_state["shared_df"].head(2))
        tab2.render()

if __name__ == "__main__":
    main()
