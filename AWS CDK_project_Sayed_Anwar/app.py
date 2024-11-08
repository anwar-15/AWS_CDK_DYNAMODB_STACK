import aws_cdk as cdk
from aws_cdk_dynamodb_stack import AwsCdkDynamodbStack

app = cdk.App() #app object
AwsCdkDynamodbStack(app, "AwsCdkDynamodbStack") 
app.synth() #sythesizing it into cloudfront template