"""Quick test for Phase 9 systems."""
from src.model_trainer import get_model_trainer, ModelType, IndependentLegalAI
from src.local_llm import get_local_llm, LLMBackend
from src.embeddings import get_legal_embeddings

print("Phase 9 imports successful!")

# Test trainer
trainer = get_model_trainer()
print(f"Trainer: {trainer.name}")

# Test LLM
llm = get_local_llm()
print(f"LLM backends: {[b.value for b in llm.available_backends]}")

# Test embeddings
emb = get_legal_embeddings()
print(f"Embeddings: {emb.name}")

# Test training data generation
trainer.generate_training_data([
    {"text": "The defendant breached the contract by failing to deliver goods.", "source": "test"},
    {"text": "The plaintiff claims negligence led to personal injury damages.", "source": "test"},
])
status = trainer.get_training_status()
print(f"Datasets: {status['datasets']}")

# Test embeddings search
emb.add_document("Smith v. Jones - breach of contract case involving damages")
emb.add_document("Doe v. Corp - negligence and personal injury lawsuit")
results = emb.search("contract breach", top_k=1)
print(f"Search works: {len(results)} result with score {results[0].score:.2f}")

print("\nALL PHASE 9 SYSTEMS OPERATIONAL!")
