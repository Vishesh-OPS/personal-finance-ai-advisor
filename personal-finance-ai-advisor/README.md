# 💰 Personal Finance AI Advisor

An AI-powered personal finance tool that tracks expenses from uploaded CSV data, visualizes spending patterns, and delivers personalized financial recommendations using LLMs.

## Features
- Upload expense data via CSV
- Automatic spending summary (total, average, top category)
- Category-wise and monthly spending visualizations
- AI-generated insights: spending patterns, predicted trends, and personalized recommendations
- End-to-end LLM integration with real user data workflows

## Tech Stack
- Python
- Pandas (data processing)
- Google Gemini API (LLM)
- Streamlit (frontend)

## How to Run Locally

1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/personal-finance-ai-advisor.git
cd personal-finance-ai-advisor
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
streamlit run app.py
```

4. Enter your Gemini API key in the sidebar, then upload a CSV file with columns: `Date, Category, Amount, Description`

## How It Works
1. Upload your expense CSV file
2. View automatic summary metrics and charts (by category and by month)
3. Click "Generate Financial Recommendations"
4. Get AI-powered analysis of your spending patterns and personalized advice
