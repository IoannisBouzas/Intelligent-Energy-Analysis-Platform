import json
import streamlit as st
import pandas as pd
from mistralai import Mistral


from tools.news_tool import GreekNewsTool
from tools.live_price_tool import LivePriceTool
from tools.data_analysis_tool import DataAnalysisTool, execute_code
from tools.forecast_tool import ChronosForecaster


class MainAgent:
    """Main agent that orchestrates data analysis and forecasting"""

    def __init__(self, mistral_api_key):
        self.client = Mistral(api_key=mistral_api_key)
        self.data_analysis_tool = DataAnalysisTool(self.client)
        self.forecaster = ChronosForecaster()
        self.live_price_tool = LivePriceTool(self.client)
        # self.bill_analysis_tool = BillAnalysisTool(self.client)
        self.greek_news_tool = GreekNewsTool(self.client)

        # Available tools for the agent
        self.tools = [
            self.data_analysis_tool.get_tool_schema(),
            self.forecaster.get_tool_schema(),
            self.live_price_tool.get_tool_schema(),
            # self.bill_analysis_tool.get_tool_schema()
            self.greek_news_tool.get_tool_schema(),
        ]

    async def analyze_query(self, query, df, conversation_history=None):
        """Main method that decides which tool to use based on query"""
        global data_summary, tool_result_content, result

        if conversation_history is None:
            conversation_history = []

        if df is None:
            data_summary = None
        else:
            data_summary = get_data_summary(df)

        system_prompt = """
        You are an intelligent orchestrator agent that coordinates specialized tools to provide comprehensive responses to user queries.

        Your role is to:
        1. **Analyze the user's request** and identify which specialized tool(s) are most appropriate
        2. **Delegate tasks** to the appropriate tools with correct parameters
        3. **Synthesize and interpret** the results from tools into coherent, actionable insights
        4. **Provide additional context** and expert interpretation when beneficial

        AVAILABLE TOOLS:
        - data_analysis_tool: For statistical analysis, data exploration, and visualizations of uploaded datasets
        - forecast_tool: For time-series forecasting using uploaded data
        - live_price_tool: For real-time Greek energy market price analysis and comparisons
        - greek_news_tool: For finding and summarizing current Greek news articles on any topic

        ORCHESTRATION PROCESS:
        1. **Tool Selection**: Choose the most relevant tool(s) based on the user's query
        2. **Parameter Extraction**: Extract or infer the necessary parameters from context
        3. **Result Integration**: When tools return results, IF need it provide your own analysis and insights
        4. **Value Addition**: Add domain expertise, context, or recommendations beyond what tools provide

        PARAMETER HANDLING:
        - For time-based forecasts: Convert user timeframes to appropriate units (days→hours, etc.)
        - For data analysis: Use column names and data characteristics from the dataset summary
        - For news searches: Use the user's exact query terms and infer relevant focus areas
        - Always validate parameters before tool execution

        You add value through interpretation, context, and recommendations - not by replacing specialized tool capabilities.
        """

        # Build messages with conversation history
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history if exists
        messages.extend(conversation_history)

        # Add current user query
        if not conversation_history:  # First message in conversation
            messages.append({
                "role": "user",
                "content": f"Dataset: {data_summary}\n\nUser Query: {query}"
            })
        else:  # Continuation of conversation
            messages.append({"role": "user", "content": query})

        response = await self.client.chat.complete_async(
            model="devstral-medium-2507",
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            parallel_tool_calls=True
        )

        # Handle tool calls
        if response.choices[0].message.tool_calls:
            # Add assistant's tool call message to conversation
            messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": response.choices[0].message.tool_calls
            })

            tool_results = []
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments

                if tool_name == "data_analysis_tool":
                    result = await self._handle_data_analysis(tool_args, df)
                    if result['error']:
                        tool_result_content += f"\nError: {result['error']}"
                    else:
                        tool_result_content = f"Analysis completed. Code: {result['code']}\nOutput: {result['output']}"

                elif tool_name == "forecast_tool":
                    result = await self._handle_forecasting(tool_args, df)
                    tool_result_content = f"Forecast completed: {result['result']}"

                elif tool_name == "live_price_tool":
                    result = await self._handle_live_prices(tool_args)
                    if not result['result']['status']:
                        tool_result_content += f"\nError: {result['error']}"
                    else:
                        tool_result_content = f"Live energy prices analysis: {result['result']['insights']}"

                elif tool_name == "greek_news_tool":
                    result = await self._handle_greek_news(tool_args)
                    if not result['result']['success']:
                        tool_result_content += f"\nError: {result['result']['error']}"
                    else:
                        tool_result_content = f"Greek news analysis completed: {result['result']['analysis']}"


                # Add tool result message
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result_content
                })

                tool_results.append(result)



            # Get LLM response to tool results
            final_response = await self.client.chat.complete_async(
                model="devstral-medium-2507",
                messages=messages
            )

            # Add final assistant response to conversation
            messages.append({
                "role": "assistant",
                "content": final_response.choices[0].message.content
            })

            return {
                "type": "tool_with_response",
                "tool_results": tool_results,
                "llm_response": final_response.choices[0].message.content,
                "conversation_history": messages[1:]  # Exclude system message
            }

        # No tool calls - direct response
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

        return {
            "type": "direct_response",
            "response": response.choices[0].message.content,
            "conversation_history": messages[1:]  # Exclude system message
        }

    async def _handle_data_analysis(self, args, df):
        """Handle data analysis tool execution"""
        args = json.loads(args)

        query = args.get("user_query", "")
        data_summary = args.get("data_summary", get_data_summary(df))

        # Generate and execute code
        code = await self.data_analysis_tool.generate_code(query, data_summary)
        output, figures, error = execute_code(code, df)

        return {
            "type": "analysis",
            "code": code,
            "output": output,
            "figures": figures,
            "error": error
        }

    async def _handle_forecasting(self, args, df):
        """Handle forecasting tool execution"""

        args = json.loads(args)

        column_name = args.get("column_name")

        series = df[column_name].dropna()

        length = args.get("prediction_length")


        forecast_result = await self.forecaster.forecast(
            series=series,
            prediction_length=length)

        return {
            "type": "forecast",
            "result": {
                "median_forecast": forecast_result["median_forecast"],
                "low_quantile": forecast_result["low_quantile"],
                "high_quantile": forecast_result["high_quantile"],
                "forecast_index": forecast_result["forecast_index"],
                "figure": forecast_result["figure"]
            }
        }

    async def _handle_live_prices(self, args):
        """Handle live prices tool execution"""

        args = json.loads(args)
        query = args.get("user_query", "")

        result = await self.live_price_tool.execute(query)

        return {
            "type": "live_prices",
            "result": result
        }

    async def _handle_greek_news(self, args):
        """Handle Greek news tool execution"""
        args = json.loads(args)
        query = args.get("query", "")

        result = await self.greek_news_tool.execute(query)

        return {
            "type": "greek_news",
            "result": result
        }



