import json
from services.payload_service import PayloadService
from services.exploit_service import ExploitService
from services.post_service import PostService
from reporting import ReportGenerator
from utils import setup_logger
from config import LOG_DIR

logger = setup_logger('Main', f"{LOG_DIR}/main.log")


class CVEProcessor:
    def __init__(self, cve_list):
        self.cve_list = cve_list
        self.report = []

    def process_cve(self, cve_data):
        """
        Process a single CVE.
        """
        cve_report = {"cve_id": cve_data["cve_id"], "results": {}}
        try:
            logger.info(f"Processing CVE: {cve_data['cve_id']} on {cve_data['host']}:{cve_data['port']}")

            # Step 1: Generate Payload
            payload_service = PayloadService(cve_data)
            payload_result = payload_service.generate_payload()
            cve_report["results"]["payload"] = payload_result

            # Step 2: Execute Exploitation
            exploit_service = ExploitService(cve_data, payload_result)
            exploit_result = exploit_service.execute_exploit()
            cve_report["results"]["exploit"] = exploit_result

            # Step 3: Perform Post-Exploitation
            if exploit_result["status"] == "success":
                post_service = PostService(cve_data)
                post_result = post_service.perform_post_exploitation()
                cve_report["results"]["post_exploitation"] = post_result
            else:
                logger.warning(f"Skipping post-exploitation for {cve_data['cve_id']}. Reason: {exploit_result['message']}")
        except Exception as e:
            logger.error(f"Error processing CVE {cve_data['cve_id']}: {e}")
            cve_report["error"] = str(e)

        self.report.append(cve_report)

    def process_all(self):
        """
        Process all CVEs and generate a report.
        """
        for cve_data in self.cve_list:
            self.process_cve(cve_data)
        ReportGenerator.save_report(self.report)


def load_cve_data(file_path):
    """
    Load CVE data from a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {file_path}")
    return []


if __name__ == "__main__":
    cve_file = "cve_targets.json"
    cve_data_list = load_cve_data(cve_file)

    if cve_data_list:
        processor = CVEProcessor(cve_data_list)
        processor.process_all()
    else:
        logger.error("No CVE data to process. Exiting.")
