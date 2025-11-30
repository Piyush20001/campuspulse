# Campus Pulse: AI-Powered Campus Crowd Intelligence System
## Poster Presentation

---

## Abstract

**Campus Pulse** is an AI-powered web application designed to help University of Florida's 50,000+ students, faculty, and staff make informed decisions about campus facility usage. The system combines **LSTM neural networks** for time-series crowd forecasting, **DistilBERT transformers** for automatic event categorization, and **autoencoder-based anomaly detection** to provide real-time crowd monitoring across 40+ campus locations. Built with Streamlit and PyTorch, the system achieves **99.8% uptime**, **<500ms response times**, and **174ms average ML inference latency**. The platform features an interactive heatmap visualization, personalized location tracking, and intelligent event management—demonstrating a complete AI/ML lifecycle from data simulation to production deployment.

---

## Problem Statement / Research Question

### The Challenge
University of Florida's campus serves **50,000+ students** across **40+ facilities** including gyms, libraries, dining halls, and study spaces. Students frequently encounter:

- **Overcrowded gyms** during peak hours (5-8 PM)
- **Full libraries** during exam periods
- **Long dining hall lines** at meal times
- **No visibility** into real-time facility usage

### Research Questions

1. **Can we accurately predict crowd levels 1-hour ahead** using historical time-series data?
2. **Can transformer-based NLP automatically categorize campus events** to inform crowd expectations?
3. **Can we detect anomalous crowd patterns** that deviate from normal facility usage?

### Project Goals

| Metric | Target | Achieved |
|--------|--------|----------|
| Prediction Accuracy | 85%+ | Under validation |
| System Uptime | 99.5% | **99.8%** |
| User Satisfaction | 4.2/5.0 | 3.8/5.0 |
| Response Time (P95) | <500ms | **<500ms** (4/5 pages) |

---

## Data / Dataset

### Data Generation Strategy

Since real-time sensor integration with UF IT is pending, we developed a **comprehensive simulation system** that generates realistic campus crowd patterns.

### Dataset Statistics

| Attribute | Value |
|-----------|-------|
| **Total Locations** | 40 UF campus venues |
| **Historical Data** | 30+ days per location |
| **Sampling Interval** | 10 minutes |
| **Total Training Points** | 5,000+ |
| **Event Templates** | 100+ real UF events |
| **Training Examples (NLP)** | 140+ labeled events |

### Location Categories (40 Venues)

```
Libraries (3)        : Library West, Marston Science, Health Science
Gyms (4)            : Southwest Rec, Student Rec, Norman Gym, O'Connell Center
Dining (6)          : The Hub, Broward Dining, Gator Dining, Fresh Food Co.
Academic (8)        : Newell Hall, Turlington, Pugh Hall, Weil Hall, etc.
Housing (4)         : Hume Hall, Broward Hall, Jennings Hall, Keys Complex
Study Spots (4)     : Reitz Union, Graham Study Center, Smathers Library
Outdoor Areas (8)   : Plaza of the Americas, Norman Field, Lake Wauberg
```

### Realistic Pattern Simulation

Each location category follows distinct temporal patterns:

| Pattern Type | Morning | Midday | Evening | Night |
|--------------|---------|--------|---------|-------|
| **Library** | 0.4 | 0.6 | **0.8** | 0.3 |
| **Gym** | **0.7** | 0.4 | **0.9** | 0.2 |
| **Dining** | **0.8** | **0.95** | **0.9** | 0.2 |
| **Academic** | 0.6 | **0.85** | 0.5 | 0.1 |
| **Housing** | 0.3 | 0.2 | 0.7 | **0.95** |

### Preprocessing Pipeline

1. **Normalization**: MinMaxScaler (0-1 range)
2. **Sequence Creation**: Sliding window (12 steps = 2 hours)
3. **Noise Injection**: Gaussian noise (σ=0.05) for robustness
4. **Train/Val Split**: 85%/15% stratified

---

## Model or Approach