def display_energy_providers_carousel(energy_data):
    """Display energy providers in a carousel format with toggle"""
    # Add toggle button
    show_providers = st.toggle("Show Energy Providers", value=False, key="providers_toggle")

    if not show_providers:
        return

    if not energy_data:
        st.warning("No energy data available")
        return

    st.subheader("🔌 Live Energy Providers")

    provider_names = list(energy_data.keys())

    if len(provider_names) > 0:
        selected_provider = st.selectbox(
            "Select Energy Provider:",
            provider_names,
            key="provider_carousel"
        )

        if selected_provider in energy_data:
            provider_contracts = energy_data[selected_provider]
            st.markdown(f"### {selected_provider}")

            if provider_contracts:
                for i, contract in enumerate(provider_contracts):
                    with st.expander(f"🔋 {contract['name']}", expanded=(i == 0)):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Under 2000 kWh",
                                contract['price_under_2000'] or "N/A",
                                help="Price for consumption under 2000 kWh"
                            )

                        with col2:
                            st.metric(
                                "Over 2000 kWh",
                                contract['price_over_2000'] or "N/A",
                                help="Price for consumption over 2000 kWh"
                            )
            else:
                st.info("No contracts available for this provider")

def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            if 'Timestamp_UTC' in df.columns:
                df['Timestamp_UTC'] = pd.to_datetime(df['Timestamp_UTC'], errors='coerce')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def get_data_summary(df):
    """Generate comprehensive dataset summary"""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()

    summary = f"""
            Dataset Summary:
            - Shape: {df.shape[0]} rows, {df.shape[1]} columns
            - Numeric columns: {numeric_cols}
            - Categorical columns: {categorical_cols}
            - DateTime columns: {datetime_cols}
            - Missing values: {df.isnull().sum().to_dict()}
            - Sample data: {df.head(10).to_dict()}
            """

    return summary

