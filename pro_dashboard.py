import streamlit as st
import json
import pandas as pd

FILE_NAME = "bank_data.json"

st.set_page_config(page_title="Bank Dashboard")

# Load Data
def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return {}

data = load_data()

# Login UI
st.sidebar.title("🔐 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if username in data and data[username]["password"] == password:
        st.session_state["user"] = username
        st.success("Login Successful!")
    else:
        st.error("Invalid Username or Password")

# After Login
if "user" in st.session_state:
    user = st.session_state["user"]
    st.title(f"🏦 Welcome {user}")

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

        st.subheader("📊 Summary")
        st.write("Total:", df["Amount"].sum())
        st.write("Deposit:", df[df["Type"]=="Deposited"]["Amount"].sum())
        st.write("Withdraw:", df[df["Type"]=="Withdrawn"]["Amount"].sum())

        st.bar_chart(df.groupby("Type")["Amount"].sum())

    else:
        st.info("No transactions found!")

else:
    st.title("🔐 Please Login First")