# Intelligent-Energy-Analysis-Platform

A comprehensive AI-powered platform for energy data analysis, market insights, and forecasting with specialized focus on the Greek energy market.

## Overview

This project is part of my summer Intership (2025) at CERTH,Greece where i had the chance to built an intelligent assistant that combines multiple specialized tools to provide comprehensive energy analysis capabilities. Built with a modular architecture, it offers data analysis, time-series forecasting, live price monitoring, news analysis, and bill processing in one integrated platform.

## Landing Page

https://agentic-energy-platform.lovable.app/

## Try it online here 

https://energy-analysis-platform.streamlit.app/

## <img width="32" height="32" alt="image" src="https://github.com/user-attachments/assets/e49f0b01-8d7c-44f1-9963-2bea07fbd4b3" /> Important Notice
- Because we use the free tier apis that Mistral provides we have a daily limit, use the app wisely
- Bigger models like Mistral-Medium that we use for news have even more smaller daily limit and it is slow
so do not worry if the app's response is slow. News tool has a hard job so be patient !!
- Also Tavily has a limit for web search which is currently at 1000 apis calls
- Of course you will find bugs, it is a proof of concept and NOT a production ready tool


## Key Features

### 🔍 **Multi-Tool Intelligence**
- **Data Analysis Tool**: Advanced statistical analysis and visualization of energy datasets
- **Forecasting Tool**: Time-series prediction using state-of-the-art Chronos models
- **Live Price Tool**: Real-time Greek energy market price scraping and comparison
- **News Analysis Tool**: Greek energy news aggregation and insight generation
- **Bill Analysis Tool**: OCR-based electricity bill processing and analysis (not yet intergraded)

### 📊 **Interactive Dashboard**
- Streamlit-based web interface with real-time data visualization
- Conversational AI chat interface for natural language queries
- Dynamic provider comparison carousel
- Integrated plotting and statistical outputs

### 🇬🇷 **Greek Energy Market Specialization**
- Live scraping from Greek energy price comparison sites
- Greek news source integration with domain-specific analysis
- Support for Greek electricity bill formats
- Market-specific insights and recommendations

## Architecture

### System Workflow

