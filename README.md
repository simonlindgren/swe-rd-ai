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
- **RQ3 Stakeholder orientation:** Who are invoked as relevant actors – institutions (EU, industry, state) vs citizens, workers, communities?
- **RQ4 Temporal dynamics:** How has AI discourse emerged and intensified over time, and which document type led the discourse?
- **RQ5 Sentiment:** How does evaluative tone differ between document types, and how has it changed over time?

## Findings

### RQ1: Framing

| Metric | Motioner | Propositioner |
|--------|----------|---------------|
| Opportunity framing (per 1k words) | 14.42 | 5.02 |
| Risk framing (per 1k words) | 8.00 | 5.59 |
| Net framing ratio | +6.43 | -0.57 |

Net framing ratio = opportunity − risk. Positive values indicate opportunity-dominant framing; negative values indicate risk-dominant framing.

**Interpretation:** The top-down/bottom-up distinction holds, but not as initially expected:

- **Propositioner** (government bills) are more cautious/balanced – technocratic language acknowledging both opportunity and risk roughly equally
- **Motioner** (MP proposals) are more advocative – MPs use stronger evaluative language overall, skewing heavily toward opportunity framing

This suggests MPs use AI discourse to push for action and investment (opportunity-focused advocacy), while government documents employ more measured policy language. The pattern is consistent across parliamentary years, not a recent phenomenon.

**Visualisations:**
- [Framing comparison](results/rq1_framing_comparison.png) – bar chart and boxplot comparing document types
- [Temporal trends](results/rq1_temporal.png) – framing evolution 2017–2025

### RQ2: Thematic focus

**Method:** Dictionary-based keyword matching across eight policy domains. Each domain is defined by 14–15 Swedish keywords (e.g. labour: *arbete, arbetslöshet, sysselsättning, anställning, jobb, arbetsmarknad...*; innovation: *innovation, näringsliv, företag, startup, tillväxt, konkurrens...*). We count keyword occurrences in the full document text using case-insensitive substring matching.

| Domain | Motioner | Propositioner | Difference |
|--------|----------|---------------|------------|
| Innovation | 12.01 | 6.02 | +5.99 |
| Education | 7.71 | 2.26 | +5.45 |
| Labour | 6.67 | 2.69 | +3.98 |
| Healthcare | 5.05 | 1.81 | +3.24 |
| Public sector | 10.82 | 10.01 | +0.81 |

Values are keyword mentions per 1,000 words, measuring density rather than raw counts. This normalisation ensures fair comparison despite different document counts (452 motioner vs 700 propositioner).

**Interpretation:** Contrary to the initial hypothesis that propositioner would emphasise competitiveness/innovation:

- **All domains** are more frequent in motioner – no domain is over-represented in propositioner
- **Innovation** shows the largest gap: MPs discuss it 2x more than government bills
- **Education and labour** also strongly over-represented in motioner
- **Public sector** is the only domain with similar frequency across both types

This reinforces the RQ1 finding: motioner use more domain-specific, substantive language overall. Propositioner are more diffuse/technocratic, while MPs concentrate on specific policy areas when discussing AI.

**Visualisations:**
- [Domain comparison](results/rq2_domain_bars.png) – grouped bar chart of all domains
- [Radar profile](results/rq2_radar.png) – spider chart showing domain profiles
- [Correlation heatmap](results/rq2_correlation.png) – domain co-occurrence patterns (correlation coefficients across documents; higher values indicate domains frequently discussed together, e.g. labour–education r=0.25, innovation–environment r=0.24)

### RQ3: Stakeholder orientation

**Method:** Regex-based keyword matching across eight stakeholder categories, grouped into institutional actors (EU/international, state/government, industry/business, experts/academia) and citizen-focused actors (citizens/individuals, workers/employees, communities/groups, vulnerable groups). Each category uses 8–11 Swedish keywords or patterns (e.g. state/government: *regering, staten, statlig, departement, minister, myndighet...*; vulnerable groups: *barn, äldre, funktionsnedsättning, utsatt, minoritet...*). Values are mentions per 1,000 words.

