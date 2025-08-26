import random

class LeadEnricher:
    """Class untuk enrichment lead: company size, industry, missing info"""

    def __init__(self, default_company_sizes=None):
        self.default_company_sizes = default_company_sizes or ["Small", "Medium", "Large"]

    def enrich_leads(self, leads):
        for lead in leads:
            self._enrich_company_size(lead)
            self._enrich_industry(lead)
            self._flag_missing_info(lead)
        return leads

    def _enrich_company_size(self, lead):
        if not getattr(lead, "company_size", None) or lead.company_size == "Unknown":
            lead.company_size = random.choice(self.default_company_sizes)

    def _enrich_industry(self, lead):
        if not getattr(lead, "industry", None) or lead.industry in [None, "General", "Unknown"]:
            company_name = getattr(lead, "company", "").lower()
            if "tech" in company_name:
                lead.industry = "Tech"
            elif "edu" in company_name:
                lead.industry = "Education"
            elif "health" in company_name:
                lead.industry = "Healthcare"
            else:
                lead.industry = "General"

    def _flag_missing_info(self, lead):
        missing = any([
            getattr(lead, "email", "Unknown") == "Unknown",
            getattr(lead, "company", "Unknown") == "Unknown",
            getattr(lead, "position", "Unknown") == "Unknown"
        ])
        lead.missing_info = "Yes" if missing else "No"
