import os
import json
import subprocess
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute_command(command, cwd=None, env=None, capture_output=True, check=True):
    """
    Executes a shell command.

    Args:
        command (list): The command to execute as a list of strings.
        cwd (str, optional): The working directory to execute the command in. Defaults to None.
        env (dict, optional): Additional environment variables. Defaults to None.
        capture_output (bool, optional): Whether to capture the command's output. Defaults to True.
        check (bool, optional): Whether to raise an exception if the command fails. Defaults to True.

    Returns:
        subprocess.CompletedProcess: The result of the command execution.

    Raises:
        subprocess.CalledProcessError: If the command fails and check is True.
    """
    logger.debug(f"Executing command: {command} in {cwd if cwd else os.getcwd()} with env {env}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            text=True,
            check=check
        )
        logger.debug(f"Command exited with code {result.returncode}")
        if capture_output:
            logger.debug(f"Stdout: {result.stdout}")
            logger.debug(f"Stderr: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")

        raise

def read_json_file(file_path):
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file: {file_path} - {e}")
        raise

def write_json_file(file_path, data, indent=4):
    """
    Writes data to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (dict): The data to write.
        indent (int, optional): The indentation level. Defaults to 4.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)
    except Exception as e:
        logger.error(f"Error writing to file: {file_path} - {e}")
        raise

def set_up_logging(log_level=logging.INFO):
    """
    Sets up logging configuration.

    Args:
        log_level (int, optional): The logging level. Defaults to logging.INFO.
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_variable_name(name):
    """
    Validates if a variable name is valid.
    A valid variable name must start with a letter or underscore, and can contain letters, numbers, or underscores.

    Args:
        name (str): The variable name to validate.

    Returns:
        bool: True if the variable name is valid, False otherwise.
    """
    import re
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    return bool(re.match(pattern, name))