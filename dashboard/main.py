import streamlit as st
from tabs import tab1, tab2

def main():
    st.set_page_config(page_title="Hello World Streamlit App", layout="wide")
    st.title("Hello World Streamlit App")
    tabs = st.tabs(["Tab 1", "Tab 2"])
    with tabs[0]:
        tab1.render()
    with tabs[1]:
        tab2.render()

if __name__ == "__main__":
    main()
