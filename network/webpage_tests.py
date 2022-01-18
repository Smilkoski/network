from unittest import TestCase

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


class WebpageTests(TestCase):

    def test_title(self):
        """Make sure title is correct"""
        driver.get('http://127.0.0.1:8000')
        self.assertEqual(driver.title, "Social Network")

    def test_login(self):
        driver.get('http://127.0.0.1:8000/login/')
        driver.find_elements_by_class_name('form-control')[0].send_keys('Hristijan')
        driver.find_elements_by_class_name('form-control')[1].send_keys('testing321')
        driver.find_element_by_class_name('btn').click()

    def test_post(self):
        """Test posting article, and number of articles"""
        self.test_login()
        driver.get('http://127.0.0.1:8000')
        driver.find_element_by_id('id_content').send_keys('Test Test Test Test Test Test Test ')

        articles = driver.find_elements_by_tag_name('article')
        self.assertEqual(len(articles), 10)

        driver.find_element_by_tag_name('button').click()

        articles = driver.find_elements_by_tag_name('article')
        self.assertEqual(len(articles), 10)

    def get_first_post_url(self):
        self.test_login()
        driver.get('http://127.0.0.1:8000')
        posts = driver.find_elements_by_tag_name('article > div > a')

        attrs = driver.execute_script(
            'var items = {}; \
            for (index = 0; index < arguments[0].attributes.length; ++index) { \
              items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; \
              return items;', posts[0])
        return attrs['href']

    def test_like(self):
        """Test like button on random post"""
        url = self.get_first_post_url()
        driver.get(f'http://127.0.0.1:8000{url}')
        before_num_likes = int(driver.find_element_by_class_name('num_likes').get_attribute('innerHTML'))
        # click like
        driver.find_element_by_tag_name('svg').click()
        after_num_likes = int(driver.find_element_by_class_name('num_likes').get_attribute('innerHTML'))

        # difference before and after click should be 1
        self.assertEqual(abs(before_num_likes - after_num_likes), 1)

    def test_edit(self):
        """Test edit button on random post"""
        url = self.get_first_post_url()
        driver.get(f'http://127.0.0.1:8000{url}')
        # click edit button
        driver.find_element_by_id('edit').click()
        element = driver.find_element_by_id('compose-content')
        # write new content
        driver.execute_script("arguments[0].innerHTML = arguments[1]", element, 'Test Test Test Test Test')
        # click save button
        driver.find_element_by_tag_name('input').click()

    def test_pagination(self):
        self.test_login()
        driver.get('http://127.0.0.1:8000')

        driver.find_element_by_link_text('1').click()
        driver.find_element_by_link_text('2').click()
        driver.find_element_by_link_text('3').click()
        driver.find_element_by_link_text('4').click()
        driver.find_element_by_link_text('Previous').click()
        driver.find_element_by_link_text('Previous').click()
        driver.find_element_by_link_text('First').click()
        driver.find_element_by_link_text('Next').click()
        driver.find_element_by_link_text('Next').click()
        driver.find_element_by_link_text('Last').click()
