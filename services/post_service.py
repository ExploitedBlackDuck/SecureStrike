from utils import setup_logger, execute_command
from config import LOG_DIR

logger = setup_logger('PostService', f"{LOG_DIR}/post_service.log")


class PostService:
    def __init__(self, cve_data):
        self.cve_data = cve_data

    def perform_post_exploitation(self):
        """
        Performs post-exploitation tasks.
        """
        command = f"post_exploit_tool --target {self.cve_data['host']} --port {self.cve_data['port']}"
        result = execute_command(command, logger)

        if result["status"] == "success":
            return {"status": "success", "message": "Post-exploitation completed successfully.", "command": command}
        return {"status": "error", "message": result["error"]}