### AI Lifecycle Management Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CAMPUS PULSE AI LIFECYCLE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │   DATA   │ → │  MODEL   │ → │ TRAINING │ → │  DEPLOY  │        │
│  │GENERATION│   │  DESIGN  │   │   & VAL  │   │ & MONITOR│        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│       │              │              │              │                │
│       ▼              ▼              ▼              ▼                │
│  • Simulator    • LSTM         • PyTorch     • Streamlit           │
│  • 40 locations • DistilBERT   • Adam optim  • Docker              │
│  • Patterns     • Autoencoder  • Early stop  • Azure               │
│  • Events DB    • Random Forest• Cross-val   • Monitoring          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### End-to-End Data Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA GENERATION PIPELINE                               │
└────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
  │   LOCATION DB   │      │ PATTERN LIBRARY │      │   EVENT BANK    │
  │                 │      │                 │      │                 │
  │  • 40 venues    │      │  • Library      │      │  • 100+ UF      │
  │  • GPS coords   │      │  • Gym          │      │    events       │
  │  • Capacities   │      │  • Dining       │      │  • Categories   │
  │  • Categories   │      │  • Academic     │      │  • Attendance   │
  └────────┬────────┘      └────────┬────────┘      └────────┬────────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │      CROWD SIMULATOR          │
                    │                               │
                    │  pattern(t) = base_level      │
                    │    × time_factor(hour)        │
                    │    × day_factor(weekday)      │
                    │    + gaussian_noise(σ=0.05)   │
                    └───────────────┬───────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
  │  TIME-SERIES    │      │   EVENT DATA    │      │  ANOMALY DATA   │
  │     DATA        │      │                 │      │                 │
  │                 │      │  Title + Desc   │      │  Normal +       │
  │  30+ days       │      │      ↓          │      │  Injected       │
  │  10-min intervals│     │  Category label │      │  Anomalies      │
  │  5000+ points   │      │  140+ examples  │      │                 │
  └────────┬────────┘      └────────┬────────┘      └────────┬────────┘
           │                        │                        │
           ▼                        ▼                        ▼
  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
  │  LSTM TRAINING  │      │ BERT TRAINING   │      │ AUTOENC TRAIN   │
  └─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

### ML Training Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              ML TRAINING PIPELINE                                   │
└────────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   RAW DATA      │
                              │   (5000+ pts)   │
                              └────────┬────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────┐
                    │         PREPROCESSING            │
                    │                                  │
                    │  ┌────────┐  ┌────────┐  ┌────┐ │
                    │  │MinMax  │  │Sliding │  │85/ │ │
                    │  │Scaler  │→ │Window  │→ │15  │ │
                    │  │(0-1)   │  │(k=12)  │  │Split│ │
                    │  └────────┘  └────────┘  └────┘ │
                    └──────────────────┬───────────────┘
                                       │
                    ┌──────────────────┴───────────────┐
                    │                                  │
                    ▼                                  ▼
          ┌─────────────────┐                ┌─────────────────┐
          │   TRAIN SET     │                │ VALIDATION SET  │
          │     (85%)       │                │     (15%)       │
          └────────┬────────┘                └────────┬────────┘
                   │                                  │
                   ▼                                  │
┌──────────────────────────────────────┐             │
│           TRAINING LOOP              │             │
│  ┌─────────────────────────────────┐ │             │
│  │  for epoch in range(100):       │ │             │
│  │      for batch in train_loader: │ │             │
│  │          ┌───────────┐          │ │             │
│  │          │  Forward  │          │ │             │
│  │          │   Pass    │          │ │             │
│  │          └─────┬─────┘          │ │             │
│  │                ▼                │ │             │
│  │          ┌───────────┐          │ │             │
│  │          │   Loss    │          │ │             │
│  │          │   (MSE)   │          │ │             │
│  │          └─────┬─────┘          │ │             │
│  │                ▼                │ │             │
│  │          ┌───────────┐          │ │             │
│  │          │ Backward  │          │ │             │
│  │          │   Pass    │          │ │             │
│  │          └─────┬─────┘          │ │             │
│  │                ▼                │ │             │
│  │          ┌───────────┐          │ │             │
│  │          │  Adam     │          │ │             │
│  │          │ Optimize  │          │ │             │
│  │          └───────────┘          │ │             │
│  └─────────────────────────────────┘ │             │
└──────────────────┬───────────────────┘             │
                   │                                  │
                   └──────────────┬───────────────────┘
                                  ▼
                    ┌──────────────────────────────────┐
                    │         VALIDATION               │
                    │                                  │
                    │  • Compute val_loss              │
                    │  • Early stopping check          │
                    │  • Save best model checkpoint    │
                    └──────────────────┬───────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  SAVED MODEL    │
                              │  (.pth file)    │
                              └─────────────────┘
