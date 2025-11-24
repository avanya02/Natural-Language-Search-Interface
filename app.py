import streamlit as st
import psycopg2

PASSWORD = "Avanya@123"   

conn = psycopg2.connect(host="localhost", dbname="companydb", user="postgres", password=PASSWORD)
cur = conn.cursor()

st.title("Natural Language Search Interface")

query = st.text_input("Ask:", placeholder="type here..")

if st.button("Search", type="primary"):
    q = query.lower()

    if "employee" in q and "all" in q:
        sql = "SELECT * FROM employees;"
    elif "engineering" in q:
        sql = "SELECT e.* FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Engineering';"
    elif "laptop" in q:
        sql = "SELECT * FROM products WHERE name ILIKE '%laptop%';"
    elif "order" in q and "over" in q:
        sql = "SELECT * FROM orders WHERE order_total > 500;"
    else:
        sql = "SELECT * FROM employees LIMIT 5;"

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        st.success(f"Found {len(rows)} results")
        st.dataframe([dict(zip(cols, row)) for row in rows])
    except Exception as e:
        st.error(str(e))

