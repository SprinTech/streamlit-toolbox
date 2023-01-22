import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

trees_df = pd.read_csv("trees.csv")
trees_df["age"] = (pd.to_datetime("today") - pd.to_datetime(trees_df["date"])).dt.days

owners = st.sidebar.multiselect("Tree Owner Filter", trees_df["caretaker"].unique())

st.title("SF Trees")
st.write("This app analyses trees in San Francisco using dataset from SF DPW")

graph_color = st.sidebar.color_picker("Graph Colors")

if owners:
    trees_df = trees_df[trees_df["caretaker"].isin(owners)]

df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ["tree_count"]

col1, col2 = st.columns(2)

with col1:
    st.write("Trees by Width")
    fig1, ax1 = plt.subplots()
    ax1 = sns.histplot(trees_df["dbh"], color=graph_color)
    plt.xlabel("Trees Width")
    st.pyplot(fig1)

with col2:
    st.write("Trees by age")
    fig2, ax2 = plt.subplots()
    ax2 = sns.histplot(trees_df["age"], color=graph_color)
    plt.xlabel("Age (Days)")
    st.pyplot(fig2)

st.write("Trees by Location")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.sample(n=1000, replace=True)
st.map(trees_df)
