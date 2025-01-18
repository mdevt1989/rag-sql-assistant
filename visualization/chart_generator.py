# visualization/chart_generator.py

from typing import List, Dict, Any
import matplotlib.pyplot as plt

class ChartGenerator:
    @staticmethod
    def generate_chart(data: List[Dict[str, Any]], chart_type: str = 'bar'):
        plt.figure(figsize=(10, 6))
        if chart_type == 'bar':
            plt.bar(range(len(data)), [d['value'] for d in data])
            plt.xticks(range(len(data)), [d['category'] for d in data], rotation=45)
        elif chart_type == 'line':
            plt.plot(range(len(data)), [d['value'] for d in data])
            plt.xticks(range(len(data)), [d['date'] for d in data], rotation=45)
        plt.title("Data Visualization")
        plt.tight_layout()
        return plt