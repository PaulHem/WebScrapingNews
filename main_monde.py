from le_monde_scraper import LeMondeScraper

scraper = LeMondeScraper()
scraper.login()


#Define the path to the file with the articles
file_path = 'LeMonde_filtered.txt'
i = 0
# Open the file and process each line
with open(file_path, 'r') as file:
    for line in file:
        # Remove any leading/trailing whitespace (like newline characters)
        line = line.strip()
        #read all comments for the article
        comments = scraper.retrieve_comments(line)
        
        print(line)
        
        #Define Output File Path
        write_path = f'comments\\{i}_output_comments.txt'

        # Open the file in write mode
        with open(write_path, 'w', encoding='utf-8') as file:
            # Iterate over the string array and write each string to the file
            for line in comments:
                #Remove any linebreaks in the comment
                line_without_linebreaks = line.replace('\n', '').replace('\r', '')
                # Write the comment to the file
                file.write(line_without_linebreaks + '\n')  # Add a newline character after each line
        i += 1
