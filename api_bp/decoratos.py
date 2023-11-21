import hashlib
import jwt
from flask import session, render_template, request, current_app
from functools import wraps
from psycopg2.sql import SQL, Literal

from functions import get_pg_connect


def login_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('data'):
            return render_template('index.html')

        return func(*args, **kwargs)

    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_pg_connect()
        cur = conn.cursor()
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            if token:
                try:
                    data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
                    cur.execute(SQL("""select email, password from executor where email = {email}""").format(
                        email=Literal(data["email"])))
                    email, password = cur.fetchone()

                    if not email:
                        return {"message": "user not found"}, 401
                    if not password == hashlib.sha224(
                            data["password"].encode()).hexdigest():
                        return {"message": "password invalid"}, 401
                except Exception as ex:
                    return {"message": "Invalid token", "error": str(ex)}, 401
            else:
                return {"message": "Authentication token required"}, 401
        else:
            return {"message": "Authorization required"}, 401

        return func(*args, **kwargs)

    return wrapper
