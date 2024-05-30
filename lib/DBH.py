import os

import psycopg2
import psycopg2.extras
from geopy.distance import geodesic


class DBH:
    conn = False
    cursor = False

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )

        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def getDriver(self, driver_id):

        self.cursor.execute(
            'SELECT * FROM "users"  WHERE role_id=27 AND id=%s', (driver_id,)
        )
        records = self.cursor.fetchall()

        return records

    def getAllDrivers(self):

        self.cursor.execute('SELECT * FROM "users"  WHERE role_id=27')
        records = self.cursor.fetchall()

        return records

    def getFreeOrders(self, id, limit):
        self.cursor.execute(
            "SELECT * FROM orders WHERE driver_id=%s AND status = 'new' ORDER BY updated_at DESC LIMIT %s",
            (id, limit),
        )
        records = self.cursor.fetchall()

        return records

    def GetOrdersByDriver(self, driver_id, limit):

        self.cursor.execute(
            'SELECT * FROM "orders"  WHERE driver_id=%s  order by updated_at DESC LIMIT %s',
            (driver_id, limit),
        )
        records = self.cursor.fetchall()

        return records

    def getNearbyOrders(self, driver_id, radius_km, limit):
        driver_location = self.GetDriverCurrentLocation(driver_id)
        if not driver_location:
            return []  # Если местоположение водителя не найдено, вернуть пустой список

        driver_latitude = driver_location[0]["geo_latitude"]
        driver_longitude = driver_location[0]["geo_longitude"]

        nearby_orders = []

        all_orders = self.cursor.execute(
            "SELECT id, geo_latitude, geo_longitude FROM orders WHERE status = 'new'"
        ).fetchall()

        for order in all_orders:
            order_id = order["id"]
            order_latitude = order["geo_latitude"]
            order_longitude = order["geo_longitude"]

            distance = geodesic(
                (driver_latitude, driver_longitude), (order_latitude, order_longitude)
            ).kilometers

            if distance <= radius_km:
                nearby_orders.append(order_id)

            if len(nearby_orders) >= limit:
                break

        return nearby_orders

    def GetDriverRating(self, driver_id):

        self.cursor.execute(
            'SELECT * FROM "account_ratings" WHERE account_id=' + str(driver_id)
        )
        records = self.cursor.fetchall()
        data = [dict(row) for row in records]

        return data

    def GetDriverCurrentLocation(self, driver_id):

        self.cursor.execute(
            'SELECT created_at,geo_latitude,geo_longitude FROM "user_locations" WHERE user_id='
            + str(driver_id)
            + " order by created_at DESC LIMIT 1"
        )
        records = self.cursor.fetchall()
        data = [dict(row) for row in records]

        return data

    def GetOrderLocation(self, order_id):
        self.cursor.execute(
            "SELECT geo_latitude, geo_longitude FROM orders WHERE id = %s", (order_id,)
        )
        record = self.cursor.fetchone()

        if record:
            order_latitude, order_longitude = record
            return order_latitude, order_longitude
        else:
            return None
