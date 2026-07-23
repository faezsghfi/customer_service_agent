

import sqlite3

from langchain_core.tools import tool



DB_PATH = "data/orders.db"



@tool
def get_order_status(order_id: str) -> dict:
    """
    Get order status from database.

    Returns order information or 404 error.
    """


    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )


    result = cursor.fetchone()


    connection.close()


    # simulate 404
    if result is None:

        return {
            "status_code": 404,
            "message": "Order Not Found"
        }


    return {

        "status_code": 200,

        "order_id": result[0],

        "status": result[1],

        "tracking_code": result[2],

        "estimated_time": result[3],

        "cancel_reason": result[4]
    }
