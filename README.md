# Natural Language to SQL Search

A complete Natural Language → SQL search engine running locally on Windows with PostgreSQL 18 + Ollama (Llama 3.2).

## Features
- Works 100% offline
- Real PostgreSQL with relationships
- Beautiful Streamlit UI
- Handles: employees, departments, products, orders

## How to Run
1. Install PostgreSQL 18
2. Install Ollama → `ollama run llama3.2`
3. Update password in `app.py`
4. Run:
```bash
python populate_data.py
streamlit run app.py

