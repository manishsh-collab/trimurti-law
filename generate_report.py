import json
import os
import sys
import codecs
from collections import defaultdict

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

history_file = "training_history.json"
data_dir = "data"
models_dir = "models"
embeddings_dir = "embeddings"

print("Generating Training Report...")
print("-" * 30)

total_docs = 0
agent_stats = defaultdict(int)

# 1. Parse History JSON
try:
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
            for session in history:
                for entry in session.get("report", []):
                    agent = entry.get("Agent", "Unknown")
                    docs = entry.get("Docs", 0)
                    if isinstance(docs, int):
                        agent_stats[agent] += docs
                        total_docs += docs
    else:
        print(f"[WARN] {history_file} not found.")
except Exception as e:
    print(f"[ERROR] Reading history: {e}")

# 2. Check Physical Files (Deep Harvest might bypass JSON log)
physical_files = 0
physical_size_mb = 0

if os.path.exists(data_dir):
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            physical_files += 1
            physical_size_mb += os.path.getsize(os.path.join(root, f)) / (1024*1024)

# 3. Model Size
model_size_mb = 0
if os.path.exists(models_dir):
    for root, dirs, files in os.walk(models_dir):
        for f in files:
            model_size_mb += os.path.getsize(os.path.join(root, f)) / (1024*1024)

# 4. Print Report
print(f"Total Documents Trained (Logged): {total_docs}")
print(f"Physical Data Stored: {physical_files} files ({physical_size_mb:.2f} MB)")
print(f"Model Artifact Size: {model_size_mb:.2f} MB")
print("-" * 30)

print("Agent Knowledge Distribution:")
sorted_agents = sorted(agent_stats.items(), key=lambda x: x[1], reverse=True)
for agent, count in sorted_agents:
    if count > 0:
        bar = "█" * (count // 50)  # Ascii bar
        print(f"{agent.ljust(20)}: {count:4d} docs {bar}")
