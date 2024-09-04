import csv
from le_figaro_scraper import LeFigaroScraper

scraper = LeFigaroScraper()
scraper.login()
#comments = scraper.retrieve_comments('https://www.lefigaro.fr/politique/il-a-fait-ca-dans-son-coin-les-coulisses-de-la-declaration-de-candidature-anticipee-d-edouard-philippe-a-la-presidentielle-20240904')
comments = scraper.retrieve_comments('https://www.lefigaro.fr/politique/course-a-matignon-ca-me-fait-penser-aux-feux-de-l-amour-ironise-fabien-roussel-20240904')
print(comments)
print(len(comments))