import os
import unittest

from dotenv import load_dotenv

from main import app  # Import your Flask app
from flask_testing import TestCase


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

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 302)

    def test_del_session(self):
        response = self.client.get('/del_session')
        self.assertEqual(response.status_code, 302)

    def test_contact(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 302)

    # def test_contact_post(self):
    #     with self.client:
    #         response = self.client.post('/contact', data={
    #             'email': 'test@example.com',
    #             'name': 'Test User',
    #             'message': 'This is a test message'
    #         })
    #
    #         self.assertRedirects(response, '/')

    def test_sign_in_post(self):
        with self.client:
            response = self.client.post('/signin', data={
                'email': 'test@example.com',
                'password': 'alert'
            })

            self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
