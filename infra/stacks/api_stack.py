from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as integrations
)
from constructs import Construct

class ApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. The Reader Lambda
        reader_fn = _lambda.Function(
            self, "ReaderLayer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="layers.reader.handler.lambda_handler",
            code=_lambda.Code.from_asset("app"),
            environment={"TABLE_NAME": table.table_name},
            timeout=Duration.seconds(5)
        )
        
        # Grant Read-Only access (Security Best Practice)
        table.grant_read_data(reader_fn)

        # 2. The API Gateway (HTTP API - Cheaper/Faster than REST)
        api = apigw.HttpApi(
            self, "EconVerseAPI",
            cors_preflight={
                "allow_origins": ["*"],
                "allow_methods": [apigw.CorsHttpMethod.GET],
            }
        )

        # 3. The Integration (Connect API -> Lambda)
        integration = integrations.HttpLambdaIntegration(
            "ReaderIntegration",
            reader_fn
        )

        # 4. The Route
        api.add_routes(
            path="/state",
            methods=[apigw.HttpMethod.GET],
            integration=integration
        )

        # 5. Output the URL so you know where to click
        CfnOutput(self, "ApiEndpoint", value=api.url)
