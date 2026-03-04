import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "192.168.56.107",  # IP Load Balancer
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "Akuganteng"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def insert_data():
    data = input("Masukkan data: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO test_table (data, created_at) VALUES (%s, %s)",
        (data, datetime.now())
    )
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data berhasil di-insert")

def read_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT inet_server_addr();")
    server_ip = cur.fetchone()[0]

    print("\n==============================")
    print(f"📡 Server Aktif : {server_ip}")
    print("==============================\n")

    cur.execute("""
        SELECT id, data, created_at 
        FROM test_table 
        ORDER BY id;
    """)
    rows = cur.fetchall()

    if not rows:
        print("Belum ada data.\n")
    else:
        print(f"{'ID':<5} {'DATA':<20} {'CREATED AT'}")
        print("-" * 50)
        for row in rows:
            id, data, created_at = row
            print(f"{id:<5} {data:<20} {created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    print()
    cur.close()
    conn.close()

while True:
    print("\n1. Insert Data (Write)")
    print("2. Lihat Data (Read)")
    print("3. Exit")
    pilih = input("Pilih: ")

    if pilih == "1":
        insert_data()
    elif pilih == "2":
        read_data()
    elif pilih == "3":
        break
    else:
        print("Pilihan tidak valid")
