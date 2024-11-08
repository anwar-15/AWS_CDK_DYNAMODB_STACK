import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TasksTable')
    
    # Parse the taskId from query parameters
    try:
        task_id = event['queryStringParameters']['taskId']

        # Fetch the item from the DynamoDB table
        response = table.get_item(Key={'taskId': task_id})
        
        task = response.get(task_id)
        if not task:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Task not found'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except (ClientError, KeyError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
