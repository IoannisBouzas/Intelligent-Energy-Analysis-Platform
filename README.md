# Intelligent-Energy-Analysis-Platform

A comprehensive AI-powered platform for energy data analysis, market insights, and forecasting with specialized focus on the Greek energy market.

## Overview

This project is part of my summer Intership(2025) at CERTH where i had the chance to built an intelligent assistant that combines multiple specialized tools to provide comprehensive energy analysis capabilities. Built with a modular architecture, it offers data analysis, time-series forecasting, live price monitoring, news analysis, and bill processing in one integrated platform.

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

### AI Models & APIs Used

- **Mistral AI**: Primary LLM for orchestration and analysis
- **Codestral**: Specialized code generation for data analysis
- **Chronos Bolt**: Time-series forecasting
- **Mistral OCR**: Bill document processing
- **Tavily API**: News search and content extraction

## Installation

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

## Usage

### Starting the Application

```bash
streamlit run ui.py
```

Navigate to `http://localhost:8501` to access the web interface.

### Core Workflows

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

## Configuration


### Model Optimization

- Use quantized models for production deployment
- Implement batch processing for multiple forecasts
- Cache frequently accessed price data

## Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-tool`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make changes and test thoroughly
5. Submit pull request with detailed description

### Adding New Tools

1. Create tool class inheriting from base structure
2. Implement `get_tool_schema()` method
3. Add tool integration to `MainAgent`
4. Update UI components as needed
5. Add comprehensive tests


## Support

For issues, questions, or contributions:

- **Issues**: GitHub Issues tracker
- **Documentation**: See `/docs` folder
- **Community**: GitHub Discussions

## Changelog

### Version 1.0.0
- Initial release with core functionality
- Data analysis, forecasting, and price monitoring tools
- Greek market specialization
- Streamlit web interface

### Roadmap

- [ ] Multi-language support
- [ ] Advanced forecasting models
- [ ] Historical price analysis
- [ ] Mobile-responsive interface
- [ ] API endpoint development
- [ ] Database integration for data persistence

---

**Intelligent-Energy-Analysis-Platform** - Transforming energy data into actionable insights with the power of AI.
