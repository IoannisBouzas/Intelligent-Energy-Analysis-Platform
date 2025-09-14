import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import io
import sys


def execute_code(code, df):
    """Execute code and capture outputs"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    plt.switch_backend('Agg')

    exec_globals = {
        'df': df, 'pd': pd, 'np': np, 'plt': plt,
        'sns': sns, 'datetime': datetime, 'print': print
    }

    try:
        exec(code, exec_globals)
        output = captured_output.getvalue()
        figures = [plt.figure(i) for i in plt.get_fignums()]
        return output, figures, None
    except Exception as e:
        return None, [], str(e)
    finally:
        sys.stdout = old_stdout


def _clean_code(code):
    """Clean generated code by removing markdown blocks"""
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
    return code.strip()


class DataAnalysisTool():
    """Tool for generating and executing data analysis code"""

    def __init__(self, mistral_client):
        self.client = mistral_client
        self.name = "data_analysis_tool"
        self.description = "Generate and execute Python code for data analysis tasks including statistics, visualizations, and data exploration"

    def get_tool_schema(self):
        """Tool schema for Mistral function calling"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "The user's data analysis question or request"
                        },
                        "data_summary": {
                            "type": "string",
                            "description": "Summary of the dataset structure and contents"
                        }
                    },
                    "required": ["user_query", "data_summary"]
                }
            }
        }

    async def generate_code(self, user_query, data_summary):
        """Generate analysis code using Codestral"""

        prompt = f"""

                You are a Python data analysis expert in energy field. Generate code to analyze data in a meaningful way and answer the user's query.
                We want the user to be able to understand many things from the analysis
                Make graphs that are meaningful for the user and present them nicely and be sure that are readable

                IMPORTANT CONSTRAINTS:
                - Convert the columns into the appropriate format IF you think that it would be beneficial.
                - The dataset is already loaded as a pandas DataFrame named 'df'
                - DO NOT use pd.read_csv() or any file reading functions
                - DO NOT import pandas (pd is already available)
                - Use only the dataframe 'df' that is already in memory
                - Include print() statements to show results
                - For plots: use plt.figure() and DO NOT use plt.show() - the plot will be displayed automatically
                - Return ONLY executable Python code, with very good explanation


                OUTPUT FORMATTING RULES:
                - Format numerical results nicely using round() and f-strings
                - Instead of print(df.describe()), use formatted statistics
                - For large tables, show only key insights, not full dataframes
                - Use clear, readable print statements with labels
                - Example: print(f"Average energy consumption: {{df['Energy_Consumption'].mean():.3f}}")


                PLOTTING GUIDELINES:
                - Use matplotlib/seaborn for visualizations
                - Create figure with plt.figure(figsize=(12, 8)) 
                - DO NOT call plt.show()
                - Add proper titles and labels


                Generate Python code using the existing dataframe 'df':
                Data Summary: {data_summary}
                """


        response = await self.client.chat.complete_async(
            model="codestral-2501",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0.7
        )

        return _clean_code(response.choices[0].message.content.strip())
