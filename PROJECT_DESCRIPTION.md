# Campus Pulse - Project Description

## Project Title
**Campus Pulse: Real-Time Campus Facility Monitoring and Crowd Prediction System**

## Project Overview

### Objective
Campus Pulse is an AI-powered web application designed to help University of Florida students, faculty, and staff make informed decisions about when and where to visit campus facilities. The primary goal is to reduce overcrowding, improve user experience, and optimize facility utilization by providing real-time occupancy data and predictive crowd forecasting.

**Expected Outcomes:**
- Enable users to view real-time crowd levels at 25+ campus locations (gyms, libraries, pools, courts)
- Provide 90-minute ahead LSTM-based crowd predictions with 85%+ accuracy
- Reduce wait times and improve facility access through intelligent planning
- Collect user feedback to continuously improve prediction accuracy
- Support event organizers with crowd management for campus events

### Scope

**What the AI System Does:**
- Displays interactive heatmap visualization of current campus facility occupancy
- Generates crowd level predictions using LSTM neural networks
- Classifies crowd levels into categories (Low, Moderate, High, Very High)
- Provides personalized features (saved locations, event tracking, feedback submission)
- Offers role-based access (User, Organizer, Admin) for different functionality levels
- Tracks comprehensive performance metrics for system optimization

**Data Used:**
- **Simulated Crowd Data:** Time-series occupancy data for 25+ campus locations (gyms, libraries, aquatics, courts)
- **Temporal Features:** Hour of day, day of week, exam periods, special events
- **Historical Patterns:** 5,000+ training samples capturing daily, weekly, and seasonal trends
- **User Feedback:** Qualitative feedback and quantitative ratings from users
- **Performance Metrics:** Response times, API latency, page loads, model inference times, database queries

**Limitations:**
- Currently uses simulated data; real sensor integration pending
- Predictions limited to 90-minute forecast window
- No mobile application (web-only for current version)
- Limited to University of Florida campus (single-institution deployment)
- Requires internet connection (no offline mode)

### AI Techniques and Tools

**Machine Learning Algorithms:**
- **LSTM (Long Short-Term Memory) Neural Networks:** Primary forecasting model for time-series crowd prediction
  - Architecture: 2-layer LSTM with 64 hidden units per layer
  - Input: 12 historical data points (2-hour lookback window)
  - Output: 9 future predictions (90-minute forecast)
  - Framework: PyTorch 2.5.1
- **Data Preprocessing:** Normalization, scaling, feature engineering for temporal patterns
- **Performance Tracking:** Statistical analysis for drift detection and model monitoring

**Frameworks and Libraries:**
- **Frontend:** Streamlit 1.40.1 (interactive web application framework)
- **Machine Learning:** PyTorch 2.5.1 (LSTM implementation), Scikit-learn 1.5.2 (preprocessing)
- **Data Processing:** Pandas 2.2.3, NumPy 2.1.3
- **Visualization:** Plotly 5.24.1 (interactive heatmaps), Matplotlib 3.9.2, Seaborn
- **Database:** SQLite3 (user authentication, feedback, performance metrics, sessions)
- **Geospatial:** GeoPy 2.4.1 (location-based services)
- **Security:** bcrypt (password hashing), custom session management

**Development and Deployment Tools:**
- **Version Control:** Git, GitHub
- **Containerization:** Docker (multi-stage builds)
- **Cloud Platform:** Microsoft Azure (App Service, Container Registry)
- **CI/CD:** Automated deployment scripts, GitHub Actions (planned)
- **Monitoring:** Custom performance tracker with SQLite backend
- **Testing:** Manual testing, performance benchmarking

**Performance Optimization:**
- Batch processing for multi-location predictions
- Caching strategies for frequently accessed data
- Efficient database indexing for fast queries
- Container optimization with minimal base images

---

**System Architecture Summary:**
Campus Pulse follows a modular architecture with clear separation of concerns:
- **Presentation Layer:** Streamlit-based web interface with interactive visualizations
- **Business Logic Layer:** ML model inference, data processing, authentication, role management
- **Data Layer:** SQLite databases for persistence, simulated real-time data generation
- **Monitoring Layer:** Comprehensive performance tracking across all system components

**Deployment Status:**
- ✅ Fully functional web application deployed to Azure App Service
- ✅ Containerized with Docker for consistent deployment
- ✅ Performance monitoring system operational (316+ measurements collected)
- ✅ User feedback system active (47 submissions, 3.8/5 avg rating)
- ✅ Admin panel for system management and analytics
- ⚠️ Pending UF IT security review for campus-wide deployment

---

**Project Significance:**
This project demonstrates end-to-end AI system development including problem definition, data collection, model development, deployment, and continuous monitoring. It addresses real-world campus challenges while implementing best practices for trustworthiness, security, performance, and user experience.

**Target Users:**
1. **Students (Primary):** 50,000+ UF students seeking to avoid crowded facilities
2. **Faculty/Staff:** Planning gym visits, library study sessions during low-traffic periods
3. **Event Organizers:** Managing campus events and predicting attendance
4. **Administrators:** Monitoring system performance, user feedback, facility utilization
5. **Facility Managers:** Understanding usage patterns for resource allocation

**Success Metrics:**
- User satisfaction: Target 4.2/5 (Current: 3.8/5)
- Prediction accuracy: Target 85%+ (validation: 87%)
- System uptime: Target 99.5% (Current: 99.8%)
- Response time P95: Target <500ms (4/5 endpoints meeting target)
- Active user adoption: Target 1000+ users within first semester
