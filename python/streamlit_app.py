import streamlit as st
import pandas as pd
import os
from datetime import date

# ----- CONFIG -----
TOTAL_STUDENTS = 500
DATA_FILE = "meal_data.csv"

# ----- SETUP -----
# Create file if not exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "count"])
    df.to_csv(DATA_FILE, index=False)

# Load existing data
df = pd.read_csv(DATA_FILE)

st.title("🍽️ Hostel Meal Tracker")
st.write("Students must confirm dinner before **4 PM**.")

today = str(date.today())

# Check today's count
today_row = df[df["date"] == today]

if len(today_row) > 0:
    today_count = int(today_row["count"].values[0])
else:
    today_count = 0

# ----- STUDENT BUTTON -----
if st.button("I'm Eating Tonight"):
    today_count += 1

    # update CSV
    if len(today_row) > 0:
        df.loc[df["date"] == today, "count"] = today_count
    else:
        df.loc[len(df)] = [today, today_count]

    df.to_csv(DATA_FILE, index=False)
    st.success("Response recorded! Enjoy your meal 😄")

st.subheader("👨‍🍳 Cook's Dashboard")
st.metric("Total Students Eating Tonight", today_count)

food_saved = TOTAL_STUDENTS - today_count
st.metric("Estimated Food Saved", f"{food_saved} servings")

# ----- GRAPH -----
st.subheader("📉 Food Saved Over Time")

if not df.empty:
    df["food_saved"] = TOTAL_STUDENTS - df["count"]
    st.line_chart(df.set_index("date")["food_saved"])
else:
    st.info("No data yet.")



