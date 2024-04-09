from flask import Flask, render_template, request, jsonify
import boto3
from uuid import uuid4  # For generating unique filenames
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize S3 client
s3 = boto3.client(
    's3',
    region_name='ap-south-1',  # Specify your AWS region
    aws_access_key_id="access_key",  # Use environment variables
    aws_secret_access_key="secret-access-key"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/track', methods=['POST'])
def track_activity():
    try:
        # Get activity data from request payload
        activity_data = request.get_json()

        # Generate a unique filename for the JSON file
        filename = f"activity_{uuid4()}.json"

        # Upload user activity data to S3 bucket with the unique filename
        bucket_name = 'fccweather'  # Replace with your S3 bucket name

        response = s3.put_object(
            Body=str(activity_data),  # Convert activity_data to string (or use json.dumps)
            Bucket=bucket_name,
            Key=filename  # Use the generated filename as the S3 object key
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return jsonify({'message': f'User activity stored successfully as {filename}'}), 200
        else:
            return jsonify({'error': 'Failed to store user activity'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
