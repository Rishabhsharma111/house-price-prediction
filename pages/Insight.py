import streamlit as st
import pandas as pd

st.title("📊 Insights")

df = pd.read_csv("data/train.csv")

st.write("### Dataset Preview")
st.dataframe(df.head())

st.write("### Basic Statistics")
st.write(df.describe())