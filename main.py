import logging
import os
import psycopg2
import hashlib

from flask import render_template, redirect, session, flash, Flask, request, logging
from flask_mail import Mail, Message
from functions import resize_and_convert_to_jpg, profile_photo, generate_secure_string
from datetime import datetime, timedelta
import base64


def get_pg_connect():
    """
    Try executing создан для удобство для того чтобы не запускать через compose
    подклчение к созданому контейнеру
    """

    try:
        conn = psycopg2.connect(
            host='postgres',
            port=5432,
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
    except Exception as ex:
        conn = psycopg2.connect(
            host='localhost',
            port=3434,
            database='flask',
            user='admin',
            password='change_me'
        )

    return conn


app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=5)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JSON_AS_ASCII"] = True
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)


@app.route('/')
def index():
    if 'data' in session:
        data = session['data']
        print(data['roll'])
        try:
            conn = get_pg_connect()
            cur = conn.cursor()

            if data.get('roll') == 'customer':
                cur.execute(
                    f"""SELECT username FROM {data.get('roll')} WHERE id = %s""", (str(data['id'])))
            else:
                cur.execute(
                    f"""SELECT username FROM {data.get('roll')} WHERE id = %s""", (str(data['id'])))

            username = cur.fetchone()[0] if cur.rowcount > 0 else None
            conn.close()

            return render_template('index.html', username=username)

        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()

    return render_template('index.html')


@app.route('/orders/<skill>')
def orders_skill(skill):
    conn = get_pg_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, title, description, price, date, customer_id, skill, status FROM orders where skill = %s and status = %s""",
            (skill, True))

        orders_list = []
        for order in cur.fetchall():
            id, title, description, price, date_created, customer_id, skill, status = order
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
        cur.execute("""SELECT count(*) FROM orders where skill = %s and status = %s""",
                    (skill, True))

        return render_template('orders.html', orders=orders_list, count=cur.fetchone()[0])

    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return "Ошибка при получении заказов из базы данных"


@app.route('/order/<id>')
def order(id):
    conn = get_pg_connect()
    cur = conn.cursor()
    customer_id = id
    if session.get('data') and session.get('data')['roll'] == 'customer':
        req = 'and c.id = {data}'.format(data=session.get("data")['id'])
        print(req)
    elif session.get('data') and session.get('data')['roll'] == 'executor':
        req = 'and e.id = {data}'.format(data=session.get("data")['id'])
    else:
        req = ''
    try:
        cur.execute(
            """SELECT o.id, title, price, c.rating, data, c.data, full_description, skill, c.username FROM orders o
join customer c on o.customer_id = c.id 
WHERE o.id = %s""", (id,))
        result = cur.fetchone()
        formatted_date = datetime.strftime(result[4], '%d-%m-%Y')
        order_dict = {
            'id': result[0],
            'title': result[1],
            'price': result[2],
            'rating': result[3],
            'date_created': formatted_date,
            'data_reg': result[5],
            'full_description': result[6],
            'skill': result[7],
            'username': result[8],
        }
        cur.execute("""select e.id, e.email, e.username, e.last_name, e.first_name, eto.data from executor_to_order eto
join executor e on e.id = eto.executor_id 
join orders o on o.id = eto.order_id 
join customer c on c.id = o.customer_id 
where o.id = %s {req}""".format(req=req), (id,))
        users_dict = []
        for user in cur.fetchall():
            id, email, username, last_name, first_name, data = user
            formatted_date = datetime.strftime(data, '%d-%m-%Y')
            users_dict.append({
                'id': id,
                'email': email,
                'username': username,
                'last_name': last_name,
                'first_name': last_name,
                'data': formatted_date
            })
        cur.execute("""select c.id from customer c
            join orders o on o.customer_id = c.id
            where o.id = %s""", customer_id)
        return render_template('order.html', order=order_dict, users=users_dict, customer=cur.fetchone()[0])
    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return "Ошибка при получении заказов из базы данных"

    finally:
        cur.close()
        conn.close()


@app.route('/orders')
def orders():
    conn = get_pg_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, title, description, price, date, customer_id, skill, status FROM orders""")

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
        cur.execute("""SELECT count(*) FROM orders""")

        return render_template('orders.html', orders=orders_list, count=cur.fetchone()[0])

    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return "Ошибка при получении заказов из базы данных"

    finally:
        cur.close()
        conn.close()


