import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
from src.knowledge_ingest import KnowledgeIngestor, InputFormat
import time

print("TESTING DEEP HARVEST MODE...")
ingestor = KnowledgeIngestor()
url = "https://www.supremecourt.gov/orders/ordersbycircuit/25"

print(f"Target: {url}")
print("Starting Generator with harvest_mode=True...")

count = 0
for event in ingestor.ingest_site_generator(url, harvest_mode=True):
    print(f"[{event['status'].upper()}] {event.get('message', '')}")
    
    if event['status'] == 'training_complete':
        print(f" >>> TRAINED ON: {event['doc_name']}")
        count += 1
        
    if count >= 3:
        print("Test limit reached (3 docs). Stopping.")
        break
        
print("Test Complete.")