| Category | Motioner | Propositioner | Difference |
|----------|----------|---------------|------------|
| State/government | 17.44 | 11.51 | **+5.93** |
| EU/international | 4.40 | 7.76 | **-3.36** |
| Communities/groups | 5.86 | 3.39 | +2.47 |
| Experts/academia | 4.52 | 1.67 | +2.85 |
| Vulnerable groups | 1.87 | 0.75 | +1.12 |

**Interpretation:** The hypothesis that propositioner invoke more institutional actors is **not supported**:

- **State/government** is mentioned 50% more in motioner than propositioner – MPs invoke government heavily
- **EU/international** is the only actor category higher in propositioner (+3.36)
- All citizen-focused categories (communities, vulnerable groups, workers) are higher in motioner
- Both document types skew institutional overall, but motioner mention MORE actors of all types

This suggests motioner call upon the state to act, while propositioner situate AI within EU/international frameworks. Propositioner use EU references to legitimise policy; motioner invoke government to demand action.

**Visualisations:**
- [Stakeholder categories](results/rq3_stakeholder_categories.png) – comparison across all categories
- [Actor balance](results/rq3_actor_balance.png) – institutional vs citizen-focused
- [Orientation scatter](results/rq3_orientation_scatter.png) – document-level positioning

### RQ4: Temporal dynamics

| Metric | Motioner | Propositioner |
|--------|----------|---------------|
| First appearance | 2011 | 2010 |
| Peak volume year | 2025 (98 docs) | 2021 (50 docs) |
| AI mention density | 4.8 per 1k | 0.07 per 1k |
| 50-doc threshold | 2019 | 2012 |

**Interpretation:** A clear shift in leadership over time:

- **2010–2017**: Propositioner dominated AI discourse; motioner nearly absent
- **2018**: Inflection point – motioner volume begins rapid growth (Swedish AI strategy released)
- **2021+**: Motioner surpass propositioner in volume and continue accelerating
- **AI density**: Motioner are 70x more AI-focused per word than propositioner

Propositioner led early but plateaued around 2021. Motioner show exponential growth, suggesting MPs are increasingly using AI as an issue for political advocacy while government bills treat AI as one topic among many.

**Visualisations:**
- [Document volume](results/rq4_volume.png) – time series of document counts
- [AI intensity](results/rq4_intensity.png) – AI mentions per 1k words over time
- [Cumulative growth](results/rq4_cumulative.png) – stacked area of corpus growth
- [Timeline](results/rq4_timeline.png) – annotated with key events

### RQ5: Sentiment

| Metric | Motioner | Propositioner |
|--------|----------|---------------|
| Mean sentiment ratio | +1.25 | +0.67 |
| Median sentiment | 0.0 | 0.0 |
| Standard deviation | 2.88 | 1.92 |
| Document count | 443 | 262 |

**Statistical test:** t = 2.92, p = 0.004. The p-value indicates less than 1% probability that the observed difference arose by chance; this difference is statistically significant.

**Interpretation:** Both document types exhibit net positive sentiment around AI mentions, but motioner are significantly more positive:

- **Motioner** use nearly twice as much positive evaluative language in AI contexts (+1.25 vs +0.67)
- **High variance** in motioner (SD 2.88) reflects heterogeneous MP stances – some strongly positive, some negative
- **Median of 0** for both types indicates many documents use neutral language around AI
- **Propositioner** are more consistently neutral/mild – tighter distribution, fewer extreme values

This aligns with RQ1 (framing): MPs deploy more evaluative language overall when discussing AI, while government bills maintain measured, technocratic prose. The sentiment difference is stable across the 2017–2025 period.

**Visualisations:**
- [Sentiment distribution](results/rq5_sentiment_boxplot.png) – boxplot comparing document types
- [Temporal trends](results/rq5_sentiment_timeline.png) – sentiment evolution over time
- [Histogram](results/rq5_sentiment_histogram.png) – frequency distribution of sentiment scores

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
