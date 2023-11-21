import hashlib
import jwt
<<<<<<< HEAD
from flask import session, render_template, request, current_app
from functools import wraps
from psycopg2.sql import SQL, Literal

from functions import get_pg_connect
=======
from flask import session, render_template, redirect, request, current_app
from functools import wraps
from psycopg2.sql import SQL, Literal

from Frilance_place.functions import get_pg_connect
>>>>>>> 4d89ff9e7401396192a5275dda1b9aa3aaaa9f40


def login_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
<<<<<<< HEAD
        if not session.get('data'):
            return render_template('index.html')
=======
        try:
            if 'data' not in session:
                return render_template('index.html')
        except Exception as ex:
            if not session.get('data'):
                return redirect('/')
>>>>>>> 4d89ff9e7401396192a5275dda1b9aa3aaaa9f40

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
