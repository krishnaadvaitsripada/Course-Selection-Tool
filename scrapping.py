import requests
from bs4 import BeautifulSoup
import boto3

def scrape_course_data():
    # URL of the course search page
    url = 'https://engineering.calendar.utoronto.ca/search-courses'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all course entries
        course_entries = soup.find_all('div', class_='views-row')

        # Initialize a list to store course data
        course_data = []

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

        return course_data
    else:
        print('Failed to retrieve data from the website')
        return None

def save_to_dynamodb(data):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    
    # Get the DynamoDB table
    table = dynamodb.Table('Courses')

    # Loop through each course data and save to DynamoDB
    for course in data:
        table.put_item(Item=course)
    
    print('Data saved to DynamoDB')

# Call the function to scrape course data
course_data = scrape_course_data()

# Print the scraped course data
if course_data:
    for course in course_data:
        print(course)

    # Save the scraped course data to DynamoDB
    save_to_dynamodb(course_data)
