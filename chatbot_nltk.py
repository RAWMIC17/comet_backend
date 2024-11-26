import nltk
import re

# Ensure necessary NLTK data is available
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Function to load college data from file with error handling
def load_college_data(file_path):
    college_data = {}
    current_university = None

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line.lower().startswith("university:"):
                    current_university = line.split(":")[1].strip().lower()
                    college_data[current_university] = {}
                elif ":" in line and current_university:
                    key, value = line.split(":", 1)
                    college_data[current_university][key.strip().lower()] = value.strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return college_data

# Function to create a regex pattern for matching college names
def create_college_pattern(college_data):
    college_names = list(college_data.keys())
    escaped_college_names = [re.escape(college) for college in college_names]
    college_pattern = r"\b(" + "|".join(escaped_college_names) + r")\b"
    return college_pattern

# Function to get the details of a specific college based on user input
def get_college_details(college_data, college_name, detail_type=None):
    college_name = college_name.lower()
    if college_name in college_data:
        details = college_data[college_name]

        if detail_type:
            detail = details.get(detail_type, 'N/A')
            return f"{detail_type.title()}: {detail}"

        # Construct a detailed response if no specific detail is requested
        return (
            f"University: {college_name.title()}\n"
            f"Course Fees: {details.get('course fees', 'N/A')}\n"
            f"Hostel Fees: {details.get('hostel fees', 'N/A')}\n"
            f"Total Fees: {details.get('total fees', 'N/A')}\n"
            f"Placement Rate: {details.get('placement rate', 'N/A')}\n"
            f"Average Salary: {details.get('average salary', 'N/A')}\n"
        )
    else:
        return "Sorry, I couldn't find the college you're asking for."

# Function to process the chatbot response
def chatbot_response(message, file_path):
    # Load the college data
    college_data = load_college_data(file_path)
    
    if not college_data:
        return "College data is unavailable."

    college_pattern = create_college_pattern(college_data)

    # Use regex to find the college name in the user's query
    match = re.search(college_pattern, message, re.IGNORECASE)

    if match:
        college_name = match.group(0)

        # Check if specific detail is requested
        detail_type = None
        if "fees" in message.lower():
            if "course" in message.lower():
                detail_type = "course fees"
            elif "hostel" in message.lower():
                detail_type = "hostel fees"
            else:
                detail_type = "total fees"
        elif "placement" in message.lower():
            detail_type = "placement rate"
        elif "salary" in message.lower():
            detail_type = "average salary"

        response = get_college_details(college_data, college_name, detail_type)
    else:
        response = "Sorry, I couldn't understand the college name. Please try again."

    return response
