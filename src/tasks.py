from invoke import Collection
from invoke.tasks import task
import inspect


# Example function with no arguments
def create_license_file():
    print("Creating license file...")


# Create a function that creates a properly configured task wrapper
def make_wrapper(func, help_text):
    """Create a wrapper function for a given task."""
    print(f"Creating wrapper for function: {func.__name__}")  # Debug print

    def wrapped_task(ctx, *args, **kwargs):
        print(
            f"Wrapper called for {func.__name__} with ctx: {ctx}, args: {args}, kwargs: {kwargs}"
        )  # Debug print
        sig = inspect.signature(func)
        params = list(sig.parameters.values())

        # If the function has no parameters, call it without any arguments
        if not params:
            print(f"{func.__name__} has no parameters, calling without arguments")
            return func()

        # Check if the function expects a ctx parameter
        if params and params[0].name == "ctx":
            print(
                f"{func.__name__} expects ctx parameter, calling with ctx, args, kwargs"
            )
            return func(ctx, *args, **kwargs)
        else:
            print(
                f"{func.__name__} does not expect ctx parameter, calling with args, kwargs"
            )
            return func(*args, **kwargs)

    # Set the docstring for help
    wrapped_task.__doc__ = help_text
    return wrapped_task


# Create namespace collection
ns = Collection()

# List of functions to convert into tasks
FUNCTIONS_TO_TASKS = [
    (create_license_file, "create-license", "Create a license file."),
]

# Create task wrappers and add them to the collection
for func, task_name, task_help in FUNCTIONS_TO_TASKS:
    # Create the wrapper function
    wrapped_task = make_wrapper(func, task_help)
    # Decorate it with @task
    task_obj = task(name=task_name)(wrapped_task)
    # Add it to the collection
    ns.add_task(task_obj)
    print(f"Task '{task_name}' added to namespace")  # Debug print


# Make the collection available to invoke
namespace = ns
