import os
from synology_api.core_active_backup import ActiveBackupBusiness
from dotenv import load
from datetime import datetime


def main():

    # 현재 로컬 시간 가져오기
    now = datetime.now()

    # 원하는 형식으로 포맷팅
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        load()
        # Get credentials from environment variables
        host = os.getenv('SYNOLOGY_HOST')
        port = os.getenv('SYNOLOGY_PORT')
        username = os.getenv('SYNOLOGY_USERNAME')
        password = os.getenv('SYNOLOGY_PASSWORD')
        target_task = os.getenv('TARGET_TASK_NAME')

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

        # 작업 목록 조회
        tasks = abb.list_tasks()
        print(f"[{formatted_time}] 작업 목록 조회 중...")

        # target_task 작업 찾기
        task_ids = []
        if tasks and tasks.get('success') and 'data' in tasks and 'tasks' in tasks['data']:
            for task in tasks['data']['tasks']:
                if task.get('task_name') == target_task:
                    task_ids.append(task.get('task_id'))
                    print(
                        f"[{formatted_time}] '{target_task}' 작업을 찾았습니다. Task ID: {task.get('task_id')}")

        if not task_ids:
            print(f"[{formatted_time}] '{target_task}' 작업을 찾을 수 없습니다.")
            exit(1)

        # 백업 작업 실행
        abb.backup_task_run(task_ids=task_ids)
        print(f"[{formatted_time}] 백업 작업 요청을 성공적으로 전송하였습니다. Task IDs: {task_ids}")
    except Exception as e:
        print(f"[{formatted_time}] 오류가 발생했습니다: {e}")
        exit(1)


if __name__ == "__main__":
    main()
