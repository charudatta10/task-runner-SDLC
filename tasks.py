# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt
####################################################
# create generalized gitignore
#####################################################
from invoke import task, Collection

import initialize
import deploy
import license
import readme
import manger
import maintain


# Define modules
modules = {
    1: initialize,
    2: deploy,
    3: license,
    4: readme,
    5: manger,
    6: maintain,
}


@task
def exit_task(ctx):
    """Gracefully quit the script."""
    print("Thank you for using this script!")
    print("Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License")


@task
def list_modules(ctx):
    """List all available modules."""
    for index, module in modules.items():
        print(f"{index}: {module.__name__.replace('_', ' ').title()}")


@task(default=True)
def default(ctx):
    """Default task to list modules and pick tasks within a module.
    Args:
        ctx (invoke.Context): The context object for invoking tasks.
    Returns:
        None
    Example:
        $ invoke task_runner"""
    print("Available modules:")
    print("0: Exit Task Runner")
    list_modules(ctx)
    module_choice = int(input("Select a module by number: "))

    if module_choice == 0:
        exit_task(ctx)
        return

    selected_module = modules.get(module_choice)
    if not selected_module:
        print("Invalid choice!")
        return

    selected_ns = selected_module.ns
    tasks = sorted(selected_ns.tasks.keys())
    print(f"Available tasks in {selected_ns.name}:")
    for i, task_name in enumerate(tasks, 1):
        print(f"{i}: {task_name}")

    task_choice = int(input("Enter the number of your choice: "))
    selected_task = tasks[task_choice - 1]
    print(f"Running task: {selected_ns.name}.{selected_task}")
    selected_task_cmd = selected_task.replace("_", "-")
    selected_module_cmd = selected_ns.name.replace("_", "-")
    print(f"Help for {selected_module_cmd}.{selected_task_cmd}:")
    command = f"invoke {selected_module_cmd}.{selected_task_cmd}"
    ctx.run(f"{command} --help")

    args = input(
        "Enter arguments (format: arg1=value1,arg2=value2, or leave blank for none): "
    )
    kwargs = (
        " ".join(
            [
                f"--{k.strip()}={v.strip()}"
                for k, v in (arg.split("=") for arg in args.split(","))
            ]
        )
        if args.strip()
        else ""
    )

    command = f"{command} {kwargs}".strip()
    print(f"Running command: {command}")
    ctx.run(command)


# Create a namespace and add tasks from the imported modules
ns = Collection(*modules.values())
ns.add_task(default)
ns.name = "task"

if __name__ == "__main__":
    default(context())
