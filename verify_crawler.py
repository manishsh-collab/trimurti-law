from src.knowledge_ingest import SiteCrawler
import time

print("TESTING CRAWLER ON SUPREMECOURT.GOV...")
crawler = SiteCrawler("https://www.supremecourt.gov/orders/ordersbycircuit/25")

for event in crawler.crawl_generator():
    print(f"[{event['status'].upper()}] {event.get('message', '')}")
    if event['status'] == 'completed':
        print(f"\nDONE! Found {event['found']} resources.")
        for r in event.get('resources', []):
            print(f" - {r['type'].upper()}: {r['url']}")