[![](https://mermaid.ink/img/pako:eNqNVV1v2jAU_SuWp73RigQS0jxMClAoXWlpoe1W0wc3uYDVEEe26cqq_vfdOOFrnbQGyeT6HJ_r-2HnjcYyARrSueL5gkza04zgE7FbDYoMsnxlHsnR0TfSZmOjgC9TYcjt4LGktS3UYUMuMhLNITPkSsUL0EZxI1XFKseO5Xbfrleg1iTKeLrWQr-XYNeCp2wiZUrGkEJshMwO1p9aSo91ueHb5aRY8LhP6LOeVBBzbT5iZ-xCvAAZKRHDR3TALuHXPxTPWVuk6T9dlmPP0r6zoSjiTkkHM2rfHvfxC1bMkz5kgMnZRXdh0SGmF2e1ETHf-aooQ0u5xDSbPJUmFU9khP_6YBd9S7pinYWSmdSkLVNDhuhys40rSxixiVgC5lgJ0JgKSMR-rkeWdL1L4p3QK56K3_xDQc4s9YbdwxMZx9g-IptXhBsLjdmzSOVL0Qn8eL7phrHFJqysQkcuc66E3mpPLHyLsapnMNiBWswXf4U6sJw7NuEvIsVeGm368c4C96yvAJ6JLedYrlQMm_X3lvADS5GZoltPX7FO-_H_sISfZSv8VYZyPLeMh221rzo3Ff5gkShio24PMyvRrd7lJIpKuF22k23jD-7L8bJkdtgN6FxmGjANBuYHbXNdcUrr9sD6eWBF7QOzmiyPY9RlPYFRko2nzWbLA9neP-bRaXkpdIXOU77e7vjrV4JXg8zmiMWYV1W0zQsojZudZtqsUywzmWHQ4Zd63Xfq9RpmTj5DYTaTrXn0SyRmEbr5ay2WqVThl5l9Nhq9SsNNit-eRvF8UqNfaTRjPvN2-3ChlTTcT2qcVRqz2UmwFwvM_PjT-xhUGnDigN_YavDEaXqtT2qcVxrBU9xo8q2G5wVP7uy_GrSGV75IaGjUCmp0CWrJC5O-FXWdUrOAJUxpiK8JHsUpnWbvuCbn2YOUy80yJVfzBQ1nPNVorfKEG-gKjq263M4qyBJQHbnKDA2dIGhYFRq-0Vcatrzjhh8064Hjt1zH8Zs1uqbhkecdN_0WNkvQ8lz_JHDea_S39escO_WTlu8FblB3Gy0H00XxDsM7Zlh-yOz37P0Pjbwb_A?type=png)](https://mermaid.live/edit#pako:eNqNVV1v2jAU_SuWp73RigQS0jxMClAoXWlpoe1W0wc3uYDVEEe26cqq_vfdOOFrnbQGyeT6HJ_r-2HnjcYyARrSueL5gkza04zgE7FbDYoMsnxlHsnR0TfSZmOjgC9TYcjt4LGktS3UYUMuMhLNITPkSsUL0EZxI1XFKseO5Xbfrleg1iTKeLrWQr-XYNeCp2wiZUrGkEJshMwO1p9aSo91ueHb5aRY8LhP6LOeVBBzbT5iZ-xCvAAZKRHDR3TALuHXPxTPWVuk6T9dlmPP0r6zoSjiTkkHM2rfHvfxC1bMkz5kgMnZRXdh0SGmF2e1ETHf-aooQ0u5xDSbPJUmFU9khP_6YBd9S7pinYWSmdSkLVNDhuhys40rSxixiVgC5lgJ0JgKSMR-rkeWdL1L4p3QK56K3_xDQc4s9YbdwxMZx9g-IptXhBsLjdmzSOVL0Qn8eL7phrHFJqysQkcuc66E3mpPLHyLsapnMNiBWswXf4U6sJw7NuEvIsVeGm368c4C96yvAJ6JLedYrlQMm_X3lvADS5GZoltPX7FO-_H_sISfZSv8VYZyPLeMh221rzo3Ff5gkShio24PMyvRrd7lJIpKuF22k23jD-7L8bJkdtgN6FxmGjANBuYHbXNdcUrr9sD6eWBF7QOzmiyPY9RlPYFRko2nzWbLA9neP-bRaXkpdIXOU77e7vjrV4JXg8zmiMWYV1W0zQsojZudZtqsUywzmWHQ4Zd63Xfq9RpmTj5DYTaTrXn0SyRmEbr5ay2WqVThl5l9Nhq9SsNNit-eRvF8UqNfaTRjPvN2-3ChlTTcT2qcVRqz2UmwFwvM_PjT-xhUGnDigN_YavDEaXqtT2qcVxrBU9xo8q2G5wVP7uy_GrSGV75IaGjUCmp0CWrJC5O-FXWdUrOAJUxpiK8JHsUpnWbvuCbn2YOUy80yJVfzBQ1nPNVorfKEG-gKjq263M4qyBJQHbnKDA2dIGhYFRq-0Vcatrzjhh8064Hjt1zH8Zs1uqbhkecdN_0WNkvQ8lz_JHDea_S39escO_WTlu8FblB3Gy0H00XxDsM7Zlh-yOz37P0Pjbwb_A)


### Core Components

```
Intelligent-Energy-Analysis-Platform/
├── main_agent.py          # Orchestrator agent coordinating all tools
├── ui.py                  # Streamlit user interface
└── tools/
    ├── data_analysis_tool.py    # Statistical analysis and visualization
    ├── forecast_tool.py         # Time-series forecasting with Chronos
    ├── live_price_tool.py       # Greek energy price scraping
    ├── news_tool.py            # Greek news analysis
    └── bill_analysis_tool.py    # OCR bill processing
```

### AI Models & APIs Used for Tools

- **Main Agent**: Devstral-Medium-2507 which excels at using tools
- **Data Analysis Tool**: Codestral-2501 for code generation at 0.7 temp
- **Live Price Tool**: Ministral-8b-2410 for analysis
- **Forecast Tool**: Chronos Bolt Small 
- **Bill Analysis Tool**: Mistral OCR + Ministral-8b-2410 for analysis
- **News Tool**: Tabliy API for news search + Mistral-Medium for comprehensive analysis

## Installation for local use

### Prerequisites

- Python 3.12+
- CUDA-compatible GPU (recommended for Chronos forecasting)

### Clone repo
```bash
git clone https://github.com/your-username/Intelligent-Energy-Analysis-Platform.git
cd CircuitImageAi
```

### Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with required API keys:

```bash
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Starting the Application 

```bash
streamlit run ui.py
```

Navigate to `http://localhost:8501` to access the web interface.




## Core Workflows

#### 1. Data Analysis
- Upload CSV/Excel energy datasets
- Ask natural language questions about your data
- Receive automated analysis with visualizations and insights

#### 2. Energy Price Monitoring
- Click "Load Live Prices" in sidebar for real-time Greek energy rates
- Ask comparative questions like "Which provider has the cheapest rates?"
- Get detailed market analysis and savings calculations

#### 3. Time-Series Forecasting
- Upload time-series energy data
- Request predictions: "Forecast energy consumption for next 24 hours"
- Receive probabilistic forecasts with confidence intervals

#### 4. News Analysis
- Query Greek energy news: "Latest news about renewable energy in Greece"
- Get summarized insights from multiple Greek news sources
- Receive market intelligence and trend analysis

### Example Queries

**Data Analysis:**
- "Show me the correlation between temperature and energy consumption"
- "Create a monthly trend analysis of electricity usage"
- "What are the peak consumption hours in my dataset?"

**Price Comparison:**
- "Which energy provider offers the best rates for high consumption?"
- "Compare all providers for usage under 2000 kWh"
- "Show me potential annual savings by switching providers"

**Forecasting:**
- "Predict energy demand for the next week"
- "Forecast solar generation for tomorrow"
- "What will be the consumption trend for next month?"

**News Intelligence:**
- "Latest developments in Greek energy policy"
- "Recent news about electricity prices in Greece"
- "Updates on renewable energy projects"

## Technical Details

### Data Processing Pipeline

1. **Data Ingestion**: Automatic CSV/Excel parsing with intelligent column detection
2. **Analysis Generation**: LLM-powered Python code generation for statistical analysis
3. **Execution Environment**: Secure code execution with captured outputs
4. **Visualization**: Automatic matplotlib/seaborn plot generation
5. **Result Integration**: Seamless integration of text, code, and visual outputs

### Forecasting Engine

- **Model**: Amazon Chronos-Bolt (small) for efficient inference
- **Quantile Predictions**: Probabilistic forecasts with uncertainty bounds
- **Visualization**: Automatic historical context and prediction plotting
- **Scalability**: Handles various time-series frequencies and lengths

### Price Intelligence System

- **Web Scraping**: Real-time data extraction from Greek energy comparison sites
- **Data Structuring**: Automated provider and contract information parsing
- **Analysis Engine**: LLM-powered market intelligence and recommendations
- **Update Frequency**: Real-time data refresh capabilities

### News Tool

- **Extracting News**: Based on the user's query the tool uses tavily to search at greek news providers to find the best suited articles
- **Articles Summary**: We use a LLM with big context window in order to do the summary and provide the user with the best articles



## Future Vision

### This was my first time dealing with agents and agentic systems so many things can be improved like:
- [ ] Better context history management
- [ ] Better prompting for the LLMs
- [ ] More tools 
- [ ] Better communication between the tools
- [ ] And many more

### The problem of agentic architectures in energy analysis is still open and every can contribute, feel free to provide better insights about this solution

---

**Intelligent-Energy-Analysis-Platform** - Transforming energy data into actionable insights with the power of AI.
