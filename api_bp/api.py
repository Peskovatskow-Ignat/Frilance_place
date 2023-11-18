from flask import Blueprint, jsonify, abort
from datetime import datetime

from Frilance_place.functions import get_pg_connect

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")


@api_bp.route('/orders')
def api_index():
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


