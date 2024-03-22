import requests
from bs4 import BeautifulSoup
import boto3
import csv

def scrape_course_data():
    # URL of the course search page
    url_ece_0 = 'https://engineering.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=Electrical%20and%20Computer%20Engineering&field_subject_area_target_id=All&page=0'
    url_ece_1 = 'https://engineering.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=Electrical%20and%20Computer%20Engineering&field_subject_area_target_id=All&page=1'
    url_ece_2 = 'https://engineering.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=Electrical%20and%20Computer%20Engineering&field_subject_area_target_id=All&page=2'
    url_ece_3 = 'https://engineering.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value=Electrical%20and%20Computer%20Engineering&field_subject_area_target_id=All&page=3'

    url_ece_list = [url_ece_0, url_ece_1, url_ece_2, url_ece_3]

    # Initialize a list to store course data
    course_data = []

    # Send a GET request to the URL
    for url in url_ece_list: 
        response = requests.get(url)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all course entries
            course_entries = soup.find_all('div', class_='views-row')

            # Loop through each course entry
            for entry in course_entries:
                # Extract course code, name, and description
                course_info = {}

                # Course code and name
                course_header = entry.find('h3', class_='js-views-accordion-group-header')
                if course_header:
                    course_code_name = course_header.find('div').get_text(separator=' ', strip=True).split(' - ')
                    if len(course_code_name) == 2:
                        course_info['CourseCode'] = course_code_name[0]
                        course_info['CourseName'] = course_code_name[1]

                # Course description
                course_description = entry.find('div', class_='views-field-field-desc')
                if course_description:
                    course_info['Description'] = course_description.find('div', class_='field-content').get_text(strip=True)

                # Append course info to the list if all data is available
                if all(course_info.values()):
                    course_data.append(course_info)

        else:
            print('Failed to retrieve data from the website')
            return None
        
    return course_data

def export_to_csv(data, filename):
    # Specify the CSV file path
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define CSV writer
        csv_writer = csv.writer(csvfile)
        
        # Write header row
        csv_writer.writerow(['CourseCode', 'CourseName', 'Description'])
        
        # Write data rows
        for row in data:
            course_code = row.get('CourseCode', '')  # Default to empty string if 'CourseCode' key is not found
            course_name = row.get('CourseName', '')  # Default to empty string if 'CourseName' key is not found
            description = row.get('Description', '')  # Default to empty string if 'Description' key is not found
            
            csv_writer.writerow([course_code, course_name, description])


# Call the function to scrape course data
course_data = scrape_course_data()

# Specify the file name for CSV export
csv_filename = 'course_data.csv'

# Export data to CSV
if course_data:
    export_to_csv(course_data, csv_filename)
    print(f'Data exported to {csv_filename}')
else:
    print('No data to export')

