import json
import boto3
import csv
import io

# Create an S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract the bucket and file name from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    output_bucket = 'your-output-bucket'  # Replace with your output bucket name

    try:
        # Get the file from the source S3 bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        
        # Read the file content (assuming it is in a format like JSON, TSV, etc. to convert into CSV)
        file_content = response['Body'].read().decode('utf-8')
        
        # If the input file is JSON, for example, convert it to CSV format (adjust as needed)
        data = json.loads(file_content)
        
        # Convert JSON data to CSV format using StringIO
        output_csv = io.StringIO()
        csv_writer = csv.DictWriter(output_csv, fieldnames=data[0].keys())
        
        # Write CSV header
        csv_writer.writeheader()
        
        # Write the rows
        for row in data:
            csv_writer.writerow(row)
        
        # Now save the CSV data into another S3 bucket
        output_csv.seek(0)  # Reset the StringIO cursor to the beginning
        
        output_key = source_key.replace('.json', '.csv')  # Adjust the output file name
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=output_csv.getvalue())
        
        return {
            'statusCode': 200,
            'body': json.dumps('File conversion and upload successful!')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }
