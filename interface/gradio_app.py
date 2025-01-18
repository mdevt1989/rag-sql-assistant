# interface/gradio_app.py

import gradio as gr
from database.db_operations import DatabaseOperations
from llm.query_generator import QueryGenerator
from visualization.chart_generator import ChartGenerator

class GradioInterface:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.query_gen = QueryGenerator()
        self.chart_gen = ChartGenerator()

    def process_query(self, user_query: str):
        try:
            sql_query = self.query_gen.generate_sql_query(user_query)
            results = self.db_ops.execute_query(sql_query)
            chart = self.chart_gen.generate_chart(results)
            return str(results), chart
        except Exception as e:
            return f"Error processing query: {str(e)}", None

    def create_interface(self):
        iface = gr.Interface(
            fn=self.process_query,
            inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
            outputs=[gr.Textbox(), gr.Plot()],
            title="Database Query Visualization System",
            description="Enter a natural language query to retrieve and visualize data from the database."
        )
        return iface