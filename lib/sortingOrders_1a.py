import math
from lib.DBH import DBH

db_handler = DBH()


def calculate_distance(lat1, lon1, lat2, lon2):
    # Функция для расчета расстояния между двумя точками на поверхности Земли
    R = 6371  # Радиус Земли в километрах
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def get_orders(driver_id):
    orders = db_handler.GetOrdersByDriver(
        driver_id, None
    )  # Получаем заказы для конкретного водителя

    result = []

    for order in orders:
        order_data = {
            "OrderID": order["id"],
            "OrderLatitude": order["pki_geo_latitude"],
            "OrderLongitude": order["pki_geo_longitude"],
            "NearbyOrders": [],
        }

        nearby_orders = db_handler.getNearbyOrders(
            order["pki_geo_latitude"], order["pki_geo_longitude"], limit=10
        )  # Получаем ближайшие заказы
        nearby_orders_sorted = sorted(
            nearby_orders,
            key=lambda x: calculate_distance(
                order["pki_geo_latitude"],
                order["pki_geo_longitude"],
                x["pki_geo_latitude"],
                x["pki_geo_longitude"],
            ),
        )

        for nearby_order in nearby_orders_sorted[:10]:
            distance = calculate_distance(
                order["pki_geo_latitude"],
                order["pki_geo_longitude"],
                nearby_order["pki_geo_latitude"],
                nearby_order["pki_geo_longitude"],
            )
            nearby_order["distance"] = distance

        order_data["NearbyOrders"] = nearby_orders_sorted[:10]
        result.append(order_data)

    return result
