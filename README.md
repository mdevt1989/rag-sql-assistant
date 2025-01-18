# RAG SQL Assistant
 Its a demo project to explore the capabilities of RAG (Retrieval-Augmented Generation) application that enables natural language querying of SQL databases with automated visualization capabilities.

In this project, I used Parch and Posey database to explore.


## 🌟 Features

- **Natural Language Processing**: Convert plain English questions into SQL queries using LLaMA 3 (70B)
- **Local Privacy**: Runs completely locally using Ollama - no data leaves your system
- **Interactive Visualization**: Automatic chart generation based on query results
- **Database Integration**: Seamless PostgreSQL connectivity
- **User-Friendly Interface**: Simple Gradio web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL database
- [Ollama](https://ollama.ai/) installed with LLaMA 3 70B model
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mdevt1989/rag-sql-assistant.git
cd rag-sql-assistant
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
```

### Running the Application

1. Using the main script:

```bash
python main.py
```

This will:
- Initialize the database connection
- Start the Ollama LLM service
- Launch the Gradio interface
- Open your default browser automatically

```

The application will be available at http://localhost:7860 by default.

### Using the Interface

1. Once the application is running:
   - Enter your question in natural language
   - Choose your preferred visualization type
   - Click "Submit" to see results

2. Example queries you can try:

```sql
"Show me the total sales by product category for the last 3 months"
"What are the top 5 customers by revenue?"
```

## 🏗️ Project Structure

```
rag-sql-assistant/
├── config/              # Configuration files
├── src/                 # Source code
│   ├── database/       # Database connectivity
│   ├── llm/           # LLM integration
│   ├── utils/         # Utilities and helpers
│   └── app.py         # Main application
├── main.py             # Main entry point
└── tests/              # Test files
```

## 🔧 Configuration

The application can be configured through:
- `config/config.py` - Main configuration
- `.env` file - Environment-specific settings
- Gradio interface settings

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License
Only for Educational purposes.
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 How It Works

1. **Query Processing**:
   - User inputs a natural language question
   - LLaMA 3 processes and converts it to SQL
   - SQL query is validated and optimized

2. **Data Retrieval**:
   - SQL query executes against PostgreSQL
   - Results are formatted and processed

3. **Visualization**:
   - Data is analyzed for best visualization method
   - Interactive charts are generated using Plotly
   - Results are displayed in the Gradio interface

## ⚠️ Limitations

- Currently supports PostgreSQL only
- Requires local Ollama installation
- Limited to basic SQL operations
- Chart types are pre-defined

## 🆘 Support

For issues and feature requests, please use the GitHub Issues tracker.

