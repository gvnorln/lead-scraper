class LeadFilter:
    """Filter leads by criteria and deduplicate"""

    def filter_by_location(self, leads, location):
        if location == "All":
            return leads
        return [lead for lead in leads if lead.location == location]

    def filter_by_industry(self, leads, industry):
        if industry == "All":
            return leads
        return [lead for lead in leads if lead.industry == industry]

    def deduplicate(self, leads):
        seen = set()
        unique = []
        for lead in leads:
            if lead.email not in seen:
                seen.add(lead.email)
                unique.append(lead)
        return unique
