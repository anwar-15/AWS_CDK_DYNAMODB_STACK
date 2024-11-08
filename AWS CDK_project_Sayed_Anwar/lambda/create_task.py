import json
import boto3
from botocore.exceptions import ClientError
import uuid  # Import to generate unique task IDs

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TasksTable')

    try:
        body = json.loads(event['body'])
        title = body.get('title')
        description = body.get('description')
        status = body.get('status')

        if not title or not description or not status:
            raise ValueError("Missing required fields: title, description, status")
        
        # Generate a unique task ID
        task_id = str(uuid.uuid4())

        # Create the item to be inserted into the table
        task = {
            'taskId': task_id,
            'title': title,
            'description': description,
            'status': status
        }
        
        # Put the item into the DynamoDB table
        table.put_item(Item=task)

        # Return the response with taskId, title, description, and status
        response = {
            'taskId': task_id,
            'title': title,
            'description': description,
            'status': status
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except (ClientError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    
    