@app.route('/signin', methods=['POST', 'GET'])
def sign_in():
    if session.get('data'):
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            roll = request.form.get('roll')

            conn = get_pg_connect()
            cur = conn.cursor()

            try:
                if roll != 'customer':
                    cur.execute(
                        f"""SELECT id, username, first_name, last_name, email, data, rating, password, photo 
                        FROM executor WHERE email = %s""",
                        (email,))
                else:
                    cur.execute(
                        f"""SELECT id, username, first_name, last_name, email, data, rating, password, photo 
                        FROM customer WHERE email = %s""",
                        (email,))

                user = cur.fetchone()
                print(user)

                if user and hashlib.sha224(password.encode()).hexdigest() == user[7]:
                    if user[8]:
                        photo_data_base64 = base64.b64encode(user[2]).decode()
                        session['data'] = {"id": user[0], 'photo': photo_data_base64, "roll": roll}
                    else:
                        session['data'] = {"id": user[0], "photo": None, "roll": roll}
                    session.permanent = True
                    conn.close()
                    return redirect('/')
                else:
                    flash("Вы ввели неправильный пароль или логин")
                    return redirect('/signin')

            except Exception as ex:
                logging.error(ex, exc_info=True)
                flash("Произошла ошибка при входе. Пожалуйста, попробуйте снова позже.")

            finally:
                conn.close()

    return render_template("sign_in.html")


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        sub_password = request.form.get('sub_password')

        if password != sub_password:
            return render_template('sign_up.html')

        password_hash = hashlib.sha224(password.encode()).hexdigest()
        roll = request.form.get('roll')

        conn = get_pg_connect()
        cur = conn.cursor()

        try:
            cur.execute(f"SELECT email FROM {roll}")
            existing_emails = [row[0] for row in cur.fetchall()]

            if email in existing_emails:
                conn.close()
                flash(f'Пользователь с почтой {email} уже зарегистрирован')
                return redirect('/')

            cur.execute(
                f"""INSERT INTO {roll} (username, email, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)""",
                (username, email, password_hash, first_name, last_name))

            conn.commit()
            conn.close()

            return redirect('/signin')
        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return f"Error: {ex}"

    return render_template('sign_up.html')


@app.route('/p', methods=['GET', 'POST'])
def p():
    if request.method == 'POST':
        photo = request.files['photo']

        if photo:
            photo_data = photo.read()
            conn = get_pg_connect()

            cursor = conn.cursor()
            try:
                jpg_data = resize_and_convert_to_jpg(photo_data)

                cursor.execute(
                    "UPDATE articles SET photo_data = %s WHERE id = 3",
                    (jpg_data,)
                )

                conn.commit()
                conn.close()
            except Exception as ex:
                logging.error(ex, exc_info=True)
                conn.rollback()
                conn.close()
                return f"Error:"

    return render_template('photo.html')


@app.route('/pp', methods=['GET', 'POST'])
def pp():
    if request.method == 'POST':
        photo = request.files['photo']

        if photo:
            photo_data = photo.read()
            conn = get_pg_connect()
            cursor = conn.cursor()
            try:
                jpg_data = profile_photo(photo_data)

                cursor.execute(
                    "UPDATE users SET photo = %s WHERE id = 4",
                    (jpg_data,)
                )

                conn.commit()
                conn.close()
            except Exception as ex:
                logging.error(ex, exc_info=True)
                conn.rollback()
                conn.close()
                return f"Error:"

    return render_template('photo.html')


@app.route('/profile_executor', methods=['GET', 'POST'])
def profile_executor():
    if session.get('data'):
        data = session.get('data')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT username, email, first_name, last_name, rating, specialty from executor 
