# 🛒 Walmart Forecasting AI

An AI-powered Walmart sales analysis and forecasting application that combines time-series forecasting, tool-based AI, and an interactive Streamlit interface.

## 🚀 Features

- 🤖 Natural-language Walmart sales assistant powered by Gemini function calling
- 📊 Historical average and total sales analysis
- 🏪 Store-to-store sales comparison
- 🔮 SARIMA/SARIMAX weekly sales forecasting
- 📈 Forecast average/total analysis
- 📉 Streamlit visualizations
- 🔐 API credentials kept outside source control
- 🧪 Automated unit tests and GitHub Actions CI

## 🏗️ Architecture

```text
User
  ↓
Streamlit Application
  ↓
Gemini AI Assistant
  ↓
Tool Registry / Dispatcher
  ↓
Analysis Tools ─────→ Forecasting Layer
  ↓                         ↓
Walmart Dataset ←───────────┘
  ↓
Structured Tool Results
  ↓
Gemini Final Response
  ↓
Streamlit Interface / Visualizations
```

The AI layer is responsible for understanding the request and selecting tools. Business logic remains in Python functions so it can be tested independently of the LLM.

## 🛠️ Technology Stack

- Python
- Pandas / NumPy
- Statsmodels (SARIMA/SARIMAX)
- Google Gemini API
- Streamlit
- pytest
- Git / GitHub / GitHub Actions

## 📁 Project Structure

```text
Walmart-forecasting-AI/
├── AI_tools/
│   ├── __init__.py
│   └── tools.py
├── Application/
│   ├── __init__.py
│   └── app.py
├── DATA/
│   └── walmart.csv
├── Forecasting/
│   ├── __init__.py
│   └── forecasting.py
├── LLM/
│   ├── __init__.py
│   └── gemini_agent.py
├── Visualization/
│   ├── __init__.py
│   └── visualizations.py
├── tests/
│   └── test_tools.py
├── .github/workflows/tests.yml
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Setup

```bash
git clone https://github.com/sriharig110-lang/Walmart-forecasting-AI.git
cd Walmart-forecasting-AI
pip install -r requirements.txt
```

Create `api.env` in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run Application/app.py
```

Run tests:

```bash
pytest -q
```

The GitHub Actions workflow runs the same test suite automatically on pushes and pull requests.

## 💬 Example Queries

- What is the total sale for Store 5?
- What is the average sale for Store 7 over the last 10 weeks?
- Forecast the next 5 weeks for Store 7.
- Compare Store 5 and Store 20.
- What is the total predicted sales for Store 10 over the next 12 weeks?
- Show historical sales for Store 7.

## 🔒 Production-readiness Decisions

- Dataset paths are resolved relative to the project root instead of a developer-specific Windows path.
- Tool arguments are validated before business logic executes.
- Unknown tools and malformed arguments return controlled errors.
- The agent has a maximum of five tool-calling iterations to prevent runaway loops.
- Gemini configuration is loaded from environment variables.
- Tool/business logic is covered by automated tests.
- CI runs tests on every push and pull request.

## 🔮 Next Improvements

- Add deterministic integration tests for the Gemini tool-calling loop.
- Add structured application logging and request tracing.
- Separate model training/evaluation from forecast inference and add model monitoring.
- Add containerization and cloud deployment.

## 👨‍💻 Author

**Sri Hari**

AI/ML Engineer in progress, focused on practical machine learning, generative AI, and AI-agent systems.

GitHub: [@sriharig110-lang](https://github.com/sriharig110-lang)
