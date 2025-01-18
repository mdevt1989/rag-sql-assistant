# main.py

import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

import gradio as gr
from src.database.db_manager import DatabaseManager
from src.llm.llm_handler import LLMHandler
from src.visualization.chart_generator import ChartGenerator
from src.utils.logger import Logger

class DataAnalysisApp:
    def __init__(self):
        Logger.setup_logging()
        self.db_manager = DatabaseManager()
        self.llm_handler = LLMHandler()
        self.chart_generator = ChartGenerator()

    def process_query(self, question: str, chart_type: str):
        try:
            # Generate SQL query from natural language question
            sql_query = self.llm_handler.generate_sql_query(question)
            
            # Check if the response is an error message
            if sql_query.startswith("Unable to generate query"):
                return None, sql_query
            
            if not sql_query or sql_query.isspace():
                return None, "Error: Could not generate SQL query"
            
            # Execute the query
            try:
                results = self.db_manager.execute_query(sql_query)
            except Exception as e:
                return None, f"Database error: {str(e)}"
            
            if not results:
                return None, "No data found for the query"
            
            # Check if results should be plotted or displayed as text
            if len(results) == 1 and len(results[0]) == 1:
                # Single value result - display as text
                key = list(results[0].keys())[0]
                value = results[0][key]
                return None, f"{key}: {value}"
            
            elif len(results) == 1:
                # Single row with multiple columns - display as text
                formatted_result = ", ".join([f"{k}: {v}" for k, v in results[0].items()])
                return None, formatted_result
            
            else:
                # Multiple rows - generate visualization
                try:
                    chart = self.chart_generator.generate_chart(results, chart_type)
                    if isinstance(chart, str):  # Error message
                        return None, chart
                    return chart, None  # Success case
                except Exception as e:
                    return None, f"Error generating chart: {str(e)}"
            
        except Exception as e:
            return None, f"Error: {str(e)}"

    def launch_interface(self):
        iface = gr.Interface(
            fn=self.process_query,
            inputs=[
                gr.Textbox(
                    label="Enter your question",
                    placeholder="e.g., Show me total sales by region"
                ),
                gr.Dropdown(
                    choices=["bar", "line", "scatter"],
                    label="Select chart type",
                    value="bar"
                )
            ],
            outputs=[
                gr.Plot(label="Visualization"),
                gr.Textbox(label="Message")
            ],
            title="Data Analysis Assistant",
            description="Ask questions about your data in natural language",
            examples=[
                ["Show me total sales by region", "bar"],
                ["What is the monthly revenue trend for 2023?", "line"],
                ["What are the top 5 sales reps by total revenue?", "bar"],
                ["What is the total revenue for all time?", "bar"],  # Will show as text
                ["Compare sales performance across different regions", "bar"],
                ["Show me the distribution of order sizes by industry", "scatter"],
                ["What's the average deal size by account tier?", "bar"],
                ["How many unique customers do we have?", "bar"],  # Will show as text
                ["Show me daily order counts for the last month", "line"]
            ],
            allow_flagging="never"
        )
        iface.launch(share=False, server_port=7860)

if __name__ == "__main__":
    app = DataAnalysisApp()
    app.launch_interface()