```

---

### Real-Time Inference Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           REAL-TIME INFERENCE PIPELINE                              │
└────────────────────────────────────────────────────────────────────────────────────┘

     USER REQUEST                    SYSTEM PROCESSING                    RESPONSE
  ┌──────────────┐              ┌─────────────────────┐              ┌──────────────┐
  │              │              │                     │              │              │
  │  "Show me    │              │   ┌─────────────┐   │              │  Heatmap +   │
  │   crowd      │─────────────▶│   │   ROUTER    │   │─────────────▶│  Forecasts + │
  │   levels"    │              │   └──────┬──────┘   │              │  Alerts      │
  │              │              │          │          │              │              │
  └──────────────┘              │          ▼          │              └──────────────┘
                                │   ┌──────────────┐  │
                                │   │  PARALLEL    │  │
                                │   │  INFERENCE   │  │
                                │   └──────┬───────┘  │
                                │          │          │
                                └──────────┼──────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
    ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
    │  LSTM FORECASTER │        │ EVENT CLASSIFIER │        │ ANOMALY DETECTOR │
    │                  │        │                  │        │                  │
    │ Input: 12 steps  │        │ Input: text      │        │ Input: 12 steps  │
    │      ↓           │        │      ↓           │        │      ↓           │
    │ ┌──────────────┐ │        │ ┌──────────────┐ │        │ ┌──────────────┐ │
    │ │ LSTM Layer 1 │ │        │ │  DistilBERT  │ │        │ │   Encoder    │ │
    │ │   (64 units) │ │        │ │  (66M params)│ │        │ │  [12→8→4]    │ │
    │ └──────┬───────┘ │        │ └──────┬───────┘ │        │ └──────┬───────┘ │
    │        ↓         │        │        ↓         │        │        ↓         │
    │ ┌──────────────┐ │        │ ┌──────────────┐ │        │ ┌──────────────┐ │
    │ │ LSTM Layer 2 │ │        │ │  Classifier  │ │        │ │   Decoder    │ │
    │ │   (64 units) │ │        │ │ [768→256→4]  │ │        │ │  [4→8→12]    │ │
    │ └──────┬───────┘ │        │ └──────┬───────┘ │        │ └──────┬───────┘ │
    │        ↓         │        │        ↓         │        │        ↓         │
    │ ┌──────────────┐ │        │ ┌──────────────┐ │        │ ┌──────────────┐ │
    │ │   Dropout    │ │        │ │   Softmax    │ │        │ │ Recon Error  │ │
    │ │    (0.2)     │ │        │ │  + Temp(1.5) │ │        │ │  Threshold   │ │
    │ └──────┬───────┘ │        │ └──────┬───────┘ │        │ └──────┬───────┘ │
    │        ↓         │        │        ↓         │        │        ↓         │
    │ ┌──────────────┐ │        │ ┌──────────────┐ │        │ ┌──────────────┐ │
    │ │  Dense → 6   │ │        │ │   4 Classes  │ │        │ │   Severity   │ │
    │ │  predictions │ │        │ │ + Confidence │ │        │ │    Level     │ │
    │ └──────────────┘ │        │ └──────────────┘ │        │ └──────────────┘ │
    │                  │        │                  │        │                  │
    │  Output: 1-hour  │        │ Output: Category │        │ Output: Normal/  │
    │  forecast (6 pts)│        │ + 0-100% conf    │        │ Medium/High/Crit │
    │                  │        │                  │        │                  │
    │  Latency: 177ms  │        │  Latency: 199ms  │        │  Latency: 146ms  │
    └──────────────────┘        └──────────────────┘        └──────────────────┘
              │                            │                            │
              └────────────────────────────┼────────────────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │    RESPONSE AGGREGATOR   │
                              │                          │
                              │  • Merge predictions     │
                              │  • Format for UI         │
                              │  • Cache results         │
                              │                          │
                              │  Total Latency: <300ms   │
                              └──────────────────────────┘
```

---

### User Request Flow

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              USER REQUEST FLOW                                      │
└────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────┐
    │  USER   │
    └────┬────┘
         │
         │ HTTP Request
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 STREAMLIT APP                                        │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PAGE ROUTER                                        │ │
│  │                                                                                 │ │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │ │
│  │   │   Home   │  │  Crowd   │  │  Events  │  │  Saved   │  │  Admin   │       │ │
│  │   │   Page   │  │  Heatmap │  │   Page   │  │Locations │  │  Panel   │       │ │
│  │   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │ │
│  │        │             │             │             │             │              │ │
│  └────────┼─────────────┼─────────────┼─────────────┼─────────────┼──────────────┘ │
│           │             │             │             │             │                │
│           ▼             ▼             ▼             ▼             ▼                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                           SERVICE LAYER                                      │  │
│  │                                                                              │  │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │  │
│  │  │   Auth      │   │  Database   │   │    ML       │   │ Monitoring  │     │  │
│  │  │  Service    │   │   Service   │   │  Service    │   │  Service    │     │  │
│  │  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘     │  │
│  │         │                 │                 │                 │             │  │
│  └─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘  │
│            │                 │                 │                 │                │
│            ▼                 ▼                 ▼                 ▼                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                          DATA LAYER                                          │  │
│  │                                                                              │  │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │  │
│  │  │   SQLite    │   │   Session   │   │   Model     │   │   Metrics   │     │  │
│  │  │     DB      │   │    State    │   │  Checkpoints│   │    Store    │     │  │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │  │
│  │                                                                              │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

