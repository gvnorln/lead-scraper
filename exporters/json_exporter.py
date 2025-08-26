import json
import os

class JSONExporter:
    def export(self, leads, filename="output/leads.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data = [lead.to_dict() for lead in leads]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data exported to {filename}")
