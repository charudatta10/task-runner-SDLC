from invoke import task
import os
import shutil
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import logging
from ..config import Config
from ..utils.logger import setup_logging


def run_command_safe(ctx, command, output_file=None, description=""):
    """
    Safely run a command with error handling and logging

    Args:
        ctx: Invoke context
        command (str): Command to run
        output_file (str): Optional output file for command result
        description (str): Description for logging

    Returns:
        tuple: (success: bool, result: str)
    """
    try:
        if output_file:
            full_command = f"{command} > {output_file}"
        else:
            full_command = command

        result = ctx.run(full_command, hide=True, warn=True)

        if result.ok:
            logger.info(f"✅ {description}: SUCCESS")
            print(f"✅ {description}")
            return True, result.stdout if hasattr(result, "stdout") else ""
        else:
            logger.warning(f"⚠️ {description}: FAILED - {result.stderr}")
            print(f"⚠️ {description}: FAILED")
            return False, result.stderr if hasattr(result, "stderr") else ""

    except Exception as e:
        logger.error(f"❌ {description}: ERROR - {str(e)}")
        print(f"❌ {description}: ERROR - {str(e)}")
        return False, str(e)


def check_tool_availability(tool_name):
    """Check if a tool is available in the system PATH"""
    try:
        subprocess.run(
            [tool_name, "--version"], capture_output=True, check=True, timeout=10
        )
        return True
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return False


def copy_file_safe(source, destination, description=""):
    """Safely copy a file with error handling"""
    try:
        source_path = Path(source)
        dest_path = Path(destination)

        if source_path.exists():
            if source_path.is_file():
                shutil.copy2(source_path, dest_path)
                logger.info(f"✅ Copied {description}: {source} -> {destination}")
                print(f"✅ Copied {description}")
                return True
            else:
                logger.warning(f"⚠️ Source is not a file: {source}")
                print(f"⚠️ Source is not a file: {source}")
                return False
        else:
            logger.warning(f"⚠️ Source file not found: {source}")
            print(f"⚠️ Source file not found: {source}")
            return False

    except Exception as e:
        logger.error(f"❌ Failed to copy {description}: {str(e)}")
        print(f"❌ Failed to copy {description}: {str(e)}")
        return False


