"""
This script is used to start the local API using the SAM CLI.
"""
import subprocess
import utils

running_process = None


def main():
    """
    Main function that builds the SAM application, validates the SAM template,
    and starts the local API.

    It handles keyboard interrupt gracefully and terminates the running process.
    """
    global running_process
    try:
        utils.clear_screen()

        # Build the SAM application
        utils.run_command(["sam", "build"])

        # Validate the SAM template
        utils.run_command(["sam", "validate"])

        # Start the local API
        running_process = subprocess.Popen(["sam", "local", "start-api"])
        running_process.wait()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nTerminating...")
    finally:
        utils.handle_termination(running_process)


if __name__ == "__main__":
    main()
