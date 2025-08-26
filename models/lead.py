import geonamescache
import random

gc = geonamescache.GeonamesCache()
CITIES = [city['name'] for city in gc.get_cities().values()]

class Lead:
    def __init__(self, name, email, company, position=None, location=None, industry=None, company_size=None):
        self.name = name
        self.email = email
        self.company = company
        self.position = position or "Unknown"
        # pilih location dari dataset geonames jika tidak ada
        self.location = location if location else random.choice(CITIES)
        self.industry = industry or "General"
        self.company_size = company_size or "Medium"
        self.tags = []
        self.score = 0

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "position": self.position,
            "location": self.location,
            "industry": self.industry,
            "company_size": self.company_size,
            "tags": self.tags,
            "score": self.score
        }

    def __repr__(self):
        return f"<Lead {self.name} - {self.company} ({self.location})>"