### LSTM Architecture Detail

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                         LSTM FORECASTER ARCHITECTURE                                │
└────────────────────────────────────────────────────────────────────────────────────┘

   INPUT SEQUENCE (12 time steps = 2 hours of history)
   ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
   │ t-11│ t-10│ t-9│ t-8│ t-7│ t-6│ t-5│ t-4│ t-3│ t-2│ t-1│ t  │
   │0.45│0.48│0.52│0.55│0.58│0.62│0.65│0.68│0.71│0.74│0.77│0.80│
   └──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┘
      │    │    │    │    │    │    │    │    │    │    │    │
      ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
   ┌────────────────────────────────────────────────────────────┐
   │                    LSTM LAYER 1 (64 units)                 │
   │  ┌──────┐ ┌──────┐ ┌──────┐         ┌──────┐ ┌──────┐    │
   │  │ LSTM │→│ LSTM │→│ LSTM │→  ...  →│ LSTM │→│ LSTM │    │
   │  │ Cell │ │ Cell │ │ Cell │         │ Cell │ │ Cell │    │
   │  └──┬───┘ └──┬───┘ └──┬───┘         └──┬───┘ └──┬───┘    │
   │     │h₁     │h₂     │h₃            │h₁₁    │h₁₂        │
   │     ▼        ▼        ▼              ▼        ▼          │
   └─────┼────────┼────────┼──────────────┼────────┼──────────┘
         │        │        │              │        │
         ▼        ▼        ▼              ▼        ▼
   ┌────────────────────────────────────────────────────────────┐
   │                    LSTM LAYER 2 (64 units)                 │
   │  ┌──────┐ ┌──────┐ ┌──────┐         ┌──────┐ ┌──────┐    │
   │  │ LSTM │→│ LSTM │→│ LSTM │→  ...  →│ LSTM │→│ LSTM │───┐│
   │  │ Cell │ │ Cell │ │ Cell │         │ Cell │ │ Cell │   ││
   │  └──────┘ └──────┘ └──────┘         └──────┘ └──────┘   ││
   └─────────────────────────────────────────────────────┬────┘│
                                                         │     │
                                    Hidden State (64-dim)│     │
                                                         ▼     │
                                    ┌────────────────────────┐ │
                                    │    DROPOUT (p=0.2)     │ │
                                    │    Regularization      │ │
                                    └───────────┬────────────┘ │
                                                │              │
                                                ▼              │
                                    ┌────────────────────────┐ │
                                    │    DENSE LAYER         │ │
                                    │    64 → 6 units        │ │
                                    │    (Linear activation) │ │
                                    └───────────┬────────────┘ │
                                                │              │
                                                ▼              │
   OUTPUT SEQUENCE (6 time steps = 1 hour forecast)           │
   ┌────┬────┬────┬────┬────┬────┐                            │
   │t+1 │t+2 │t+3 │t+4 │t+5 │t+6 │  ◄─────────────────────────┘
   │0.82│0.84│0.85│0.86│0.85│0.83│
   └────┴────┴────┴────┴────┴────┘
    +10   +20   +30   +40   +50   +60 minutes
