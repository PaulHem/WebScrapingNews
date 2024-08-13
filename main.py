from le_monde_scraper import LeMondeScraper

scraper = LeMondeScraper()
scraper.login()
comments = scraper.retrieve_comments("https://www.lemonde.fr/emploi/article/2023/06/27/les-maladies-professionnelles-des-salaries-ages-ne-penaliseront-plus-leurs-employeurs_6179358_1698637.html")


file_path = 'output_comments.txt'

# Open the file in write mode
with open(file_path, 'w', encoding='utf-8') as file:
    # Iterate over the string array and write each string to the file
    for line in comments:
        line_without_linebreaks = line.replace('\n', '').replace('\r', '')
        file.write(line_without_linebreaks + '\n')  # Add a newline character after each line
