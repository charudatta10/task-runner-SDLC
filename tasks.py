from invoke import Program
from src import ns

# Configure CLI
program = Program(
    namespace=ns,
    version="1.0.0",
    name="Task Runner"
)