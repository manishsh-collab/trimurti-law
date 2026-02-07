import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from src.knowledge_ingest import KnowledgeIngestor, IngestedDocument, InputFormat

print("TESTING OMNI-TRAIN ROUTING...")
ingestor = KnowledgeIngestor()

# Test Case: Simple text that normally goes to NO specific agent
neutral_text = "The quick brown fox jumps over the lazy dog."
doc = IngestedDocument(
    id="TEST-001",
    source="test",
    format=InputFormat.TEXT,
    doc_type="test",
    raw_text=neutral_text,
    extracted_data={},
    metadata={}
)

# 1. Normal Routing
print("\n[Case 1] Normal Routing:")
agents = ingestor.router.route_document(doc, force_all_agents=False)
print(f"Target Agents: {agents}")
assert len(agents) <= 2, "Should be minimal/fallback agents"

# 2. Omni-Train Routing
print("\n[Case 2] Omni-Train Routing (Force All):")
all_agents = ingestor.router.route_document(doc, force_all_agents=True)
print(f"Target Agents: {len(all_agents)} agents selected.")
print(f"Agents: {all_agents[:5]}...")

assert len(all_agents) > 20, "Should target ALL agents"
print("\nSUCCESS: Omni-Train correctly targets entire agent fleet.")