```

---

### DistilBERT Event Classifier Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                      DISTILBERT EVENT CLASSIFIER                                    │
└────────────────────────────────────────────────────────────────────────────────────┘

   INPUT: Event Title + Description
   ┌─────────────────────────────────────────────────────────────────────────────────┐
   │  "Annual Career Fair - Meet top employers and explore internship opportunities" │
   └─────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │       TOKENIZER          │
                              │                          │
                              │  • WordPiece tokenization│
                              │  • Max length: 128       │
                              │  • [CLS] ... [SEP]       │
                              └────────────┬─────────────┘
                                           │
      Token IDs: [101, 2093, 3040, 2469, ..., 102, 0, 0, 0]
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         DISTILBERT ENCODER (66M params)                           │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                        EMBEDDING LAYER                                      │  │
│  │   Token Embeddings (30522 × 768) + Position Embeddings (512 × 768)         │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                            │
│                                      ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                     TRANSFORMER BLOCKS × 6                                  │  │
│  │  ┌──────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Multi-Head Self-Attention (12 heads, 768 dim)                       │  │  │
│  │  │         ↓                                                            │  │  │
│  │  │  Layer Norm + Residual                                               │  │  │
│  │  │         ↓                                                            │  │  │
│  │  │  Feed-Forward (768 → 3072 → 768)                                     │  │  │
│  │  │         ↓                                                            │  │  │
│  │  │  Layer Norm + Residual                                               │  │  │
│  │  └──────────────────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                            │
│                           [CLS] Token Embedding (768-dim)                         │
└──────────────────────────────────────┬───────────────────────────────────────────┘
                                       │
     ┌─────────────────────────────────┴─────────────────────────────────┐
     │              PHASE 1: FROZEN          PHASE 2: FINE-TUNED         │
     │              (Epochs 0-4)              (Epochs 5-14)               │
     └─────────────────────────────────┬─────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         CLASSIFICATION HEAD                                       │
│                                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  Dense(768 → 256) → BatchNorm → ReLU → Dropout(0.3)                     │   │
│   └────────────────────────────────────┬────────────────────────────────────┘   │
│                                        │                                         │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  Dense(256 → 128) → BatchNorm → ReLU → Dropout(0.21)                    │   │
│   └────────────────────────────────────┬────────────────────────────────────┘   │
│                                        │                                         │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  Dense(128 → 4) → Softmax / Temperature(1.5)                            │   │
│   └────────────────────────────────────┬────────────────────────────────────┘   │
│                                        │                                         │
└────────────────────────────────────────┼─────────────────────────────────────────┘
                                         │
                                         ▼
                        ┌────────────────────────────────────┐
                        │           OUTPUT                   │
                        │                                    │
                        │   Academic:  0.89  ████████████▓   │
                        │   Social:    0.06  ██               │
                        │   Sports:    0.03  █                │
                        │   Cultural:  0.02  █                │
                        │                                    │
                        │   Prediction: ACADEMIC (89%)       │
                        └────────────────────────────────────┘
```

---

### Autoencoder Anomaly Detection Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                      AUTOENCODER ANOMALY DETECTOR                                   │
└────────────────────────────────────────────────────────────────────────────────────┘

                           NORMAL DATA (Training)
   ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
   │0.45│0.48│0.52│0.55│0.58│0.62│0.65│0.68│0.71│0.74│0.77│0.80│  Input (12-dim)
   └──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┘
      │    │    │    │    │    │    │    │    │    │    │    │
      └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
                                 │
                                 ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                        ENCODER                               │
   │  ┌────────────────────────────────────────────────────────┐  │
   │  │  Dense(12 → 8) + ReLU                                  │  │
   │  │      ↓                                                 │  │
   │  │  Dense(8 → 4) + ReLU                                   │  │
   │  └────────────────────────────────────────────────────────┘  │
   └──────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   LATENT SPACE   │
                    │     (4-dim)      │
                    │                  │
                    │  Compressed      │
                    │  Representation  │
                    └────────┬─────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                        DECODER                               │
   │  ┌────────────────────────────────────────────────────────┐  │
   │  │  Dense(4 → 8) + ReLU                                   │  │
   │  │      ↓                                                 │  │
   │  │  Dense(8 → 12) + Sigmoid                               │  │
   │  └────────────────────────────────────────────────────────┘  │
   └──────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
   ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
   │0.46│0.49│0.51│0.54│0.59│0.61│0.66│0.67│0.72│0.73│0.78│0.79│  Reconstruction
   └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘


   ═══════════════════════════════════════════════════════════════
                        ANOMALY DETECTION
   ═══════════════════════════════════════════════════════════════

   NORMAL INPUT:                          ANOMALOUS INPUT:
   ┌─────────────────────────┐            ┌─────────────────────────┐
   │ 0.45 0.48 0.52 ... 0.80 │            │ 0.45 0.48 0.95 ... 0.30 │
   └────────────┬────────────┘            └────────────┬────────────┘
                │                                      │
                ▼                                      ▼
   ┌─────────────────────────┐            ┌─────────────────────────┐
   │     RECONSTRUCTION      │            │     RECONSTRUCTION      │
   │ 0.46 0.49 0.51 ... 0.79 │            │ 0.47 0.50 0.58 ... 0.55 │
   └────────────┬────────────┘            └────────────┬────────────┘
                │                                      │
                ▼                                      ▼
   ┌─────────────────────────┐            ┌─────────────────────────┐
   │   MSE = 0.002           │            │   MSE = 0.18            │
   │   < threshold (0.15)    │            │   > threshold (0.15)    │
   └────────────┬────────────┘            └────────────┬────────────┘
                │                                      │
                ▼                                      ▼
        ┌──────────────┐                      ┌──────────────┐
        │   NORMAL     │                      │   ANOMALY    │
        │   ✓          │                      │   ⚠ HIGH     │
        └──────────────┘                      └──────────────┘


   SEVERITY SCALE:
   ┌─────────────────────────────────────────────────────────────────┐
   │                                                                 │
   │  0.00    0.15      0.20       0.25       0.30                  │
   │    │───────│─────────│──────────│──────────│────────▶          │
   │  NORMAL  MEDIUM     HIGH     CRITICAL                          │
   │    ✓       ⚠         ⚠⚠        ⚠⚠⚠                            │
   │                                                                 │
   └─────────────────────────────────────────────────────────────────┘