WHERE id = %s""",
                (str(data['id'])))
            result = cur.fetchone()
            user_data = {
                'username': result[0],
                'email': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'rating': result[4],
                'skill': result[5]
            }
            cur.execute(
                """select title, description, price, date, skill, status from orders where customer_id = %s""",
                (str(data['id'])))

            orders_list = []
            for order in cur.fetchall():
                title, description, price, date_created, skill, status = order

                formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

                orders_list.append({
                    'title': title,
                    'description': description,
                    'price': price,
                    'date_created': formatted_date,
                    'skill': skill,
                    'status': status,
                })

            return render_template('executor/profile.html', user=user_data, )
        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return render_template('index.html')

    return render_template('index.html')


@app.route('/profile_executor_search/<id>', methods=['GET', 'POST'])
def profile_executor_search(id):
    conn = get_pg_connect()
    cur = conn.cursor()
    data = session.get('data')
    try:
        cur.execute(
            """SELECT username, email, first_name, last_name, rating, specialty, id from executor
WHERE id = %s""",
            (id,))
        result = cur.fetchone()
        user_data = {
            'username': result[0],
            'email': result[1],
            'first_name': result[2],
            'last_name': result[3],
            'rating': result[4],
            'skill': result[5],
            'id': result[6],
        }
        # cur.execute(
        #     """select title, description, price, date, skill, status from orders where customer_id = %s""",
        #     (str(data['id'])))
        #
        # orders_list = []
        # for order in cur.fetchall():
        #     title, description, price, date_created, skill, status = order
        #
        #     formatted_date = datetime.strftime(date_created, '%d-%m-%Y')
        #
        #     orders_list.append({
        #         'title': title,
        #         'description': description,
        #         'price': price,
        #         'date_created': formatted_date,
        #         'skill': skill,
        #         'status': status,
        #     })

        return render_template('executor/profile_search.html', user=user_data, executor_id=int(id),
                               id=int(str(data['id'])), roll=str(data['roll']))
    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return render_template('index.html')


@app.route('/profile_customer', methods=['GET', 'POST'])
def profile_customer():
    if session.get('data'):
        data = session.get('data')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT username, email, first_name, last_name from customer WHERE id = %s""",
                (str(data['id']))
            )
            result = cur.fetchone()
            user_data = {
                'username': result[0],
                'email': result[1],
                'first_name': result[2],
                'last_name': result[3],
            }
            cur.execute("""with test as (
                        SELECT o.id as order_id, COUNT(*) as comment_num
                        FROM executor_to_order eto
                        JOIN orders o ON eto.order_id = o.id
                        where eto.status = True
                        group by o.id
                        )
                        SELECT
                            o.id as order_id,
                            o.title,
                            o.description,
                            o.price,
                            o.date,
                            o.customer_id,
                            o.skill,
                            o.status,
                            (
                                SELECT comment_num
                                FROM test eto
                                WHERE o.id = eto.order_id
                            ) AS counter
                        FROM orders o
                        WHERE o.customer_id = %s;""",
                        (str(data['id']))
                        )
            active_orders_list = []
            for order in cur.fetchall():
                id, title, description, price, date_created, customer_id, skill, status, counter = order
                # Format the date as 'dd-mm-yyyy'
                formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

                active_orders_list.append({
                    'id': id,
                    'title': title,
                    'description': description,
                    'price': price,
                    'date_created': formatted_date,
                    'customer_id': customer_id,
                    'skill': skill,
                    'status': status,
                    'counter': counter
                })

            cur.execute("""with test as (
                        SELECT o.id as order_id, COUNT(*) as comment_num
                        FROM executor_to_order eto
                        JOIN orders o ON eto.order_id = o.id
                        where eto.status = False
                        group by o.id
                        )
                        SELECT
                            o.id as order_id,
                            o.title,
                            o.description,
                            o.price,
                            o.date,
                            o.customer_id,
                            o.skill,
                            o.status,
                            (
                                SELECT comment_num
                                FROM test eto
                                WHERE o.id = eto.order_id
                            ) AS counter
                        FROM orders o
                        WHERE o.customer_id = %s;""",
                        (str(data['id']))
                        )
            success_order_list = []
            for order in cur.fetchall():
                id, title, description, price, date_created, customer_id, skill, status, counter = order
                # Format the date as 'dd-mm-yyyy'
                formatted_date = datetime.strftime(date_created, '%d-%m-%Y')

                success_order_list.append({
                    'id': id,
                    'title': title,
                    'description': description,
                    'price': price,
                    'date_created': formatted_date,
                    'customer_id': customer_id,
                    'skill': skill,
                    'status': status,
                    'counter': counter
                })
            return render_template('customer/profile.html', user=user_data, active_orders=active_orders_list,
                                   success_order=success_order_list)
        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return redirect('/')

    return redirect('/')


