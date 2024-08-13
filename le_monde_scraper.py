from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv
import time
class LeMondeScraper:
    def __init__(self):
        load_dotenv()
        profile_path = os.getenv('CHROME_PROFILE_PATH')
        options = Options()
        options.add_argument(f"user-data-dir={profile_path}") 
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get('https://secure.lemonde.fr/sfuser/connexion')
        time.sleep(1)
        try:
            # Try to find the element
            self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(os.getenv('EMAIL_LE_MONDE'))
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('PASSWORD_LE_MONDE'))
            self.driver.find_element(By.XPATH, '//*[@id="login"]/main/form/div[4]/input').click()
            print("Login has been done.")
        except NoSuchElementException:
            print("Already logged in.")

    def retrieve_comments(self, article_url):
        # Implement your comments retrieval logic here
        # Use self.self.driver to navigate to the article page and extract the comments
        comment_texts = []
        #Get number of Comment-Pages
        contributions_url = article_url+'?contributions'
        self.driver.get(contributions_url)
        time.sleep(1)
        pagination_items = self.driver.find_elements(By.CLASS_NAME, 'pagination__item')
        number_of_comment_pages = len(pagination_items)
        if number_of_comment_pages == 0:
            number_of_comment_pages = 1
        for i in range(number_of_comment_pages):
            comment_page_url = contributions_url + f'&page={i+1}'
            print(comment_page_url)
            self.driver.get(comment_page_url)
            wait = WebDriverWait(self.driver, 10)
            comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'comment')))
            for comment in comments:
                comment_texts.append(comment.find_element(By.CLASS_NAME, 'comment__content').get_attribute('textContent'))
        return comment_texts

