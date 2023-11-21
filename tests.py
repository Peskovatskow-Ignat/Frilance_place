import json
import os
import unittest

from dotenv import load_dotenv

from functions import generate_secure_string, resize_and_convert_to_jpg, profile_photo
from main import app  # Import your Flask app
from flask_testing import TestCase
from PIL import Image
from io import BytesIO


class TestYourApp(TestCase):

    def create_app(self):
        load_dotenv()
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        app.config["JSON_AS_ASCII"] = True
        app.config["MAIL_SERVER"] = 'smtp.gmail.com'
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

        return app

    def setUp(self):
        # Set up a test client
        self.app = self.create_app().test_client()
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.test_image_data = BytesIO()
        self.test_image.save(self.test_image_data, format='PNG')
        self.test_image_data.seek(0)

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_route_customer(self):
        self.client.post('/signin', data={
            'email': 'test@example.com',
            'password': 'password',
            'roll': 'customer'
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.client.get('/del_session')

    def test_index_route_executor(self):
        self.client.post('/signin', data={
            'email': 'test@example.com',
            'password': 'password',
            'roll': 'executor'
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.client.get('/del_session')

    def test_index_route_bed(self):
        self.client.post('/signin', data={
            'email': 'test@example.com',
            'password': 'password',
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.client.get('/del_session')

    def test_orders_skill_route(self):
        for value in ['development', 'testing', 'seo', 'management', 'ads', 'design']:
            response = self.client.get(f'/orders/{value}')  # Replace 'some_skill' with an actual skill
            self.assertEqual(response.status_code, 200)
        # Add assertions to check the content of the response

    def test_order_route(self):
        response = self.client.get('/orders')  # Replace '1' with an actual order ID
        self.assertEqual(response.status_code, 200)
        # Add assertions to check the content of the response

    def test_sign_in(self):
        response = self.client.get('/signin')
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_profile_executor(self):
        response = self.client.get('/profile_executor')
        self.assertEqual(response.status_code, 200)

    def test_profile_customer(self):
        response = self.client.get('/profile_customer')
        self.assertEqual(response.status_code, 200)

    def test_del_session(self):
        response = self.client.get('/del_session')
        self.assertEqual(response.status_code, 302)

    # def test_contact_post(self):
    #     # with self.client:
    #     response = self.client.post('/contact', data={
    #         'email': 'test@example.com',
    #         'name': 'Test User',
    #         'message': 'This is a test message'
    #     })
    #
    #     self.assertRedirects(response, '/')

    def test_order_number(self):
        with self.client:
            self.client.post('/signup', data={
                'email': 'test@example.com',
                'username': 'test',
                'first_name': 'Test User',
                'last_name': 'Test User',
                'password': 'password',
                'sub_password': 'password',
                'roll': 'customer'
            })
            self.client.post('/signin', data={
                'email': 'test@example.com',
                'password': 'password',
                'roll': 'customer'
            })
            self.client.post('/customer/add_orders', data={
                'title': 'Test Order',
                'price': 122,
                'description': 'Test Order Description',
                'full_description': 'Test Order Full Description',
                'skill': 'test',
            })
            response = self.client.get('/order/1')

            self.client.get('dell_session')
            self.assertEqual(response.status_code, 200)

    def test_sign_in_post(self):
        with self.client:
            response = self.client.post('/signin', data={
                'email': 'test@example.com',
                'password': 'alert'
            })

            self.assertEqual(response.status_code, 302)

    def test_sign_ip_post(self):
        with self.client:
            response = self.client.post('/signup', data={
                'email': 'test@example.com',
                'username': 'test',
                'first_name': 'Test User',
                'last_name': 'Test User',
                'password': 'password',
                'sub_password': 'password',
                'roll': 'executor'
            })
            self.assertEqual(response.status_code, 302)

    def test_add_order(self):
        response = self.client.get('/customer/add_orders')
        self.assertEqual(response.status_code, 200)

    def test_add_order_post(self):
        with self.client:
            self.client.post('/signup', data={
                'email': 'test@example.com',
                'username': 'test',
                'first_name': 'Test User',
                'last_name': 'Test User',
                'password': 'password',
                'sub_password': 'password',
                'roll': 'customer'
            })
            self.client.post('/signin', data={
                'email': 'test@example.com',
                'password': 'password',
                'roll': 'customer'
            })
            response = self.client.post('/customer/add_orders', data={
                'title': 'Test Order',
                'price': 122,
                'description': 'Test Order Description',
                'full_description': 'Test Order Full Description',
                'skill': 'test',
            })

            self.assertEqual(response.status_code, 302)
            self.client.get('/del_session')

    def test_generate_secure_string_length(self):
        length = 10
        secure_string = generate_secure_string(length)
        self.assertEqual(len(secure_string), length)

    def test_generate_secure_string_default_length(self):
        secure_string = generate_secure_string()
        self.assertEqual(len(secure_string), 50)

    def test_generate_secure_string_contains_only_letters(self):
        secure_string = generate_secure_string()
        self.assertTrue(secure_string.isalpha())

    def test_resize_and_convert_to_jpg(self):
        jpg_data = resize_and_convert_to_jpg(self.test_image_data.getvalue())
        image = Image.open(BytesIO(jpg_data))
        self.assertEqual(image.format, 'JPEG')
        self.assertEqual(image.size, (1080, 1024))

    def test_profile_photo(self):
        jpg_data = profile_photo(self.test_image_data.getvalue())
        image = Image.open(BytesIO(jpg_data))
        self.assertEqual(image.format, 'JPEG')
        self.assertEqual(image.size, (75, 75))

    def test_api_orders_without_token(self):
        response = self.client.get('api/orders')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior when no token is provided

    def test_api_order_without_token(self):
        response = self.client.get('api/order/1')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior when no token is provided

    def test_api_order_query_without_token(self):
        response = self.client.get('api/order?id=1')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior when no token is provided

    def test_auth_without_token(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "key": app.config["SECRET_KEY"]
        }
        response = self.client.post('api/auth', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.token = response_data.get("token")
        # Add more assertions based on the expected behavior when no token is provided

    def test_get_customer_without_token(self):
        response = self.client.get('api/get_customer')
        self.assertEqual(response.status_code, 401)
        # Add more assertions based on the expected behavior when no token is provided

    def test_api_orders_with_valid_token(self):
        if not hasattr(self, 'token'):
            # If the token is not set, run the authentication test to obtain it
            self.test_auth_without_token()

        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/orders', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
