import jwt
from flask import Blueprint, jsonify, abort, request, current_app
from datetime import datetime, timezone, timedelta

from psycopg2.sql import SQL, Literal

from Frilance_place.api_bp.decoratos import token_required
from Frilance_place.functions import get_pg_connect

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")


@api_bp.route('/orders')
def api_orders():
    conn = get_pg_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, title, description, price, date, customer_id, skill, status FROM orders where status""")

        orders_list = []
        for order in cur.fetchall():
            id, title, description, price, date_created, customer_id, skill, status = order

            # Format the date as 'dd-mm-yyyy'
            formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

            orders_list.append({
                'id': id,
                'title': title,
                'description': description,
                'price': price,
                'date_created': formatted_date,
                'customer_id': customer_id,
                'skill': skill,
                'status': status,
            })

        return jsonify(orders_list)

    except Exception as ex:
        return abort(418)

    finally:
        cur.close()
        conn.close()


@api_bp.route('/order/<order_id>')
def api_order(order_id):
    conn = get_pg_connect()
    cur = conn.cursor()
    try:
        cur.execute(SQL(
            """SELECT id, title, description, price, date, customer_id, skill, status 
            FROM orders where status and id = {order_id}""").format(
            order_id=Literal(order_id)))

        id, title, description, price, date_created, customer_id, skill, status = cur.fetchone()

        # Format the date as 'dd-mm-yyyy'
        formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

        order_dict = {
            'id': id,
            'title': title,
            'description': description,
            'price': price,
            'date_created': formatted_date,
            'customer_id': customer_id,
            'skill': skill,
            'status': status,
        }

        return jsonify(order_dict)

    except Exception as ex:
        print(ex)
        return abort(418)

    finally:
        cur.close()
        conn.close()


@api_bp.route('/order')
def api_order_qwery():
    order_id = request.args.get('id')
    conn = get_pg_connect()
    cur = conn.cursor()
    try:
        cur.execute(SQL(
            """SELECT id, title, description, price, date, customer_id, skill, status 
            FROM orders where status and id = {order_id}""").format(
            order_id=Literal(order_id)))

        id, title, description, price, date_created, customer_id, skill, status = cur.fetchone()

        # Format the date as 'dd-mm-yyyy'
        formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

        order_dict = {
            'id': id,
            'title': title,
            'description': description,
            'price': price,
            'date_created': formatted_date,
            'customer_id': customer_id,
            'skill': skill,
            'status': status,
        }

        return jsonify(order_dict)

    except Exception as ex:
        print(ex)
        return abort(418)

    finally:
        cur.close()
        conn.close()


@api_bp.route('/auth', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        key = request.json.get("key")
        print(key, current_app.secret_key)
        if key != current_app.secret_key:
            return abort(418)
        exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        token = jwt.encode(dict(email=email, password=password, exp=exp), current_app.secret_key,
                           algorithm="HS256")
        return {"status": "token generated successfully", "token": token}
    return abort(418)


@api_bp.route('/get_customer', methods=["GET", "POST"])
@token_required
def get_customer():
    if request.method == "POST":  # проверяем метод
        conn = get_pg_connect()
        cur = conn.cursor()
        cur.execute(SQL("""SELECT id, username, email FROM customer"""))
        users = cur.fetchall()
        users_list = []
        for user in users:
            user_id, username, email = user
            cur.execute(SQL("""SELECT id, title, description, price FROM orders WHERE customer_id = {id}""").format(
                id=Literal(user_id)))
            orders = cur.fetchall()
            orders_list = []
            for order in orders:
                order_id, title, description, price = order
                orders_list.append({
                    'order_id': order_id,
                    'title': title,
                    'description': description,
                    'price': price
                })
            users_list.append({
                user_id: {
                    "name": username,
                    "email": email,
                    "orders": orders_list
                }
            })
        return jsonify(users_list)
    return abort(405)
