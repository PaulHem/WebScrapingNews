from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv
import time
class LeFigaroScraper:
    def __init__(self):
        load_dotenv()
        profile_path = os.getenv('CHROME_PROFILE_PATH')
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument(f"user-data-dir={profile_path}") 
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get('https://connect.lefigaro.fr/login?client=horizon_web&type=main&redirect_uri=https://www.lefigaro.fr/')
        time.sleep(1)
        try:
            # Try to find the element
            self.driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(os.getenv('EMAIL_LE_FIGARO'))
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('PASSWORD_LE_FIGARO'))
            self.driver.find_element(By.XPATH, '//*[@id="wrapper"]/section/div/div/div[2]/form/div[3]/button').click()
            print("Login has been done.")
        except NoSuchElementException:
            print("Already logged in.")

    def retrieve_comments(self, article_url):
        # Implement your comments retrieval logic here
        # Use self.self.driver to navigate to the article page and extract the comments
        comment_texts = []
        #Get number of Comment-Pages
        self.driver.get(article_url)
        wait = WebDriverWait(self.driver, 10)
        comment_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-toggle-figcomments')))
        comment_button.click()
        
        ## Scroll down to load all comments
        wait = WebDriverWait(self.driver, 10)
        comment_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'figc__wrapper')))
        # Scroll the div until the end
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", comment_wrapper)

        while True:
            # Scroll down
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", comment_wrapper)
            time.sleep(2)  # wait for content to load

            # Calculate new scroll height and compare with last height
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", comment_wrapper)
            if new_height == last_height:
                break
            last_height = new_height
        comments = comment_wrapper.find_elements(By.CLASS_NAME, 'figc-comment')
        self.driver.execute_script("arguments[0].scrollIntoView();", comments[0])
        time.sleep(3)
        for comment in comments:
            comment_texts.append(self.retrieve_metadata(comment))
            comment_texts.extend(self.retrieve_replies(comment))
            
        return comment_texts
            
            
            
            
            
    def retrieve_replies(self, comment):
        replies_text = []
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", comment)
            time.sleep(0.3)
            button_expand = comment.find_element(By.CLASS_NAME, 'figc-comment__link--responses')
            button_expand.click()
            time.sleep(1)
            replies = comment.find_elements(By.CLASS_NAME, 'figc-comment')
            print("found replies")
            print(len(replies))
            for reply in replies:
                replies_text.append(self.retrieve_metadata(reply))
                replies_text.extend(self.retrieve_replies(reply))
            return replies_text
        except:
            return []
        
    def retrieve_metadata(self, comment):
        user_name_data = comment.find_element(By.CLASS_NAME, 'figc-comment__username').text
        date_data = comment.find_element(By.CLASS_NAME, 'figc-comment__date').text
        text_data = comment.find_element(By.CLASS_NAME, 'figc-comment__text').text
        return {'text':text_data.replace('\n', '').replace('\r', ''), 'user_name': user_name_data, 'date': date_data}