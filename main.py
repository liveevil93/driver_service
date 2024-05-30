from fastapi import FastAPI, HTTPException

from lib.sortingOrders_1a import db_handler, get_orders

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "pong"}


@app.get("/drivers")
async def get_all_drivers_data():
    all_drivers = db_handler.getAllDrivers()
    data = []
    for driver in all_drivers:
        driver_id = driver["id"]
        driver_data = {"id": driver_id, "orders": []}

        orders_info = get_orders(driver_id)
        for order in orders_info:
            order_data = {
                "id": order["OrderID"],
                "latitude": order["OrderLatitude"],
                "longitude": order["OrderLongitude"],
                "nearby_orders": [],
            }
            for nearby_order in order["NearbyOrders"]:
                order_data["nearby_orders"].append(
                    {
                        "id": nearby_order["id"],
                        "distance": nearby_order["distance"],
                    }
                )
            driver_data["orders"].append(order_data)
        data.append(driver_data)
    return {"data": data}


@app.get("/drivers/{id}")
async def get_driver_data(id: int):
    one_driver = db_handler.getDriver(id)
    if len(one_driver) > 0:
        driver_data = {"id": id, "orders": []}
        orders_info = get_orders(id)
        for order in orders_info:
            order_data = {
                "id": order["OrderID"],
                "latitude": order["OrderLatitude"],
                "longitude": order["OrderLongitude"],
                "nearby_orders": [],
            }
            for nearby_order in order["NearbyOrders"]:
                order_data["nearby_orders"].append(
                    {
                        "id": nearby_order["id"],
                        "distance": nearby_order["distance"],
                    }
                )
            driver_data["orders"].append(order_data)
        return {"data": driver_data}
    raise HTTPException(status_code=404)
