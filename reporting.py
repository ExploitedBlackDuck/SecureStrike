import json
from config import REPORT_FILE


class ReportGenerator:
    @staticmethod
    def save_report(data):
        """
        Saves the final report in JSON format.
        """
        try:
            with open(REPORT_FILE, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Report saved to {REPORT_FILE}")
        except Exception as e:
            print(f"Failed to save report: {e}")
