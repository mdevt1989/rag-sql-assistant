from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging

class ChartGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _get_axis_labels(self, df: pd.DataFrame) -> Dict[str, str]:
        """Determine appropriate axis labels based on column names."""
        columns = list(df.columns)
        
        # Common patterns for measures (usually numeric columns)
        measure_patterns = ['total', 'sum', 'avg', 'count', 'amount', 'revenue', 'sales', 'profit']
        # Common patterns for dimensions (usually categorical or time-based columns)
        dimension_patterns = ['name', 'category', 'region', 'date', 'month', 'year', 'id']
        
        y_axis = None
        x_axis = None
        
        # Find measure column (y-axis)
        for col in columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in measure_patterns):
                y_axis = col
                break
        
        # Find dimension column (x-axis)
        for col in columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in dimension_patterns):
                x_axis = col
                break
        
        # Fallback: if no patterns matched
        if not y_axis and len(columns) >= 2:
            # Assume last column is measure if numeric
            if pd.api.types.is_numeric_dtype(df[columns[-1]]):
                y_axis = columns[-1]
                x_axis = columns[0]
        
        # Final fallback
        if not y_axis:
            y_axis = columns[-1]
        if not x_axis:
            x_axis = columns[0]
            
        return {"x": x_axis, "y": y_axis}

    def generate_chart(self, data: List[Dict[str, Any]], chart_type: str):
        try:
            # If data is empty list
            if not data:
                return "No data available to generate chart."
                
            df = pd.DataFrame(data)
            
            # Check if dataframe is empty
            if df.empty:
                return "No data available to generate chart."
                
            # Ensure we have at least two columns for meaningful visualization
            if len(df.columns) < 2:
                return "Insufficient columns for visualization. Need at least 2 columns."
                
            try:
                # Get appropriate axis labels
                axis_labels = self._get_axis_labels(df)
                
                if chart_type == "bar":
                    fig = px.bar(
                        df,
                        x=axis_labels["x"],
                        y=axis_labels["y"],
                        title=f"{axis_labels['y']} by {axis_labels['x']}"
                    )
                elif chart_type == "line":
                    fig = px.line(
                        df,
                        x=axis_labels["x"],
                        y=axis_labels["y"],
                        title=f"{axis_labels['y']} over {axis_labels['x']}"
                    )
                elif chart_type == "scatter":
                    fig = px.scatter(
                        df,
                        x=axis_labels["x"],
                        y=axis_labels["y"],
                        title=f"{axis_labels['y']} vs {axis_labels['x']}"
                    )
                else:
                    return f"Unsupported chart type: {chart_type}"
                
                # Update layout for better readability
                fig.update_layout(
                    xaxis_title=axis_labels["x"].replace('_', ' ').title(),
                    yaxis_title=axis_labels["y"].replace('_', ' ').title(),
                    template="plotly_white"
                )
                
                return fig
                
            except Exception as e:
                self.logger.error(f"Error creating chart: {str(e)}")
                return f"Could not create chart: {str(e)}"
                
        except Exception as e:
            self.logger.error(f"Error generating chart: {str(e)}")
            return f"Error generating chart: {str(e)}" 