@app.route('/del_session')
def del_session():
    session.pop('data', None)
    return redirect('/')


@app.route('/profile_customer_search/<id>')
def profile_customer_search(id):
    print(id)
    conn = get_pg_connect()
    cur = conn.cursor()
    data = session.get('data')
    try:
        cur.execute(
            """SELECT email, username, last_name, first_name, id from customer WHERE id = %s""", (id,))
        result = cur.fetchone()
        customer_dict = {
            'email': result[0],
            'username': result[1],
            'last_name': result[2],
            'first_name': result[3],
            'id': result[4]
        }

        cur.execute("""with test as (
                        SELECT o.id as order_id, COUNT(*) as comment_num
                        FROM executor_to_order eto
                        JOIN orders o ON eto.order_id = o.id
                        where eto.status = True
                        group by o.id
                        )
                        SELECT
                            o.id as order_id,
                            o.title,
                            o.description,
                            o.price,
                            o.date,
                            o.customer_id,
                            o.skill,
                            o.status,
                            (
                                SELECT comment_num
                                FROM test eto
                                WHERE o.id = eto.order_id
                            ) AS counter
                        FROM orders o
                        WHERE o.customer_id = %s;""",
                    (int(id),)
                    )
        orders_list = []
        for order in cur.fetchall():
            id, title, description, price, date_created, customer_id, skill, status, counter = order
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
                'counter': counter
            })

        return render_template('customer/profile_search.html', user=customer_dict, orders=orders_list,
                               customer_id=int(id), id=int(str(data['id'])), roll=data['roll'])

    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return "Ошибка при получении статей из базы данных"


@app.route("/contact", methods=["GET", "POST", ])
def contact():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        message = request.form.get("message")
        msg = Message("Вам поступило новое обращение на сайте", sender='frilansplace@gmail.com', recipients=[email])
        msg.html = render_template('email_send.html', name=name, message=message)
        mail.send(msg)
        flash("Спасибо большое за обраную связь, мы обязательно с вами свяжемся!!!")
        return redirect('/')
    else:
        flash("Произошла ошибка")
        return redirect('/')


@app.route('/profile_executor/edit', methods=['POST', "GET", ])
def profile_executor_edit():
    if request.method == 'POST':
        if session.get('data'):
            data = session.get('data')
            conn = get_pg_connect()
            cur = conn.cursor()
            email = request.form.get('email')
            cur.execute("SELECT email FROM executor WHERE id != %s", str(data['id']))
            existing_emails = [row[0] for row in cur.fetchall()]
            if email in existing_emails:
                conn.close()
                flash(f'Пользователь с почтой {email} уже зарегистрирован')
                return redirect('/executor/profile')
            username = request.form.get('username')
            last_name = request.form.get('last_name')
            first_name = request.form.get('first_name')
            skill = request.form.get('skill')
            cur.execute("""
                UPDATE executor
                SET username = %s, last_name = %s, first_name = %s, specialty = %s, email = %s
                WHERE id = %s
            """, (username, last_name, first_name, skill, email, str(data['id'])))
            conn.commit()
            return redirect('/profile_executor')
    if session.get('data'):
        data = session.get('data')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT username, email, first_name, last_name, rating, specialty from executor 
WHERE id = %s""",
                (str(data['id'])))
            result = cur.fetchone()
            user_data = {
                'username': result[0],
                'email': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'rating': result[4],
                'skill': result[5]
            }
            return render_template('executor/profile_edit.html', user=user_data)
        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return redirect('/')
    return redirect('/')


@app.route('/profile_customer/edit', methods=['POST', "GET", ])
def profile_customer_edit():
    if request.method == 'POST':
        if session.get('data'):
            data = session.get('data')
            conn = get_pg_connect()
            cur = conn.cursor()
            email = request.form.get('email')
            cur.execute("SELECT email FROM customer WHERE id != %s", str(data['id']))
            existing_emails = [row[0] for row in cur.fetchall()]
            if email in existing_emails:
                conn.close()
                flash(f'Пользователь с почтой {email} уже зарегистрирован')
                return redirect('/profile_executor')
            username = request.form.get('username')
            last_name = request.form.get('last_name')
            first_name = request.form.get('first_name')
            cur.execute("""
                UPDATE customer
                SET username = %s, last_name = %s, first_name = %s, email = %s
                WHERE id = %s
            """, (username, last_name, first_name, email, str(data['id'])))
            conn.commit()
            return redirect('/profile_customer')
    if session.get('data'):
        data = session.get('data')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT username, email, first_name, last_name, rating from customer 
WHERE id = %s""",
                (str(data['id'])))
            result = cur.fetchone()
            user_data = {
                'username': result[0],
                'email': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'rating': result[4],
            }

            return render_template('customer/profile_edit.html', user=user_data)
        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return redirect('/')
    return redirect('/')


