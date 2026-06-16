import streamlit as st
import pandas as pd
import google.generativeai as genai

# ---------------------------------------------------
# Personal Finance AI Advisor
# Tracks expenses, predicts spending patterns, and delivers
# AI-generated personalized financial recommendations
# ---------------------------------------------------

st.set_page_config(page_title="Personal Finance AI Advisor", page_icon="💰", layout="centered")

st.title("💰 Personal Finance AI Advisor")
st.write("Upload your expense data and get AI-powered insights, spending patterns, and personalized financial recommendations.")

# ---------------- API KEY ----------------
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")
else:
    st.warning("Please enter your Gemini API key in the sidebar to use this app.")
    st.stop()

st.sidebar.divider()
st.sidebar.subheader("📄 CSV Format Required")
st.sidebar.write("Your CSV must have these columns:")
st.sidebar.code("Date, Category, Amount, Description")
st.sidebar.write("Example:")
st.sidebar.code("2025-01-05, Food, 450, Lunch at cafe")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload your expenses CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip().capitalize() for c in df.columns]

        required_cols = {"Date", "Category", "Amount", "Description"}
        if not required_cols.issubset(set(df.columns)):
            st.error(f"CSV must contain these columns: {', '.join(required_cols)}")
            st.stop()

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df = df.dropna(subset=["Date", "Amount"])

        st.success(f"Loaded {len(df)} transactions successfully!")

        # ---------------- SUMMARY METRICS ----------------
        st.divider()
        st.subheader("📊 Expense Summary")

        total_spent = df["Amount"].sum()
        avg_transaction = df["Amount"].mean()
        top_category = df.groupby("Category")["Amount"].sum().idxmax()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"₹{total_spent:,.2f}")
        col2.metric("Avg Transaction", f"₹{avg_transaction:,.2f}")
        col3.metric("Top Category", top_category)

        # ---------------- CATEGORY BREAKDOWN ----------------
        st.divider()
        st.subheader("📁 Spending by Category")
        category_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(category_summary)

        # ---------------- MONTHLY TREND ----------------
        st.divider()
        st.subheader("📈 Monthly Spending Trend")
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        monthly_summary = df.groupby("Month")["Amount"].sum()
        st.line_chart(monthly_summary)

        # ---------------- RAW DATA ----------------
        with st.expander("View Raw Transaction Data"):
            st.dataframe(df)

        # ---------------- AI ANALYSIS ----------------
        st.divider()
        st.subheader("🤖 AI-Powered Insights")

        if st.button("Generate Financial Recommendations"):
            with st.spinner("Analyzing your spending patterns..."):
                category_text = category_summary.to_string()
                monthly_text = monthly_summary.to_string()

                prompt = f"""You are an expert personal financial advisor.

Here is a user's spending summary by category:
{category_text}

Here is their monthly spending trend:
{monthly_text}

Total spent: ₹{total_spent:,.2f}
Average transaction size: ₹{avg_transaction:,.2f}
Number of transactions: {len(df)}

Based on this data:
1. Identify the top 2-3 spending patterns or concerns
2. Predict how their spending might trend next month if habits continue
3. Give 4-5 specific, actionable personalized recommendations to save money or budget better

Keep the tone friendly and practical. Use clear headings and bullet points."""

                response = model.generate_content(prompt)
                st.markdown(response.text)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("👆 Upload a CSV file to get started. Use the sidebar for the required format.")
