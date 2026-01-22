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

## Findings

### RQ1: Framing

| Metric | Motioner | Propositioner |
|--------|----------|---------------|
| Opportunity framing (per 1k words) | 14.42 | 5.02 |
| Risk framing (per 1k words) | 8.00 | 5.59 |
| Net framing ratio | +6.43 | -0.57 |

**Interpretation:** The top-down/bottom-up distinction holds, but not as initially expected:

- **Propositioner** (government bills) are more cautious/balanced – technocratic language acknowledging both opportunity and risk roughly equally
- **Motioner** (MP proposals) are more advocative – MPs use stronger evaluative language overall, skewing heavily toward opportunity framing

This suggests MPs use AI discourse to push for action and investment (opportunity-focused advocacy), while government documents employ more measured policy language. The pattern is consistent across parliamentary years, not a recent phenomenon.

**Visualisations:**
- [Framing comparison](results/rq1_framing_comparison.png) – bar chart and boxplot comparing document types
- [Temporal trends](results/rq1_temporal.png) – framing evolution 2017–2025

### RQ2: Thematic focus

| Domain | Motioner | Propositioner | Difference |
|--------|----------|---------------|------------|
| Innovation | 12.01 | 6.02 | +5.99 |
| Education | 7.71 | 2.26 | +5.45 |
| Labour | 6.67 | 2.69 | +3.98 |
| Healthcare | 5.05 | 1.81 | +3.24 |
| Public sector | 10.82 | 10.01 | +0.81 |

**Interpretation:** Contrary to the initial hypothesis that propositioner would emphasise competitiveness/innovation:

- **All domains** are more frequent in motioner – no domain is over-represented in propositioner
- **Innovation** shows the largest gap: MPs discuss it 2x more than government bills
- **Education and labour** also strongly over-represented in motioner
- **Public sector** is the only domain with similar frequency across both types

This reinforces the RQ1 finding: motioner use more domain-specific, substantive language overall. Propositioner are more diffuse/technocratic, while MPs concentrate on specific policy areas when discussing AI.

**Visualisations:**
- [Domain comparison](results/rq2_domain_bars.png) – grouped bar chart of all domains
- [Radar profile](results/rq2_radar.png) – spider chart showing domain profiles
- [Difference chart](results/rq2_difference.png) – over/under-representation by type
- [Correlation heatmap](results/rq2_correlation.png) – domain co-occurrence patterns

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
