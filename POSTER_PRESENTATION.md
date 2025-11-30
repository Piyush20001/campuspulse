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
