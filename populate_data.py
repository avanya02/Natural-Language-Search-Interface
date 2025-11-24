import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

PASSWORD = "Avanya@123"  


conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=PASSWORD,
    port=5432
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("Setting up database...")


try:
    cur.execute("DROP DATABASE IF EXISTS companydb;")
    print("Dropped existing companydb (if any)")
except Exception as e:
    print(f"Note: {e}")

cur.execute("CREATE DATABASE companydb;")
print("Created companydb")

cur.close()
conn.close()

conn = psycopg2.connect(
    host="localhost",
    database="companydb",
    user="postgres",
    password=PASSWORD
)
cur = conn.cursor()

print("Creating tables...")

cur.execute("""
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department_id INT REFERENCES departments(id),
    email VARCHAR(255),
    salary DECIMAL(10,2)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    employee_id INT REFERENCES employees(id),
    order_total DECIMAL(10,2),
    order_date DATE
);
""")

print("Inserting data...")

cur.execute("INSERT INTO departments(name) VALUES('HR'),('Engineering'),('Sales');")

employees = [
    ("Ria", 1, "abc@fds.com", 9000),
    ("Sarthak", 2, "abd@tif.com", 9500),
    ("Pihu", 2, "sur@uuh.com", 8800),
    ("Roy", 3, "fer@emb.com", 6200),
]
for name, dept, email, salary in employees:
    cur.execute(
        "INSERT INTO employees(name, department_id, email, salary) VALUES(%s,%s,%s,%s)",
        (name, dept, email, salary)
    )

products = ["Laptop", "PC", "Keyboard", "CPU", "SSD"]
for name in products:
    price = round(100 + len(name) * 25.5, 2)
    cur.execute("INSERT INTO products(name, price) VALUES(%s,%s)", (name, price))

customers = ["Jayant", "Arifa", "Rimie", "Aditi"]
for i, cust in enumerate(customers):
    cur.execute(
        """INSERT INTO orders(customer_name, employee_id, order_total, order_date)
           VALUES(%s, %s, %s, %s)""",
        (cust, (i % 4) + 1, 200 + i * 300, f"2025-{i+1:02d}-15")
    )

conn.commit()
cur.close()
conn.close()

print(" Database created and populated successfully!")
print("Run: streamlit run app.py")