from chronos import BaseChronosPipeline
import torch
import pandas as pd
from matplotlib import pyplot as plt


class ChronosForecaster:
    def __init__(self, model_name="amazon/chronos-bolt-small"):
        self.pipeline = BaseChronosPipeline.from_pretrained(model_name,torch_dtype=torch.bfloat16)
        self.name = "forecast_tool"
        self.description = "Generate time-series forecasts using Chronos"


    def get_tool_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column_name": {
                            "type": "string",
                            "description": "Name of the column to forecast"
                        },
                        "prediction_length": {
                            "type": "integer",
                            "description": "Number of time steps to predict"
                        }
                    },
                    "required": ["column_name", "prediction_length"]
                }
            }
        }

    async def forecast(self, series, prediction_length):
        """
        series: list or pandas Series of float values
        prediction_length: number of time steps to predict (e.g., 24 for 1 day hourly)
        """
        if isinstance(series, pd.Series):
            series = series.dropna().tolist()

        context = torch.tensor(series).unsqueeze(0)  # shape (1, len)
        quantiles , mean = self.pipeline.predict_quantiles(context, prediction_length=prediction_length,quantile_levels=[0.7, 0.8, 0.9])

        forecast_index = range(len(series), len(series) + prediction_length)

        history_length = min(5 * prediction_length, len(series))
        start_idx = len(series) - history_length

        historical_index = range(start_idx, len(series))
        historical_data = series[start_idx:]

        low, median, high = quantiles[0, :, 0], quantiles[0, :, 1], quantiles[0, :, 2]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(historical_index, historical_data,color="royalblue", label="historical data")
        ax.plot(forecast_index, median, color="tomato", label="median forecast")
        ax.fill_between(forecast_index, low, high, color="tomato", alpha=0.3, label="Prediction intervals")
        ax.legend()
        ax.grid()
        ax.set_title("Time Series Forecast")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Values")


        return {
            "median_forecast": median.tolist(),
            "low_quantile": low.tolist(),
            "high_quantile": high.tolist(),
            "forecast_index": list(forecast_index),
            "figure": fig

        }
