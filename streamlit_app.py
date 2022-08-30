import streamlit as st
import pandas as pd

st.cache(persist=True, show_spinner=True)
def load_world_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url) 


if __name__ == "__main__":
    world_df = load_world_data("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

    sub_df = world_df[["date", "total_deaths", "new_deaths", "total_vaccinations", "new_vaccinations"]].dropna()

    dates = sorted(sub_df.date.unique().tolist())    
    start_date, end_date = st.select_slider("Date:", options=dates, value=(dates[0], dates[-1]))

    # Apply slider range
    # greater than the start date and smaller than the end date
    # mask = (sub_df['date'] > pd.to_datetime(start_date)) & (sub_df['date'] <= pd.to_datetime(end_date))
    mask = (sub_df['date'] > start_date) & (sub_df['date'] <= end_date)

    sub_df = sub_df.loc[mask]

    # Get the year and month
    sub_df["year_month"] = sub_df['date'].str.slice(0, 7)
    sub_df = sub_df.groupby(by="year_month").sum()

    col1, col2 = st.columns(2)

    with col1:
        st.line_chart(sub_df[["new_deaths"]])
        st.line_chart(sub_df[["new_vaccinations"]])
    
    with col2:
        first_nd = int(sub_df.new_deaths.iloc[0])
        last_nd = int(sub_df.new_deaths.iloc[-1])
        nd_diff = int(((last_nd - first_nd) / first_nd) * 100)
        st.metric("Death Count for the last month", value=last_nd, delta=f"{nd_diff}%", delta_color="inverse")
