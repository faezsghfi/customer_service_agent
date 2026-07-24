
import requests

from langchain_core.tools import tool


API_URL = "http://localhost:8000/orders"



@tool
def get_order_status(order_id: str):
    """
    Get order status from Mock FastAPI Order API.
    """


    try:

        response = requests.get(
            f"{API_URL}/{order_id}"
        )


        if response.status_code == 200:

            return response.json()



        elif response.status_code == 404:

            return {
                "code": 404,
                "message": "Order Not Found"
            }



        else:

            return {
                "code": response.status_code,
                "message": response.text
            }



    except Exception as e:

        return {
            "code": 500,
            "message": str(e)
        }
