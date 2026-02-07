# Legal Case AI

Enterprise-grade AI-powered Legal Case Metadata Extraction System.

## Features

- **Hybrid AI Extraction**: Combines regex patterns, spaCy NER, and Gemini LLM
- **Best Accuracy**: Multi-tier extraction with intelligent result merging
- **Confidence Scoring**: Know how reliable each extraction is
- **Professional CLI**: Beautiful terminal output with progress tracking
- **Batch Processing**: Process multiple cases efficiently

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run demo
python cli.py demo

# Extract from a case file
python cli.py extract case.txt

# Extract with JSON output
python cli.py extract case.txt --format json -o result.json

# Batch process
python cli.py batch ./cases/ -o ./results/

# View configuration
python cli.py config
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your Gemini API key (optional but recommended for best accuracy)
3. Adjust settings as needed

```bash
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

## Extraction Modes

| Mode | Description | API Required |
|------|-------------|--------------|
| `hybrid` | Best accuracy - regex + LLM | Yes (recommended) |
| `llm_only` | LLM extraction only | Yes |
| `ml_only` | SpaCy + regex | No |
| `regex_only` | Fast pattern matching | No |

## Output Schema

```json
{
  "case_name": "Apple Inc. v. Qualcomm Inc.",
  "court_name": "U.S. Court of Appeals for the Ninth Circuit",
  "jurisdiction_level": "Federal",
  "plaintiffs": [{"name": "Apple Inc.", "type": "Corporation"}],
  "defendants": [{"name": "Qualcomm Inc.", "type": "Corporation"}],
  "primary_topic": "Intellectual Property",
  "disposition": "Affirmed",
  "evidence_types": ["Documentary Evidence", "Expert Testimony"],
  "confidence": {"overall": 0.85}
}
```

## Project Structure

```
legal-case-extractor/
├── cli.py                 # Command-line interface
├── src/
│   ├── __init__.py        # Package exports
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic data models
│   └── extractor.py       # Hybrid extraction engine
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
└── sample_cases/          # Example case files
```

## License

MIT
