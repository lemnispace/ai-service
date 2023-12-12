"""
Run the test script using pytest.
"""
import subprocess
import utils

running_process = None


def main():
    """
    Run the test script using pytest.

    This function clears the screen, starts a subprocess to run pytest,
    and waits for the subprocess to finish. It handles keyboard interrupt
    gracefully and terminates the subprocess before exiting.
    """
    global running_process
    try:
        utils.clear_screen()
        running_process = subprocess.Popen(["pytest"])
        running_process.wait()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nTerminating...")
    finally:
        utils.handle_termination(running_process)


if __name__ == "__main__":
    main()
