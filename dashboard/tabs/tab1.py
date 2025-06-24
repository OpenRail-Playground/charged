import streamlit as st


def load_kpi(df):
    df_result = (
        df.groupby("VEHICLE_ID")
        .agg(BATTERY_SOH_AVG=("BATTERY_SOH", "mean"), ERROR_COUNT=("ERROR_SIZE", "sum"))
        .assign(
            ERROR_STATE=lambda x: x["ERROR_COUNT"].apply(
                lambda count: 1 if count > 0 else 0
            ),
            SOH_STATE=lambda x: x["BATTERY_SOH_AVG"].apply(
                lambda soh: 0 if soh > 95 else (0.5 if soh > 50 else 0)
            ),
        )
    )
    df_result["KPI"] = df_result["ERROR_STATE"] + df_result["SOH_STATE"]
    df_result = df_result.sort_values("KPI", ascending=False)

    return df_result.reset_index()[
        ["VEHICLE_ID", "KPI", "BATTERY_SOH_AVG", "ERROR_COUNT"]
    ]


def color_value(val):
    if val > 1:
        return "background-color: red"
    elif val < 0.5:
        return "background-color: green"
    else:
        return "background-color: orange"


def render():
    # load data for kpi overview
    df_kpi = load_kpi(st.session_state["shared_df"])
    st.write(df_kpi.style.applymap(color_value, subset=["KPI"]))
