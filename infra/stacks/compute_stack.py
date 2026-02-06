from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks
)
from constructs import Construct

class ComputeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- 1. Define Lambdas ---
        def create_func(id_name, handler_path):
            func = _lambda.Function(
                self, id_name,
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler=handler_path,
                code=_lambda.Code.from_asset("app"),
                environment={"TABLE_NAME": table.table_name},
                timeout=Duration.seconds(10)
            )
            table.grant_read_write_data(func)
            return func

        anchor_fn = create_func("AnchorLayer", "layers.anchor.handler.lambda_handler")
        macro_fn = create_func("MacroLayer", "layers.macro.handler.lambda_handler")
        market_fn = create_func("MarketLayer", "layers.market.handler.lambda_handler")
        agent_fn = create_func("AgentLayer", "layers.agents.handler.lambda_handler")
        ledger_fn = create_func("LedgerLayer", "layers.ledger.handler.lambda_handler")

        # --- 2. Define Step Function Tasks ---
        # Each task runs a Lambda and passes the result to the next
        
        task_anchor = tasks.LambdaInvoke(
            self, "Run Anchor Layer",
            lambda_function=anchor_fn,
            output_path="$.Payload" # Pass the function's return value to the next step
        )

        task_macro = tasks.LambdaInvoke(
            self, "Run Macro Layer",
            lambda_function=macro_fn,
            output_path="$.Payload"
        )

        task_market = tasks.LambdaInvoke(
            self, "Run Market Layer",
            lambda_function=market_fn,
            output_path="$.Payload"
        )

        task_agents = tasks.LambdaInvoke(
            self, "Run Agent Layer",
            lambda_function=agent_fn,
            output_path="$.Payload"
        )

        task_ledger = tasks.LambdaInvoke(
            self, "Run Ledger Layer",
            lambda_function=ledger_fn,
            output_path="$.Payload"
        )

        # --- 3. Define the Workflow (The Chain) ---
        # Anchor -> Macro -> Market -> Agents -> Ledger
        chain = task_anchor.next(task_macro).next(task_market).next(task_agents).next(task_ledger)

        # --- 4. Create the State Machine ---
        sfn.StateMachine(
            self, "EconVerseSimulationLoop",
            definition=chain,
            timeout=Duration.minutes(5),
            state_machine_name="EconVerse_Tick_Orchestrator"
        )
