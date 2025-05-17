import os
from synology_api.core_active_backup import ActiveBackupBusiness
from dotenv import load


def run_backup(task_ids):
    """
    Run a backup task on Synology Active Backup for Business

    Args:
        task_ids (list): List of task IDs to run
    """
    # Load credentials from .env file
    load()

    # Get credentials from environment variables
    host = os.getenv('SYNOLOGY_HOST')
    port = os.getenv('SYNOLOGY_PORT')
    username = os.getenv('SYNOLOGY_USERNAME')
    password = os.getenv('SYNOLOGY_PASSWORD')

    # Initialize connection to Synology
    abb = ActiveBackupBusiness(
        host,
        port,
        username,
        password,
        secure=True,
        cert_verify=False,
        dsm_version=7,
        debug=False,
        otp_code=None
    )

    # Run the backup task
    abb.backup_task_run(task_ids=task_ids)


def main():
    # Example task ID - you can modify this or accept input parameters
    task_ids = [45]
    try:
        run_backup(task_ids)
        print("Backup task started successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
