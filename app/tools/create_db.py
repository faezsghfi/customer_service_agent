
import sqlite3
import os


DB_PATH = "data/orders.db"


def create_database():

    os.makedirs(
        "data",
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute(
        "DROP TABLE IF EXISTS orders"
    )


    cursor.execute(
        """
        CREATE TABLE orders (

            id TEXT PRIMARY KEY,

            status TEXT,

            estimated_time TEXT,

            tracking_code TEXT,

            cancel_reason TEXT

        )
        """
    )


    orders = [

        (
            "1001",
            "در حال پردازش",
            "۲ روز کاری",
            None,
            None
        ),

        (
            "1002",
            "ارسال شده",
            None,
            "123456789IR",
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
        INSERT INTO orders
        VALUES (?, ?, ?, ?, ?)
        """,
        orders
    )


    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
