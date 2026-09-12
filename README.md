# 🛒 Walmart Forecasting AI

An AI-powered Walmart sales analysis and forecasting application that combines **time-series forecasting, machine learning tools, and a Gemini-powered AI assistant**.

The application allows users to ask natural-language questions about Walmart sales, analyze historical performance, compare stores, and generate future sales forecasts through an interactive Streamlit interface.
## 🚀 Key Features

- 🤖 **AI-Powered Assistant** — Ask questions about Walmart sales using natural language.
- 📊 **Historical Sales Analysis** — Calculate total and average sales for individual stores and recent periods.
- 🏪 **Store Comparison** — Compare the sales performance of two Walmart stores.
- 🔮 **Sales Forecasting** — Predict future weekly sales using a SARIMA time-series model.
- 📈 **Forecast Analysis** — Calculate average or total predicted sales from forecasts.
- 📉 **Interactive Visualizations** — Display forecasts and sales comparisons through Streamlit charts.
- 🧠 **Gemini Function Calling** — The AI assistant selects the appropriate backend tool based on the user's question.
- 🔐 **API Key Protection** — Sensitive API credentials are kept outside the repository using environment configuration.

## 🏗️ System Architecture

The application follows a tool-based AI architecture where the Gemini AI assistant interprets the user's request and selects the appropriate backend operation.


                    User
                      │
                      ▼
             Streamlit Application
                      │
                      ▼
              Gemini AI Assistant
                      │
              Function Calling
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
 Historical       Store          Forecasting
 Sales Tools    Comparison         Tool
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                Walmart Dataset
                      │
                      ▼
               Analysis / Forecast
                      │
                      ▼
              AI-generated Response
                      │
                      ▼
             Streamlit Interface '''

## 🛠️ Technology Stack

### Programming & Data
- **Python**
- **Pandas**
- **NumPy**

### Machine Learning & Forecasting
- **Statsmodels**
- **SARIMA / SARIMAX**
- **Time-Series Analysis**

### Generative AI
- **Google Gemini API**
- **Gemini Function Calling**
- **Tool-based AI Architecture**

### Application
- **Streamlit**

### Development & Version Control
- **Git**
- **GitHub**
- **GitHub Desktop**

## 📁 Project Structure


Walmart-forecasting-AI/
│
├── AI_tools/
│   ├── __init__.py
│   └── tools.py
│
├── Application/
│   ├── __init__.py
│   └── app.py
│
├── DATA/
│   └── Walmart.csv
│
├── Forecasting/
│   ├── __init__.py
│   └── forecasting.py
│
├── LLM/
│   ├── __init__.py
│   └── gemini_agent.py
│
├── .gitignore
├── test.py
└── README.md

## ⚙️ How It Works

The application processes user questions through an AI-driven tool-selection workflow.

### 1. User Input

The user enters a natural-language question through the Streamlit interface.

Example:

> "What is the average sale for Store 7 over the last 10 weeks?"

### 2. AI Understanding

The Gemini-powered assistant analyzes the question and determines what operation is required.

For example:

- Historical average → historical sales tool
- Historical total → total sales tool
- Store comparison → comparison tool
- Future prediction → forecasting tool

### 3. Tool Execution

The selected backend tool processes the Walmart dataset and returns the required result.

### 4. Forecasting

For future sales questions, the application uses a **SARIMA/SARIMAX** time-series model to generate weekly sales forecasts.

### 5. AI Response

The tool result is returned to the Gemini assistant, which converts the result into a natural-language response for the user.

### 6. Visualization

When enabled, the Streamlit interface can display relevant charts such as:

- Sales forecasts
- Average sales comparisons
- Total sales comparisons

## 💬 Example Queries

The AI assistant supports natural-language questions such as:

### Historical And Forecasting Analysis

What is the total sale for Store 5?
what is the average sale for store 7 iver the last 10 weeks?

Compare store 5and store 20
forecast the next  5 weeks for store 9.
what will be the total predicted sales for Store 10 over the next 12 weeks?

## 🚀 Setup & Installation

### 1. Clone the Repository


git clone https://github.com/sriharig110-lang/Walmart-forecasting-AI.git
cd Walmart-forecasting-AI

## 🔮 Future Improvements

The project is designed to be extended into a more complete AI-powered analytics platform.

Planned improvements include:

- 📊 Add more interactive sales visualizations.
- 📈 Add historical sales trend analysis.
- 🔮 Combine historical sales and forecast results in a single visualization.
- 🏪 Add advanced multi-store comparison capabilities.
- 🧠 Improve AI tool selection and error handling.
- 🧪 Add comprehensive automated tests.
- ⚡ Separate model training from forecast inference for better performance.
- ☁️ Deploy the application to a cloud platform.
- 🔄 Add MLOps practices for model monitoring and updates.
- 🤖 Extend the system toward a more autonomous AI analytics agent.

## 👨‍💻 Author

**Sri Hari**

AI/ML Engineer in progress, focused on building practical machine learning, generative AI, and AI-agent systems.

GitHub: [@sriharig110-lang](https://github.com/sriharig110-lang)