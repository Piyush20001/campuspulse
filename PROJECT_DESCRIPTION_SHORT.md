# Campus Pulse - Short Project Description

**Use this concise version for your AI System Project Template submissions**

---

## For Template Section: "Project Overview"

**Project Title:**
Campus Pulse: Real-Time Campus Facility Monitoring and Crowd Prediction System

**Objective:**
Campus Pulse aims to reduce overcrowding at University of Florida facilities by providing students and faculty with real-time occupancy data and AI-powered crowd predictions. The system enables users to make informed decisions about when to visit 25+ campus locations including gyms, libraries, pools, and courts. Expected outcomes include reduced wait times, optimized facility utilization, and improved user experience through 90-minute ahead LSTM-based crowd forecasting with 85%+ accuracy.

**Scope:**
The AI system displays an interactive heatmap of current campus facility occupancy and generates crowd level predictions using LSTM neural networks. It uses time-series occupancy data for 25+ locations with temporal features (hour, day of week, exam periods, events) trained on 5,000+ historical samples. The system provides personalized features including saved locations, event tracking, and feedback submission through role-based access (User, Organizer, Admin). Limitations include simulated data (real sensor integration pending), 90-minute forecast window, web-only interface, single-institution deployment, and internet requirement.

**AI Techniques and Tools:**
The system employs **LSTM (Long Short-Term Memory) neural networks** implemented in PyTorch 2.5.1 for time-series crowd prediction with a 2-layer architecture (64 hidden units per layer). The web application is built with **Streamlit 1.40.1**, using **Pandas 2.2.3** and **NumPy 2.1.3** for data processing, **Plotly 5.24.1** for interactive visualizations, and **SQLite3** for database management. Deployment utilizes **Docker** containerization on **Microsoft Azure App Service** with automated deployment scripts and custom performance monitoring.

---

## Even Shorter Version (2-3 Sentences)

Campus Pulse is an AI-powered web application that provides University of Florida students with real-time occupancy data and 90-minute crowd predictions for 25+ campus facilities using LSTM neural networks. The system processes time-series data with PyTorch and delivers predictions through an interactive Streamlit-based heatmap interface, deployed on Azure App Service using Docker containerization. Performance monitoring tracks 316+ measurements across response times, API latency, page loads, ML inference, and database queries to ensure optimal system performance.

---

## Copy-Paste Template Fill-In

**[Insert Project Title]**
Campus Pulse: Real-Time Campus Facility Monitoring and Crowd Prediction System

**[Insert project overview considering the following items]**

**Objective:**
Reduce overcrowding at University of Florida facilities by providing real-time occupancy data and AI-powered 90-minute crowd predictions for 25+ campus locations. Expected outcomes: 85%+ prediction accuracy, reduced wait times, optimized facility utilization, and improved user experience.

**Scope:**
The system displays interactive heatmap visualizations of current facility occupancy and generates LSTM-based crowd predictions. Uses time-series data for 25+ locations with temporal features (hour, day, exam periods) trained on 5,000+ samples. Provides saved locations, event tracking, feedback submission, and role-based access (User/Organizer/Admin). Limitations: simulated data, 90-minute forecast window, web-only, single institution, requires internet.

**AI Techniques and Tools:**
- **Algorithms:** LSTM neural networks (2-layer, 64 hidden units) for time-series forecasting
- **ML Framework:** PyTorch 2.5.1
- **Web Framework:** Streamlit 1.40.1
- **Data Processing:** Pandas 2.2.3, NumPy 2.1.3
- **Visualization:** Plotly 5.24.1, Matplotlib 3.9.2
- **Database:** SQLite3
- **Deployment:** Docker, Microsoft Azure App Service
- **Monitoring:** Custom performance tracker (response times, API latency, model inference)