```

---

### Deployment Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                            DEPLOYMENT PIPELINE                                      │
└────────────────────────────────────────────────────────────────────────────────────┘

   DEVELOPMENT                    BUILD                         PRODUCTION
   ───────────                    ─────                         ──────────

   ┌─────────────┐
   │   GitHub    │
   │ Repository  │
   └──────┬──────┘
          │
          │ git push
          ▼
   ┌─────────────┐          ┌─────────────┐          ┌─────────────────────┐
   │   CI/CD     │          │   Docker    │          │   Azure App         │
   │  Pipeline   │─────────▶│   Build     │─────────▶│    Service          │
   │  (GitHub    │          │             │          │                     │
   │   Actions)  │          │ • Multi-    │          │  ┌───────────────┐  │
   └─────────────┘          │   stage     │          │  │  Container    │  │
                            │ • Python    │          │  │   Instance    │  │
   ┌─────────────┐          │   3.11      │          │  │               │  │
   │   Tests     │          │ • PyTorch   │          │  │  Streamlit    │  │
   │             │          │ • Models    │          │  │  App (8501)   │  │
   │ • Unit      │          │             │          │  │               │  │
   │ • Integra-  │          └──────┬──────┘          │  └───────┬───────┘  │
   │   tion      │                 │                 │          │          │
   │ • Model     │                 ▼                 │          ▼          │
   │   validation│          ┌─────────────┐          │  ┌───────────────┐  │
   └─────────────┘          │   Azure     │          │  │   Load        │  │
                            │  Container  │─────────▶│  │   Balancer    │  │
                            │  Registry   │          │  │               │  │
                            │             │          │  └───────────────┘  │
                            │  campuspulse│          │                     │
                            │  :latest    │          └─────────────────────┘
                            └─────────────┘
                                                               │
                                                               ▼
                                                     ┌─────────────────────┐
                                                     │    MONITORING       │
                                                     │                     │
                                                     │  • Response times   │
                                                     │  • Error rates      │
                                                     │  • ML inference     │
                                                     │  • User metrics     │
                                                     │                     │
                                                     │  316+ data points   │
                                                     └─────────────────────┘
```

---

### Model 1: LSTM Time-Series Forecaster

**Purpose**: Predict crowd levels 1-hour ahead (6 time steps)

**Architecture**:
```
Input (12 timesteps) → LSTM(64, 2 layers) → Dropout(0.2) → Dense(6) → Output
```

| Hyperparameter | Value |
|----------------|-------|
| Hidden Units | 64 |
| LSTM Layers | 2 |
| Sequence Length | 12 (2 hours) |
| Forecast Horizon | 6 (1 hour) |
| Dropout | 0.2 |
| Optimizer | Adam (lr=0.001) |
| Loss | MSE + L2 regularization |
| Epochs | 100 |

**Key Design Decisions**:
- Univariate approach (crowd level only) for simplicity
- Persistence baseline fallback when model unavailable
- Output clipping to valid [0, 1] range

---

### Model 2: DistilBERT Event Classifier

**Purpose**: Automatically categorize campus events (Academic, Social, Sports, Cultural)

**Architecture**:
```
Text Input → DistilBERT Encoder (66M params) → Classification Head → 4 Classes
                                                      │
                                    ┌─────────────────┴─────────────────┐
                                    │ Dense(768→256) + BN + ReLU + Drop │
                                    │ Dense(256→128) + BN + ReLU + Drop │
                                    │ Dense(128→4) → Softmax            │
                                    └───────────────────────────────────┘
```

**Two-Phase Training Strategy**:

| Phase | Epochs | Learning Rate | Description |
|-------|--------|---------------|-------------|
| **Phase 1** | 0-4 | 2e-5 | Freeze encoder, train classifier head |
| **Phase 2** | 5-14 | 2e-6 | Unfreeze encoder, fine-tune full model |

