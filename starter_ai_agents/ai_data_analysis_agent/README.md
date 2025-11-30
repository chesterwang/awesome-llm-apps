开发笔记

1. [Python API – DuckDB](https://duckdb.org/docs/stable/clients/python/overview)
  1. DuckDB的使用文档
  2. 使用非常方便
2. [Core Extensions – DuckDB](https://duckdb.org/docs/stable/core_extensions/overview)
  1. 还有各种插件可以使用
3. pandas 在处理字符串的单个双引号特殊情况的具体方法
  1. `df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)`
  2. CSV解析器中对于 引号的解析逻辑规则
    1. 根据 CSV 规范，连续的两个双引号 "" 代表一个字面意义上的双引号 "，而不是字段的结束。
4. 数据分析的tools  
  1. `tools=[duckdb_tools, PandasTools()],`
  2. 这两个工具都可以
  3. 但 PandasTools 写得过于粗糙，并且两个方法 需要dataframe做参数，所以在query中需要一定程度的引导说明是哪个表，即使是当前只有一个dataframe（虽然不指定哪个表也有可能执行成功）。
  4. PandasTools 中的init方法并没有 dataframes参数，必须手动赋值（不符合一般的python成员暴露规范）。


# 📊 AI Data Analysis Agent

### 🎓 FREE Step-by-Step Tutorial 
**👉 [Click here to follow our complete step-by-step tutorial](https://www.theunwindai.com/p/build-an-ai-data-analysis-agent) and learn how to build this from scratch with detailed code walkthroughs, explanations, and best practices.**

An AI data analysis Agent built using the Agno Agent framework and Openai's gpt-4o model. This agent helps users analyze their data - csv, excel files through natural language queries, powered by OpenAI's language models and DuckDB for efficient data processing - making data analysis accessible to users regardless of their SQL expertise.

## Features

- 📤 **File Upload Support**: 
  - Upload CSV and Excel files
  - Automatic data type detection and schema inference
  - Support for multiple file formats

- 💬 **Natural Language Queries**: 
  - Convert natural language questions into SQL queries
  - Get instant answers about your data
  - No SQL knowledge required

- 🔍 **Advanced Analysis**:
  - Perform complex data aggregations
  - Filter and sort data
  - Generate statistical summaries
  - Create data visualizations

- 🎯 **Interactive UI**:
  - User-friendly Streamlit interface
  - Real-time query processing
  - Clear result presentation

## How to Run

1. **Setup Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
   cd awesome-llm-apps/starter_ai_agents/ai_data_analysis_agent

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   - Get OpenAI API key from [OpenAI Platform](https://platform.openai.com)

3. **Run the Application**
   ```bash
   streamlit run ai_data_analyst.py
   ```

## Usage

1. Launch the application using the command above
2. Provide your OpenAI API key in the sidebar of Streamlit
3. Upload your CSV or Excel file through the Streamlit interface
4. Ask questions about your data in natural language
5. View the results and generated visualizations

