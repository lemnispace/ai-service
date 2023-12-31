"""
This script is used to build the Python code using SAM CLI as a build tool only.
"""

import utils

running_process = None


def main():
    """
    Main function to build the python code using SAM CLI as a build tool only.

    Returns:
      None
    """
    global running_process
    try:
        # Build the SAM application
        utils.run_command(["sam", "build"])
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nTerminating...")
    finally:
        utils.handle_termination(running_process)


if __name__ == "__main__":
    main()
