import psycopg2
from datetime import datetime

LB_IP = "192.168.56.107"   # IP Load Balancer / HAProxy
USER = "postgres"
PASSWORD = "Akuganteng"
DB = "postgres"


def check_write():
    print("\n--- Checking WRITE PORT (Port 5432) ---")

    conn = psycopg2.connect(
        host=LB_IP,
        port=5432,
        database=DB,
        user=USER,
        password=PASSWORD
    )

    cur = conn.cursor()

    cur.execute("SELECT inet_server_addr(), pg_is_in_recovery();")
    server, recovery = cur.fetchone()

    if recovery == False:
        print(f"Status: Connected to MASTER (Writable) [{server}]")
    else:
        print(f"Status: Unexpected Replica on write port [{server}]")

    data = f"Data sent to Master port at {datetime.now()}"

    cur.execute(
        "INSERT INTO test_table (data) VALUES (%s);",
        (data,)
    )

    conn.commit()

    print("Action: Successfully wrote new row to table.")
    print(f"Latest Data: '{data}'")

    cur.close()
    conn.close()


def check_read():
    print("\n--- Checking READ PORT (Port 5433) ---")

    conn = psycopg2.connect(
        host=LB_IP,
        port=5433,
        database=DB,
        user=USER,
        password=PASSWORD
    )

    cur = conn.cursor()

    cur.execute("SELECT inet_server_addr(), pg_is_in_recovery();")
    server, recovery = cur.fetchone()

    if recovery == True:
        print(f"Status: Connected to SLAVE (Read-Only) [{server}]")
    else:
        print(f"Status: Unexpected Master on read port [{server}]")

    cur.execute("""
        SELECT id, data, created_at
        FROM test_table
        ORDER BY id DESC
        LIMIT 3;
    """)

    rows = cur.fetchall()

    print("\nLatest Data:")
    print("---------------------------------------------------------------")
    print(f"{'ID':<5} {'DATA':<40} {'CREATED_AT'}")
    print("---------------------------------------------------------------")

    for r in rows:
        data = str(r[1])[:43] + "..." if len(str(r[1])) > 43 else r[1]
        print(f"{r[0]:<5} {data:<45} {r[2]}")

    cur.close()
    conn.close()


print("========== HA DATABASE TEST ==========")

check_write()
check_read()

print("\n========== TEST COMPLETE ==========")
