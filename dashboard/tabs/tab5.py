def render():
    import streamlit as st

    # st.header("Tab 1")
    st.write("This is the content of Tab 1.")
    st.dataframe(st.session_state["shared_df"])
