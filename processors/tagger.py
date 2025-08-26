class LeadTagger:
    """Tagging lead dengan industry & high potential"""

    def tag_industry(self, leads):
        industry_map = {
            "Tech": ["software", "developer", "engineer"],
            "Finance": ["finance", "bank", "investment"],
            "Retail": ["retail", "store", "shop"],
            "Healthcare": ["health", "medical", "clinic"]
        }
        for lead in leads:
            if not lead.industry or lead.industry == "General":
                # assign industry based on position/company keyword
                lead.industry = "General"
                for key, keywords in industry_map.items():
                    if any(k.lower() in (lead.position or "").lower() for k in keywords):
                        lead.industry = key
                        break
        return leads

    def add_tag_high_potential(self, leads):
        for lead in leads:
            if lead.score >= 50:
                lead.add_tag("High Potential")
        return leads

    def tag_defaults(self, leads):
        """Assign default values if missing"""
        for lead in leads:
            if not lead.industry:
                lead.industry = "General"
            if not lead.company_size:
                lead.company_size = "Medium"
        return leads
