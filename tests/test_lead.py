import unittest
from models.lead import Lead

class TestLead(unittest.TestCase):
    def test_add_tag(self):
        lead = Lead("John Doe", "john@example.com", "Company")
        lead.add_tag("Tech")
        self.assertIn("Tech", lead.tags)

    def test_to_dict(self):
        lead = Lead("Jane Doe", "jane@example.com", "Company", "Engineer", "Jakarta")
        d = lead.to_dict()
        self.assertEqual(d["name"], "Jane Doe")
        self.assertEqual(d["location"], "Jakarta")

if __name__ == "__main__":
    unittest.main()
