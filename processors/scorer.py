class LeadScorer:
    """Enhanced lead scoring based on target cities, industries, company size, and tags"""

    def __init__(self, target_cities=None, target_industries=None, base_score=10):
        self.target_cities = target_cities or []
        self.target_industries = target_industries or []
        self.base_score = base_score

    def apply(self, leads):
        for lead in leads:
            score = self.base_score

            # city bonus
            if lead.location in self.target_cities:
                score += 30

            # industry bonus
            if getattr(lead, "industry", None) in self.target_industries:
                score += 40

            # company size bonus
            if getattr(lead, "company_size", "Medium") == "Large":
                score += 20
            elif getattr(lead, "company_size", "Medium") == "Medium":
                score += 10
            # Small → +0

            # High Potential tag bonus
            if "High Potential" in getattr(lead, "tags", []):
                score += 10

            # cap maximum 100
            lead.score = min(score, 100)

        return leads
