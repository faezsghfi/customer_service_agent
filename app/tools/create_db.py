
import sqlite3


DB_PATH = "data/orders.db"


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


cursor.execute(
"""
CREATE TABLE IF NOT EXISTS orders (

    order_id TEXT PRIMARY KEY,

    status TEXT,

    tracking_code TEXT,

    estimated_time TEXT,

    cancel_reason TEXT

)
"""
)


orders = [
    (
        "1001",
        "در حال پردازش",
        None,
        "۲ روز کاری",
        None
    ),

    (
        "1002",
        "ارسال شده",
        "123456789IR",
        None,
        None
    ),

    (
        "1003",
        "لغو شده",
        None,
        None,
        "عدم موجودی انبار"
    )
]


cursor.executemany(
"""
INSERT OR REPLACE INTO orders
VALUES (?, ?, ?, ?, ?)
""",
orders
)


connection.commit()

connection.close()


print("Database created")
