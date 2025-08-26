import requests
from models.lead import Lead
import random
import geonamescache

gc = geonamescache.GeonamesCache()
CITIES = [city['name'] for city in gc.get_cities().values()]

COMPANIES = [
    "TechNova", "Innova Solutions", "Caprae Finance", "HealthPlus", 
    "EduSmart", "RetailCo", "Global Trade Inc.", "FinTech Global", "DataWorks"
]

POSITIONS = [
    "Software Engineer", "Data Analyst", "Product Manager", 
    "Sales Executive", "Marketing Specialist", "HR Manager", "Consultant"
]

INDUSTRIES = ["Tech", "Finance", "Healthcare", "Education", "Retail", "Consulting", "Other"]
COMPANY_SIZES = ["Small", "Medium", "Large"]

class APIScraper:
    API_URL = "https://randomuser.me/api/"

    def fetch(self, results=50):
        response = requests.get(f"{self.API_URL}?results={results}")
        response.raise_for_status()
        data = response.json()
        leads = []

        for item in data["results"]:
            city = item["location"]["city"]
            if city not in CITIES:
                city = random.choice(CITIES)

            lead = Lead(
                name=f"{item['name']['first']} {item['name']['last']}",
                email=item["email"],
                company=random.choice(COMPANIES),
                position=random.choice(POSITIONS),
                location=city,
                industry=random.choice(INDUSTRIES),
                company_size=random.choice(COMPANY_SIZES)
            )
            leads.append(lead)
        return leads
