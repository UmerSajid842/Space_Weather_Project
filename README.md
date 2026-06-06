
# Space_Weather_Project
# 📡 Explainable AI-Based Space Weather Forecasting and Solar Activity Monitoring

An end-to-end **AI-powered space weather intelligence system** that analyzes, forecasts, and explains solar activity using satellite observations from NASA and NOAA data sources. The project combines **Machine Learning, Time Series Forecasting, Anomaly Detection, and Explainable AI (XAI)** to support real-world space weather monitoring.

---

## 🚀 Project Overview

Space weather events such as solar flares and geomagnetic storms can disrupt satellites, GPS systems, aviation, and power grids. This project builds an intelligent system that:

- Monitors solar activity in real time  
- Predicts future solar flux behavior  
- Detects anomalies in space weather data  
- Explains AI predictions using SHAP  
- Provides interactive dashboards for decision-making  

---

## 🧠 Key Features

### 📊 Data Processing
- NASA & NOAA space weather datasets
- Multi-source data fusion
- Time-series preprocessing and cleaning
- Feature engineering (lag features, rolling averages, normalization)

### 🤖 Machine Learning Models
- Random Forest Classifier (Risk prediction)
- Isolation Forest (Anomaly detection)
- ARIMA (Time series forecasting)
- LSTM (Deep learning-based forecasting)

### 🔍 Explainable AI (XAI)
- SHAP feature importance analysis
- Model interpretability for predictions
- Feature contribution visualization

### 📈 Visualization & Dashboard
- Streamlit interactive dashboard
- Power BI reporting dashboard (optional extension)
- Real-time KPI monitoring
- Solar flux trend analysis
- Anomaly visualization

---

## 📁 Project Structure


📦 Space-Weather-AI
├── dashboard.py
├── Space_Weather_Project.ipynb
├── BI_Dashboard_Telemetry_Data.csv
├── final_fused_space_weather.csv
├── forecast_results.csv
├── lstm_forecast.csv
├── model_metrics.csv
├── shap_explainability_analysis.png
└── README.md


---

## 📊 Dashboard Features

### 🔭 Overview Page
- Solar flux monitoring
- Sunspot activity trends
- Key performance indicators (KPIs)
- Date filtering

### 🔮 Forecasting
- ARIMA-based predictions
- LSTM-based predictions
- Actual vs predicted comparison

### ⚠️ Anomaly Detection
- Isolation Forest-based detection
- Highlighted anomaly timeline
- Event-based analysis

### 🧠 Explainability
- SHAP feature importance visualization
- Model transparency insights

### 📉 Model Comparison
- ARIMA vs LSTM performance
- RMSE and MAE comparison
- Best model selection

---

## 📦 Installation

```bash
git clone https://github.com/your-username/space-weather-ai.git
cd space-weather-ai

pip install -r requirements.txt
▶️ Run Streamlit Dashboard
streamlit run dashboard.py
📊 Power BI Dashboard (Optional)

To use Power BI version:

Open Power BI Desktop
Import CSV files from /data folder
Create relationships using time_tag and Date
Use built-in visuals for KPIs and forecasting
🧪 Technologies Used
Python 🐍
Pandas & NumPy
Scikit-learn
Statsmodels (ARIMA)
TensorFlow / Keras (LSTM)
SHAP (Explainability)
Streamlit
Power BI
Plotly & Matplotlib
📌 Key Insights
Solar activity follows strong cyclical patterns
Sunspot count correlates with solar flux intensity
LSTM outperforms ARIMA in most forecasting cases
Anomaly detection highlights extreme solar events
Explainable AI improves trust in predictions
⚠️ Applications
Satellite communication safety
GPS and navigation protection
Power grid disturbance prevention
Aviation route planning
Space mission monitoring
📈 Future Improvements
Real-time NASA API streaming
Cloud deployment (AWS / Azure)
Deep Transformer-based forecasting
Live alert system for solar storms
Mobile dashboard version
👨‍💻 Author

Umer Sajid
MS Data Science
Research Focus: Explainable AI & Time Series Forecasting

📜 License

This project is for academic and research purposes.
