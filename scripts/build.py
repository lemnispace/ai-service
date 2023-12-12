"""
This script builds and validates a SAM (Serverless Application Model) application.

Usage:
  python build.py [--profile PROFILE_NAME]

Arguments:
  --profile (str): The AWS profile to use for building and validating. Default is "lemnispace-sam".

Example:
  python build.py --profile my-aws-profile
"""

import subprocess
import utils
import argparse

running_process = None


def main(profile):
    """
    Main function to build and validate the SAM application.

    Args:
      profile (str): The AWS profile to use for building and validating.

    Returns:
      None
    """
    global running_process
    try:
        utils.clear_screen()

        # Build the SAM application
        utils.run_command(["sam", "build", "--profile", profile])

        # Validate the SAM template
        running_process = subprocess.Popen(["sam", "validate"])
        running_process.wait()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nTerminating...")
    finally:
        utils.handle_termination(running_process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="lemnispace-sam", help="AWS profile name")
    args = parser.parse_args()
    main(args.profile)
