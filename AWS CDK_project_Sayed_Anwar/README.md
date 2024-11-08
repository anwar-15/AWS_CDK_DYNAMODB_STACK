Install CDK
**CREATE new project using init command**
    * mkdir aws-cdk-project && cd aws-cdk-project    ## project name
    * cdk init app --language python
    * source .venv/bin/activate                      ##activates app's python venv
    * python -m pip install -r requirements.txt      ##install the core dependencies

**SETUP AWS Eniornment**
    * aws sts get-caller-identity --profile your-profile-name --query "Account" --output text
    * aws configure get region --profile your-profile-name

**CONFIGURE Enviornment for CDK Stack**
    AwsCdkDynamodbStack(app, "AwsCdkDynamodbStack",
  env=cdk.Environment(account='your_aws_account_number', region='us-east-1')    ##specify region
  )

**BOOTSTRAP AWS Enviornment**
    cdk bootstrap

**BUILD YOUR CDK APP**
    * The application aws_cdk_dynamodb_stack

**SYNTHESIZE to generate cloudfront template**
    cdk synth                                    ##app.py should be in root dir

**DEPLOY your Stack**
    cdk deploy