@app.route('/customer/add_orders', methods=['POST', 'GET', ])
def new_orders():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        description = request.form.get('descriptions')
        full_description = request.form.get('full_descriptions')
        data = session.get('data')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO orders (title, price, description, full_description, customer_id)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (title, price, description, full_description, str(data['id'])))
            conn.commit()
            return redirect('/profile_customer')

        except Exception as ex:
            logging.error(ex, exc_info=True)
            conn.rollback()
            conn.close()
            return redirect('/')

    return render_template('new_orders.html')


@app.route('/add_order/<id>')
def add_order(id):
    if not session.get('data'):
        return redirect('/signin')
    conn = get_pg_connect()
    cur = conn.cursor()
    data = session.get('data')
    try:
        cur.execute('select email from executor where id = %s', (str(data['id'])))
        email_executor = cur.fetchone()[0]
        print(email_executor)
        cur.execute("""
        select c.email from orders o 
join customer c on c.id = o.customer_id 
where o.id = %s""", (id,))
        customer_email = cur.fetchone()[0]
        msg = Message("Вам поступило новое обращение на сайте", sender='frilansplace@gmail.com',
                      recipients=[customer_email])
        msg.html = render_template('email_orders_add.html', email=email_executor)
        mail.send(msg)
        cur.execute("""
                INSERT INTO executor_to_order (order_id, executor_id)
                VALUES (%s, %s)""", (id, str(data['id'])))
        conn.commit()
        flash("Спасибо большое за обраную связь, мы обязательно с вами свяжемся!!!")
        return redirect('/profile_executor')
    except Exception as ex:
        logging.error(ex, exc_info=True)
        conn.rollback()
        conn.close()
        return redirect('/')


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    if session.get('data'):
        return redirect('/')
    if request.method == 'POST':
        email = request.form.get('email')
        roll = request.form.get('roll')
        conn = get_pg_connect()
        cur = conn.cursor()
        try:
            cur.execute(f"""select id from {roll} where email = %s""", (email,))
            id = cur.fetchone()[0]
            session['token'] = {'token': generate_secure_string(), 'roll': roll, 'id': id}
            flash('На вашу почту было направлено письмо с новым паролем')
            msg = Message("Вам поступило новое обращение на сайте", sender='frilansplace@gmail.com', recipients=[email])
            msg.html = render_template('email_reset_password.html', hash=session.get('token')['token'])
            mail.send(msg)
        except Exception as ex:
            flash("Пользователя с почтой %s не существует", email)
            conn.rollback()
            conn.close()
            return redirect('/')

    return render_template('reset_password.html')


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    sub_token = session.get('token')
    if token == sub_token['token']:
        if request.method == 'POST':
            conn = get_pg_connect()
            cur = conn.cursor()
            if request.form.get('password') != request.form.get('sub_password'):
                return redirect('/')
            try:
                cur.execute(f"""UPDATE {session.get('token')['roll']} 
                SET password = %s
                WHERE id = %s""", (
                    hashlib.sha224((request.form.get('password').encode())).hexdigest(),
                    session.get('token')['id']))
                conn.commit()
                session.pop('token', None)
                return redirect('/signin')
            except Exception as ex:
                logging.error(ex, exc_info=True)
                conn.rollback()
                conn.close()
                return redirect('/signup')
        return render_template('reset_passwd_submit.html')
    return redirect('/')


@app.route('/del_session_token')
def del_session_token():
    session.pop('token', None)
    return redirect('/')


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
