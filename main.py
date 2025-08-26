from scraper.api_scraper import APIScraper
from processors.filter import LeadFilter
from processors.tagger import LeadTagger
from processors.scorer import LeadScorer
from exporters.csv_exporter import CSVExporter

def main():
    # fetch
    scraper = APIScraper()
    leads = scraper.fetch()
    print(f"📥 {len(leads)} leads fetched.")

    # deduplicate
    lead_filter = LeadFilter()
    leads = lead_filter.deduplicate(leads)
    print(f"🔹 {len(leads)} unique leads after deduplication.")

    # scoring
    scorer = LeadScorer(target_cities=["Jakarta"], target_industries=["Tech"])
    leads = scorer.apply(leads)

    # tagging
    tagger = LeadTagger()
    leads = tagger.tag_industry(leads)
    leads = tagger.add_tag_high_potential(leads)

    # export
    CSVExporter().export(leads)

if __name__ == "__main__":
    main()