**Additional Techniques**:
- Linear warmup (10% of steps) + linear decay
- Gradient clipping (max_norm=1.0)
- Early stopping (patience=3)
- Temperature scaling (T=1.5) for calibration

---

### Model 3: Autoencoder Anomaly Detector

**Purpose**: Detect unusual crowd patterns (spikes, drops, irregular behavior)

**Architecture**:
```
Input (12) → Encoder[12→8→4] → Latent(4) → Decoder[4→8→12] → Reconstruction
```

**Anomaly Detection Method**:
- Train on normal data only
- Compute reconstruction error at inference
- Threshold: 0.15 (95th percentile of training errors)
- Severity levels: Normal → Medium → High → Critical

---

### Model 4: Random Forest (Alternative)

**Purpose**: Backup predictor with interpretable features

| Parameter | Value |
|-----------|-------|
| Estimators | 200 trees |
| Max Depth | 20 |
| Features | 20 (temporal, spatial, contextual) |
| Test R² | ~0.85 |

**Feature Engineering** (20 features):
- Temporal: hour, day_of_week, month, sin/cos encodings
- Contextual: is_peak_hour, is_class_time, is_late_night
- External: weather conditions, exam periods, holidays

---

## Results & Evaluation

### System Performance Metrics

**Total Measurements**: 316 data points across 5 categories

#### Response Time Analysis

```
                    Response Time by Endpoint (ms)
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
400 │                                    ████                │
    │                              ████  ████                │
300 │        ████           ████  ████  ████  ████          │
    │  ████  ████     ████  ████  ████  ████  ████          │
200 │  ████  ████     ████  ████  ████  ████  ████          │
    │  ████  ████     ████  ████  ████  ████  ████          │
100 │  ████  ████     ████  ████  ████  ████  ████          │
    │  ████  ████     ████  ████  ████  ████  ████          │
  0 └────────────────────────────────────────────────────────┘
      Admin  Crowd    Events  Home   Profile  API   DB
      Panel  Heatmap  Page    Page   Page    Latency Query
      248ms  314ms    246ms   392ms  284ms   93ms   79ms
```

| Endpoint | Avg (ms) | P95 (ms) | Status |
|----------|----------|----------|--------|
| Admin Panel | 248 | 403 | ✅ Excellent |
| Crowd Heatmap | 314 | 474 | ✅ Excellent |
| Events Page | 246 | 443 | ✅ Excellent |
| Profile Page | 284 | 450 | ✅ Excellent |
| Home Page | 392 | 1913 | ⚠️ Needs optimization |

---

### ML Model Inference Performance

```
              ML Model Inference Time (ms)
    ┌──────────────────────────────────────────────┐
    │                                              │
250 │              ████                            │
    │        ████  ████  ████                      │
200 │        ████  ████  ████                      │
    │  ████  ████  ████  ████                      │
150 │  ████  ████  ████  ████                      │
    │  ████  ████  ████  ████                      │
100 │  ████  ████  ████  ████                      │
    │  ████  ████  ████  ████                      │
 50 │  ████  ████  ████  ████                      │
    │  ████  ████  ████  ████                      │
  0 └──────────────────────────────────────────────┘
      Anomaly  LSTM    Event    Random
      Detector Forecast Classifier Forest
      146ms    177ms    199ms     ~50ms
```

| Model | Avg Latency | P95 Latency | Per-Prediction |
|-------|-------------|-------------|----------------|
| **LSTM Forecaster** | 177 ms | 262 ms | 25.3 ms |
| **Event Classifier** | 199 ms | 277 ms | 43.3 ms |
| **Anomaly Detector** | 146 ms | 245 ms | 23.9 ms |

---

### Database Performance

| Operation | Avg Latency (ms) |
|-----------|------------------|
| INSERT (feedback) | 79 |
| SELECT (events) | 90 |
| SELECT (users) | 90 |
| UPDATE (roles) | 55 |

---

### User Feedback Summary

```
              User Satisfaction Distribution
    ┌──────────────────────────────────────────────┐
    │                                              │
 20 │                    ████████                  │
    │              ████  ████████                  │
 15 │        ████  ████  ████████  ████           │
    │        ████  ████  ████████  ████           │
 10 │  ████  ████  ████  ████████  ████           │
    │  ████  ████  ████  ████████  ████           │
  5 │  ████  ████  ████  ████████  ████           │
    │  ████  ████  ████  ████████  ████           │
  0 └──────────────────────────────────────────────┘
       1★     2★     3★     4★      5★
```

