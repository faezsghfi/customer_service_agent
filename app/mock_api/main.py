
from fastapi import FastAPI, HTTPException

import sqlite3


app = FastAPI(
    title="Mock Order API"
)


DB_PATH = "data/orders.db"



@app.get("/orders/{order_id}")
def get_order(order_id: str):

    # شبیه سازی خطای 500

    if order_id == "5000":

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE id=?
        """,
        (order_id,)
    )


    order = cursor.fetchone()


    conn.close()


    if order is None:

        raise HTTPException(
            status_code=404,
            detail="Order Not Found"
        )


    order_id, status, estimated, tracking, reason = order


    return {

        "code": 200,

        "order_id": order_id,

        "status": status,

        "estimated_time": estimated,

        "tracking_code": tracking,

        "cancel_reason": reason
    }
