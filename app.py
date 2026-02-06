import aws_cdk as cdk
from infra.stacks.database_stack import DatabaseStack
from infra.stacks.compute_stack import ComputeStack
from infra.stacks.api_stack import ApiStack

app = cdk.App()

# 1. Database
db_stack = DatabaseStack(app, "EconVerse-DatabaseStack")

# 2. Compute (The Simulation Engine)
compute_stack = ComputeStack(
    app,
    "EconVerse-ComputeStack",
    table=db_stack.table
)

# 3. API (The Observer)
api_stack = ApiStack(
    app,
    "EconVerse-ApiStack",
    table=db_stack.table
)

app.synth()
