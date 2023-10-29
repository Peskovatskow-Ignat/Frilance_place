from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class TestPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:5000/")  # Замените на ваш URL

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_check_menu_items(self):
        menu_items = self.driver.find_elements(By.CSS_SELECTOR, '.u-nav-1 .u-nav-link')
        self.assertTrue(len(menu_items) == 3)

    def test_check_search_form(self):
        search_form = self.driver.find_element(By.CSS_SELECTOR, '.u-search-1')
        self.assertTrue(search_form.is_displayed())

    def test_navigation(self):
        # Перейдем на страницу Orders
        orders_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Orders')
        orders_link.click()
        # Проверим, что мы на нужной странице (например, по заголовку)
        expected_title = "Orders"  # Замените на ожидаемый заголовок
        self.assertEqual(self.driver.title, expected_title)

    def test_search_functionality(self):
        search_input = self.driver.find_element(By.NAME, 'title')
        search_input.send_keys('test')  # Введите тестовый запрос
        search_button = self.driver.find_element(By.CSS_SELECTOR, '.u-search-button')
        search_button.click()
        # Проверьте, что результаты поиска отображаются корректно
        # (например, проверьте список результатов)

if __name__ == '__main__':
    unittest.main()
