import streamlit as st
import json
import pandas as pd

FILE_NAME = "bank_data.json"

st.set_page_config(page_title="Bank Dashboard", layout="centered")

st.title("🏦 Banking Data Analysis Dashboard")

# Load Data
def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return {}

data = load_data()

if not data:
    st.warning("No data found! Run banking system first.")
else:
    user = st.selectbox("Select User", list(data.keys()))
    history = data[user]["history"]

    amounts = []
    types = []

    for h in history:
        parts = h.split()
        types.append(parts[0])
        amounts.append(int(parts[1]))

    if amounts:
        df = pd.DataFrame({
            "Type": types,
            "Amount": amounts
        })

        total = df["Amount"].sum()
        deposit = df[df["Type"]=="Deposited"]["Amount"].sum()
        withdraw = df[df["Type"]=="Withdrawn"]["Amount"].sum()

        st.subheader("📊 Summary")
        st.write("Total:", total)
        st.write("Deposit:", deposit)
        st.write("Withdraw:", withdraw)

        st.subheader("📈 Bar Chart")
        st.bar_chart(df.groupby("Type")["Amount"].sum())

        st.subheader("🥧 Pie Chart")
        pie_data = df.groupby("Type")["Amount"].sum()
        st.pyplot(pie_data.plot.pie(autopct='%1.1f%%').figure)

    else:
        st.info("No transactions yet!")