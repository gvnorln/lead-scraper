import unittest
from scraper.api_scraper import APIScraper

class TestAPIScraper(unittest.TestCase):
    def test_fetch(self):
        scraper = APIScraper()
        leads = scraper.fetch()
        self.assertTrue(len(leads) > 0)
        self.assertTrue(hasattr(leads[0], "name"))
        self.assertTrue(hasattr(leads[0], "email"))

if __name__ == "__main__":
    unittest.main()
