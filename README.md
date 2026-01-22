# swe-rd-ai

Comparative analysis of AI-related discourse in Swedish parliamentary documents (1990 onwards).

## Corpus

Documents matching "artificiell intelligens" or "AI" from two sources:

| Type | Description |
|------|-------------|
| `mot` | Motioner (MP proposals) |
| `prop` | Propositioner (government bills) |

## Working hypothesis

Propositioner reflect top-down discourse; motioner reflect bottom-up discourse.

|  | Propositioner (top-down) | Motioner (bottom-up) |
|---|---|---|
| **Source** | Government/executive | Individual MPs |
| **Function** | Policy implementation | Agenda-setting, critique |
| **Orientation** | State capacity, EU alignment | Constituent concerns, dissent |
| **Likely framing** | Governing AI, competitiveness | Protecting from / demanding access to AI |

## Research questions

**Overarching:** How does AI discourse differ between government bills (propositioner) and MP motions (motioner) in Swedish parliamentary documents?

- **RQ1 Framing:** How is AI framed in each document type – as opportunity, risk, or both?
- **RQ2 Thematic focus:** Which policy domains (labour, education, healthcare, defence, innovation) dominate in each document type?
- **RQ3 Stakeholder orientation:** Who is invoked as relevant actors – institutions (EU, industry, state) vs citizens, workers, communities?
- **RQ4 Temporal dynamics:** How has AI discourse emerged and intensified over time in each document type, and which leads?
- **RQ5 Sentiment:** How does evaluative tone differ between document types, and how has it changed over time?
- **RQ6 Agency and directionality:** Who is positioned as acting on AI – the state governing it, or people affected by it?

## Usage

```bash
# Count available documents
python download_corpus.py --dry-run

# Download full corpus
python download_corpus.py

# Test with limited sample
python download_corpus.py --limit 10
```

## Structure

```
data/
├── motioner/
└── propositioner/
```

Each document includes a metadata header (search term, document ID, title, type, date, parliamentary year).
