from flask import Flask, jsonify
import os

app = Flask(__name__)

# Function to read the data file and structure it
def read_college_data():
    data = []
    file_path = r'C:\Users\hks17\OneDrive\Desktop\Chatbot\college_corpus.txt'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            college_info = {}
            for line in file:
                line = line.strip()
                if line:
                    try:
                        key, value = line.split(': ', 1)  # Split at first ": "
                        key = key.strip()  # Trim any extra spaces
                        value = value.strip()  # Trim any extra spaces
                        if key == "University":
                            if college_info:  # If previous college exists, add it to data
                                data.append(college_info)
                            college_info = {"University": value}
                        else:
                            college_info[key] = value
                    except ValueError:
                        print(f"Skipping malformed line: {line}")
            if college_info:  # Add last college
                data.append(college_info)
    else:
        print("College data file not found.")
    return data


@app.route('/', methods=['GET'])
def index():
    colleges = read_college_data()
    return jsonify(colleges)  # Return JSON response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
