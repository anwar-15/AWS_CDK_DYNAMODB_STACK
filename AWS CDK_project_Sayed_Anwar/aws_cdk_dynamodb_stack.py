## Name: Sayed Anwar
## Date: 9/11/24
## email : anwar15sayed@gmail.com
## github repo : github.com/anwar-15

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

class AwsCdkDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a DynamoDB table with taskId as the partition key and capacity as on-demand
        table = dynamodb.Table(self, "MyDynamoDBTable",
            partition_key=dynamodb.Attribute(
                name="taskId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Create Lambda functions for CRUD operations
        create_task_function = self.create_lambda_function("CreateTaskFunction", "create_task.handler")
        read_task_function = self.create_lambda_function("ReadTaskFunction", "read_task.handler")
        update_task_function = self.create_lambda_function("UpdateTaskFunction", "update_task.handler")
        delete_task_function = self.create_lambda_function("DeleteTaskFunction", "delete_task.handler")

        # Grant the Lambda functions read and write permissions to the DynamoDB table
        table.grant_read_write_data(create_task_function)
        table.grant_read_write_data(read_task_function)
        table.grant_read_write_data(update_task_function)
        table.grant_read_write_data(delete_task_function)

        # Create an API Gateway
        api = apigateway.RestApi(self, "ApiGatewayTask",
            rest_api_name="DynamoDB-CRUD-API",
            description="CRUD API for DynamoDB."
        )

        # Integrate the Lambda functions with API Gateway
        items = api.root.add_resource("items")
        items.add_method("POST", apigateway.LambdaIntegration(create_task_function))   # Create
        items.add_method("GET", apigateway.LambdaIntegration(read_task_function))    # Read
        items.add_method("PUT", apigateway.LambdaIntegration(update_task_function))  # Update
        items.add_method("DELETE", apigateway.LambdaIntegration(delete_task_function)) # Delete

    def create_lambda_function(self, id: str, handler: str) -> _lambda.Function:
        return _lambda.Function(self, id,
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler=handler,
            code=_lambda.Code.from_asset("lambda")
        )
