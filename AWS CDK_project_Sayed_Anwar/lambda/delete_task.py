import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MyDynamoDBTable')
    
    # Parse the taskId from the request body
    try:
        body = json.loads(event['body'])
        task_id = body.get('taskId')

        if not task_id:
            raise ValueError("Missing required field: taskId")
        
        # Delete the item from the DynamoDB table
        response = table.delete_item(
            Key={'taskId': task_id}
        )

        deleted_task = response.get(task_id)
        if not deleted_task:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Task not found'})
            }

        return {
            'statusCode': 204,
            'body': json.dumps({"No Content!"})
        }

    except (ClientError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
