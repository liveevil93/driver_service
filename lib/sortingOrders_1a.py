from modules.DBH import DBH
import math

db_handler = DBH()

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Радиус Земли в километрах
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def get_orders(driver_id):
    orders = db_handler.GetOrdersByDriver(driver_id, None)

    result = []

    for order in orders:
        order_data = {
            'OrderID': order['id'],
            'OrderLatitude': order['pki_geo_latitude'],
            'OrderLongitude': order['pki_geo_longitude'],
            'NearbyOrders': []
        }

        nearby_orders = db_handler.getNearbyOrders(order['pki_geo_latitude'], order['pki_geo_longitude'], limit=10)
        nearby_orders_sorted = sorted(nearby_orders, key=lambda x: (x['status'] != 'picked up', calculate_distance(order['pki_geo_latitude'], order['pki_geo_longitude'], x['pki_geo_latitude'], x['pki_geo_longitude'])))

        for nearby_order in nearby_orders_sorted[:10]:
            distance = calculate_distance(order['pki_geo_latitude'], order['pki_geo_longitude'], nearby_order['pki_geo_latitude'], nearby_order['pki_geo_longitude'])
            nearby_order['distance'] = distance

        order_data['NearbyOrders'] = nearby_orders_sorted[:10]
        result.append(order_data)

    return result

all_drivers = db_handler.getAllDrivers()

for driver in all_drivers:
    driver_id = driver['id']
    print(f"Информация о водителе с id {driver_id}:")

    picked_up_orders = db_handler.getPickedUpOrders(driver_id, 10)
    new_orders = db_handler.getFreeOrders(driver_id, 10)

    print("Заказы со статусом 'picked up':")
    for picked_up_order in picked_up_orders:
        print(f"ID: {picked_up_order['id']}, Статус: {picked_up_order['status']}")

        nearby_new_orders = db_handler.getNearbyOrders(picked_up_order['id'], 5, 1)
        if nearby_new_orders:
            nearby_order_id = nearby_new_orders[0]['id']
            distance_to_nearest_order = calculate_distance(picked_up_order['pki_geo_latitude'], picked_up_order['pki_geo_longitude'], nearby_new_orders[0]['pki_geo_latitude'], nearby_new_orders[0]['pki_geo_longitude'])
            print(f"Ближайший заказ со статусом 'new': ID {nearby_order_id}, Расстояние: {distance_to_nearest_order} км")

    print("Заказы со статусом 'new':")
    for new_order in new_orders:
        print(f"ID: {new_order['id']}, Статус: {new_order['status']}")
