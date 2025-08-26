import pandas as pd
import os

class CSVExporter:
    def export(self, leads, filename="output/leads.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame([lead.to_dict() for lead in leads])
        df.to_csv(filename, index=False)
        print(f"✅ Data exported to {filename}")