@task
def generate_system_reports(ctx, destination_folder=None, include_optional=False):
    """
    Generate comprehensive system reports and copy configuration files.

    Args:
        destination_folder (str): Destination folder for reports (default: Config.BACKUP_DIR)
        include_optional (bool): Include optional/experimental package managers
    """

    # Setup destination folder
    if destination_folder is None:
        destination_folder = Config.BACKUP_DIR

    dest_path = Path(destination_folder)
    dest_path.mkdir(parents=True, exist_ok=True)

    # Setup logging
    global logger
    logger = setup_logging(dest_path / "logs")

    # Save current directory
    original_dir = Path.cwd()

    try:
        # Change to destination directory
        os.chdir(dest_path)

        logger.info(f"Starting system reports generation in: {dest_path}")
        print(f"🚀 Generating system reports in: {dest_path}")
        print(f"💻 System: {platform.system()} {platform.release()}")

        # Create system info report
        system_info = {
            "timestamp": datetime.now().isoformat(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
        }

        with open("system_info.json", "w") as f:
            json.dump(system_info, f, indent=2)
        logger.info("✅ System info saved")
        print("✅ System info saved")

        # Package manager reports
        reports_config = [
            # Core package managers
            {
                "tool": "scoop",
                "command": "scoop export",
                "output": "scoop.json",
                "description": "Scoop packages",
                "required": False,
            },
            {
                "tool": "winget",
                "command": "winget export -o winget.json",
                "output": None,
                "description": "Windows Package Manager",
                "required": False,
            },
            {
                "tool": "pip",
                "command": "pip list --format=json",
                "output": "pip.json",
                "description": "Python pip packages",
                "required": False,
            },
            {
                "tool": "pipx",
                "command": "pipx list --json",
                "output": "pipx.json",
                "description": "Python pipx packages",
                "required": False,
            },
            {
                "tool": "conda",
                "command": "conda list --json",
                "output": "conda_packages.json",
                "description": "Conda packages (current env)",
                "required": False,
            },
            {
                "tool": "npm",
                "command": "npm list -g --json",
                "output": "npm_global.json",
                "description": "NPM global packages",
                "required": False,
            },
        ]

        # Optional package managers (if include_optional is True)
        if include_optional:
            optional_reports = [
                {
                    "tool": "choco",
                    "command": "choco list",
                    "output": "choco.txt",
                    "description": "Chocolatey packages",
                    "required": False,
                },
                {
                    "tool": "brew",
                    "command": "brew list --json",
                    "output": "brew.json",
                    "description": "Homebrew packages",
                    "required": False,
                },
                {
                    "tool": "cargo",
                    "command": "cargo install --list",
                    "output": "cargo.txt",
                    "description": "Rust Cargo packages",
                    "required": False,
                },
                {
                    "tool": "gem",
                    "command": "gem list --local",
                    "output": "gems.txt",
                    "description": "Ruby gems",
                    "required": False,
                },
            ]
            reports_config.extend(optional_reports)

        # Generate reports
        successful_reports = 0
        failed_reports = 0

        for report in reports_config:
            tool = report["tool"]
            command = report["command"]
            output = report["output"]
            description = report["description"]

            # Check if tool is available
            if not check_tool_availability(tool):
                logger.info(f"⏭️ Skipping {description}: {tool} not found")
                print(f"⏭️ Skipping {description}: {tool} not available")
                continue

            # Run the command
            success, result = run_command_safe(ctx, command, output, description)

            if success:
                successful_reports += 1
            else:
                failed_reports += 1

        # Special conda environments export
        if check_tool_availability("conda"):
            try:
                # Get list of conda environments
                result = ctx.run("conda env list --json", hide=True, warn=True)
                if result.ok:
                    envs_data = json.loads(result.stdout)
                    envs = envs_data.get("envs", [])

                    conda_exports = {}
                    for env_path in envs:
                        env_name = Path(env_path).name
                        if env_name in ["base", "conda"]:
                            continue

                        try:
                            env_result = ctx.run(
                                f"conda env export --name {env_name} --json",
                                hide=True,
                                warn=True,
                            )
                            if env_result.ok:
                                conda_exports[env_name] = json.loads(env_result.stdout)
                                logger.info(
                                    f"✅ Exported conda environment: {env_name}"
                                )
                                print(f"✅ Exported conda environment: {env_name}")
                        except Exception as e:
                            logger.warning(
                                f"⚠️ Failed to export conda env {env_name}: {e}"
                            )

                    if conda_exports:
                        with open("conda_environments.json", "w") as f:
                            json.dump(conda_exports, f, indent=2)
                        successful_reports += 1

            except Exception as e:
                logger.error(f"❌ Failed to export conda environments: {e}")
                failed_reports += 1

        # Copy configuration files
        config_files = [
            {
                "source": getattr(Config, "PROFILE_PATH", None),
                "destination": dest_path,
                "description": "PowerShell Profile",
            },
            {
                "source": Path.home() / ".gitconfig",
                "destination": dest_path,
                "description": "Git configuration",
            },
            {
                "source": Path.home() / ".vimrc",
                "destination": dest_path,
                "description": "Vim configuration",
            },
            {
                "source": Path.home() / ".bashrc",
                "destination": dest_path,
                "description": "Bash configuration",
            },
        ]

        copied_files = 0
        for config in config_files:
            if config["source"]:
                if copy_file_safe(
                    config["source"], config["destination"], config["description"]
                ):
                    copied_files += 1

        # Generate summary report
        summary = {
            "generation_time": datetime.now().isoformat(),
            "destination": str(dest_path),
            "system_info": system_info,
            "reports_generated": successful_reports,
            "reports_failed": failed_reports,
            "config_files_copied": copied_files,
            "total_files": len(list(dest_path.glob("*"))),
        }

        with open("generation_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Final summary
        logger.info(f"System reports generation completed")
        logger.info(f"✅ Reports generated: {successful_reports}")
        logger.info(f"⚠️ Reports failed: {failed_reports}")
        logger.info(f"📄 Config files copied: {copied_files}")

        print(f"\n🎉 System reports generation completed!")
        print(f"📊 Summary:")
        print(f"  ✅ Reports generated: {successful_reports}")
        print(f"  ⚠️ Reports failed: {failed_reports}")
        print(f"  📄 Config files copied: {copied_files}")
        print(f"  📁 Output directory: {dest_path}")

    except Exception as e:
        logger.error(f"❌ Critical error during system reports generation: {str(e)}")
        print(f"❌ Critical error: {str(e)}")

    finally:
        # Return to original directory
        os.chdir(original_dir)


@task
def list_system_tools(ctx):
    """
    List available system package managers and tools.
    """
    tools_to_check = [
        "scoop",
        "winget",
        "pip",
        "pipx",
        "conda",
        "npm",
        "choco",
        "brew",
        "cargo",
        "gem",
        "git",
        "node",
        "python",
    ]

    print("🔍 Checking available system tools:")
    print("=" * 40)

    available_tools = []
    unavailable_tools = []

    for tool in tools_to_check:
        if check_tool_availability(tool):
            available_tools.append(tool)
            print(f"✅ {tool}")
        else:
            unavailable_tools.append(tool)
            print(f"❌ {tool}")

    print(f"\n📊 Summary:")
    print(f"✅ Available: {len(available_tools)} tools")
    print(f"❌ Unavailable: {len(unavailable_tools)} tools")

    return available_tools


@task
def quick_backup(ctx, destination_folder=None):
    """
    Quick backup of essential system configurations.
    Only backs up core package managers and essential config files.
    """
    if destination_folder is None:
        destination_folder = Config.BACKUP_DIR

    print("🏃‍♂️ Running quick system backup...")
    generate_system_reports(ctx, destination_folder, include_optional=False)
