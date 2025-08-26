import pandas as pd

class ExcelExporter:
    """Export leads ke Excel (.xlsx)"""

    def export(self, leads, filepath):
        data = [lead.to_dict() for lead in leads]
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False, engine="openpyxl")
        print(f"[EXPORT] Data diekspor ke {filepath}")
