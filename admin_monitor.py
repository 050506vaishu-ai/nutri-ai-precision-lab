import sqlite3
import os
from datetime import datetime

def check_database():
    db_path = 'users.db'
    
    if not os.path.exists(db_path):
        print("--- Error: users.db not found. Run your main app first! ---")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("   NUTRI AI - SECURE ADMIN AUDIT PANEL")
    print("="*50)

    # 1. Check Registered Users
    print("\n[ REGISTERED USERS ]")
    print(f"{'ID':<4} | {'Full Name':<20} | {'Email Address':<25}")
    print("-" * 55)
    
    try:
        cursor.execute('SELECT id, full_name, email FROM users')
        users = cursor.fetchall()
        for u in users:
            print(f"{u[0]:<4} | {u[1]:<20} | {u[2]:<25}")
    except sqlite3.OperationalError:
        print("No users table found yet.")

    # 2. Check Database Stats
    print("\n" + "="*50)
    cursor.execute('SELECT COUNT(*) FROM users')
    total = cursor.fetchone()[0]
    print(f"TOTAL REGISTERED BIOMETRIC PROFILES: {total}")
    print("="*50 + "\n")

    conn.close()

if __name__ == "__main__":
    check_database()