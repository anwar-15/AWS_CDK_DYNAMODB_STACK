import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TasksTable')
    
    # Parse the taskId from query parameters
    try:
        body = json.loads(event['body'])
        #parsing update expressions
        task_id = body.get('taskId')
        title = body.get('title')
        description = body.get('description')
        status = body.get('status')

        if not task_id or not title or not description or not status:
            raise ValueError("Missing required fields: taskId, title, description, status")
        
        # Update the item in the DynamoDB table
        update_expression = "SET #title = :title, #description = :description, #status = :status"
        expression_attribute_names = {
            '#title': 'title',
            '#description': 'description',
            '#status': 'status'
        }
        expression_attribute_values = {
            ':title': title,
            ':description': description,
            ':status': status
        }

        response = table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        updated_item = response.get('Attributes')

        return {
            'statusCode': 200,
            'body': json.dumps(updated_item)
        }

    except (ClientError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
