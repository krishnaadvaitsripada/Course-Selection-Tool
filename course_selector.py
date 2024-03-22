import json
import boto3
import csv
import io


boto3_bedrock = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # TODO implement
    print("boto3 version:"+boto3.__version__)
    
    # Initialize Boto3 client for S3
    s3 = boto3.client('s3')
    
    # Retrieve CSV content from S3
    response = s3.get_object(Bucket='hackthestudentlifeteam20-2', Key='course_data.csv')
    csv_content = response['Body'].read().decode('utf-8')
    
    # Parse CSV content without Pandas
    csv_data = csv.reader(io.StringIO(csv_content))
    course_dict = {}
    for i, row in enumerate(csv_data):
        if i >= 200:  # Stop after processing 10 rows
            break
        if not row[0]:
            continue
        course_code = row[0]  # Course code is the first element in the row
        description = row[2]  # Description is the second element in the row
        prompt_data='''I will give you a course name and their description. Categorize the course into one of the following categories: Software development, Artificial Intelligence/Machine Learning,
        Cybersecurity, Business, Robotics, Data Science, Networks and Telecommunications, Cloud Computing. Give the output in the following format: Course code->Category. Only output the format so that I can later add this into an array.'''
        
        prompt_data += f"Course Code: {course_code}\nDescription: {description}\n\n"
        body = json.dumps({"prompt": "Human:"+prompt_data+"\nAssistant:", "max_tokens_to_sample":2000})
        modelId='anthropic.claude-v2'
        accept = 'application/json'
        contentType = 'application/json'
        response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get('body').read())
        completion_string = response_body.get('completion', '')
        
        parts = completion_string.split('->')
        if len(parts) != 2:
            # If the input string doesn't match the expected format, return None for both values
            return None, None
        # Remove leading/trailing whitespaces from the extracted parts
        course_code = parts[0].strip()
        course_category = parts[1].strip()
        if course_code and course_category:
            course_dict[course_code] = course_category
    
    #print(course_dict)
    selected_category = 'cybersecurity'
    print("Here are the courses that are related to", selected_category + ":")    
    for course_code, course_category in course_dict.items():
        if course_category.lower() == selected_category:
            print(course_code) 
    
    #formatting body for Jurassic models
    #body = json.dumps({"prompt": prompt_data, "maxTokens":500})
    
    #formatting body for claude
    
    
    #set model
    #modelId='ai21.j2-ultra-v1'
    
    
    #invoke model
    
    
   

    
    # Extract course names and their categories using regular expressions
    #courses = re.findall(r'(\w+\d+\w*)\:.*?(Software development|Artificial Intelligence/Machine Learning|Cybersecurity|Business|Robotics|Data Science|Networks and Telecommunications|Cloud Computing)', prompt_data)

    # Create a dictionary to store course names and their categories
    #course_categories = {}
    #for course, category in courses:
     #   course_categories[course] = category

    #print(course_categories)

    
    return {
        'statusCode': 200,
        'body': json.dumps('Bedrock is awesome')
    }