- **Total Submissions**: 47
- **Average Rating**: 3.8/5.0
- **Target**: 4.2/5.0

---

### System Reliability

| Metric | Target | Achieved |
|--------|--------|----------|
| **Uptime** | 99.5% | **99.8%** ✅ |
| **Request Success Rate** | 99%+ | **100%** ✅ |
| **Database Availability** | 99.5% | **100%** ✅ |

---

## Key Takeaways / Discussion

### What Worked Well

| Aspect | Success Factor |
|--------|----------------|
| **Multi-Model Architecture** | Specialized models for different tasks (LSTM for time-series, Transformer for NLP, Autoencoder for anomaly) outperformed single general-purpose approaches |
| **Two-Phase Transfer Learning** | Freezing DistilBERT encoder initially, then fine-tuning, prevented catastrophic forgetting with limited data (140 examples) |
| **Realistic Data Simulation** | Category-specific temporal patterns created high-fidelity synthetic data for training |
| **Performance Monitoring** | Continuous metrics collection (316+ measurements) enabled rapid identification of bottlenecks |
| **Containerized Deployment** | Docker + Azure provided consistent, scalable deployment |

### Challenges & Lessons Learned

| Challenge | Solution Applied |
|-----------|------------------|
| **Limited Real Data** | Developed comprehensive simulator with domain-specific patterns |
| **Home Page Latency Spike** | Identified as priority; Redis caching planned |
| **Model Cold Start** | Implemented persistence baseline fallbacks |
| **Event Classification Confidence** | Added temperature scaling (T=1.5) for better calibration |
| **Real-time Requirements** | Optimized inference to <200ms per model |

### What Didn't Work

1. **Single LSTM for All Locations**: Location-specific patterns required per-category model tuning
2. **High Learning Rate for Fine-tuning**: Caused instability; reduced 10x for encoder unfreezing
3. **Complex Feature Engineering for LSTM**: Univariate approach outperformed multivariate on limited data

### Future Improvements

1. **Real Sensor Integration**: Partner with UF IT for actual occupancy data
2. **Federated Learning**: Privacy-preserving training across facilities
3. **Graph Neural Networks**: Model spatial relationships between locations
4. **Reinforcement Learning**: Optimize crowd distribution recommendations
5. **Mobile App**: Push notifications for crowd alerts

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAMPUS PULSE ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │   FRONTEND  │    │   BACKEND   │    │  ML MODELS  │                 │
│  │  Streamlit  │◄──►│   Python    │◄──►│   PyTorch   │                 │
│  │  + Folium   │    │  + SQLite   │    │ Transformers│                 │
│  └─────────────┘    └─────────────┘    └─────────────┘                 │
│         │                  │                  │                         │
│         ▼                  ▼                  ▼                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │ Interactive │    │    Auth     │    │    LSTM     │                 │
│  │   Heatmap   │    │   System    │    │  Forecaster │                 │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤                 │
│  │   Events    │    │  Database   │    │ DistilBERT  │                 │
│  │   Browser   │    │   Layer     │    │ Classifier  │                 │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤                 │
│  │   Profile   │    │ Monitoring  │    │ Autoencoder │                 │
│  │  Dashboard  │    │   Module    │    │  Detector   │                 │
│  └─────────────┘    └─────────────┘    └─────────────┘                 │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     DEPLOYMENT LAYER                             │   │
│  │         Docker → Azure App Service → Performance Monitoring      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Streamlit 1.40, Folium, Plotly 5.24 |
| **Backend** | Python 3.11+, SQLite3 |
| **ML/AI** | PyTorch 2.5, Transformers 4.30+, scikit-learn 1.5 |
| **Deployment** | Docker, Azure App Service |
| **Monitoring** | Custom performance module (316+ metrics) |

---

## References & Resources

- **Project Repository**: github.com/Piyush20001/campuspulse
- **LSTM Architecture**: Hochreiter & Schmidhuber (1997)
- **DistilBERT**: Sanh et al. (2019) - "DistilBERT, a distilled version of BERT"
- **Autoencoder Anomaly Detection**: Chalapathy & Chawla (2019)
- **Streamlit Documentation**: docs.streamlit.io
- **PyTorch Documentation**: pytorch.org/docs

---

## Contact

**Team**: Campus Pulse Development Team
**Institution**: University of Florida
**Course**: AI/ML Systems Development
**Date**: November 2025

---

*This poster demonstrates the complete AI/ML lifecycle: data generation → model design → training & validation → deployment & monitoring*
