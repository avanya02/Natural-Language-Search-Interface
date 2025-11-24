import psycopg2

PASSWORD = "********" 

print("Checking PostgreSQL connection...")


try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=PASSWORD,
        port=5432
    )
    print("Connected to PostgreSQL")
    
    cur = conn.cursor()
    
    
    cur.execute("SELECT datname FROM pg_database WHERE datname = 'companydb';")
    result = cur.fetchone()
    
    if result:
        print("Database 'companydb' exists")
    else:
        print("Database 'companydb' does NOT exist")
        print("Run: python setup_and_populate.py")
        cur.close()
        conn.close()
        exit()
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("  1. PostgreSQL is not running")
    print("  2. Wrong password")
    print("  3. Wrong port (default is 5432)")
    exit()


try:
    conn = psycopg2.connect(
        host="localhost",
        database="companydb",
        user="postgres",
        password=PASSWORD,
        port=5432
    )
    print("Connected to 'companydb'")
    
    cur = conn.cursor()
    
    
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    
    if tables:
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
            
            
            cur.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cur.fetchone()[0]
            print(f"    ({count} rows)")
    else:
        print(" No tables found in 'companydb'")
        print(" Run: python setup_and_populate.py")
    
    cur.close()
    conn.close()
    
    print("\n all good. run: streamlit run app.py")
    
except Exception as e:
    print(f"✗ Error checking companydb: {e}")

    print("  → Run: python setup_and_populate.py")
