import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("🧠 Habit Breakpoint Analyzer")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("habitdata.csv")

df = load_data()

# Habit Selection
habit = st.selectbox("Select Habit", df["habit"].unique())

habit_df = df[df["habit"] == habit]
habit_df["date"] = pd.to_datetime(habit_df["date"])

# Completion Stats
completed = habit_df[habit_df["completed"] == "Yes"].shape[0]
missed = habit_df[habit_df["completed"] == "No"].shape[0]

st.metric("Completed Days", completed)
st.metric("Missed Days", missed)

# Breakpoint Detection
st.subheader("🚨 Habit Breakpoints")

breakpoints = habit_df[habit_df["completed"] == "No"]
st.write(breakpoints[["date", "reason"]])

# Failure Reason Analysis
st.subheader("📉 Failure Reasons")

reason_counts = breakpoints["reason"].value_counts()

fig, ax = plt.subplots()
reason_counts.plot(kind="bar", ax=ax)
ax.set_ylabel("Count")
ax.set_title("Failure Reasons")

st.pyplot(fig)

# Day-wise Risk Analysis
st.subheader("📅 Risk Days")

habit_df["day"] = habit_df["date"].dt.day_name()
risk_days = habit_df[habit_df["completed"] == "No"]["day"].value_counts()

st.bar_chart(risk_days)
