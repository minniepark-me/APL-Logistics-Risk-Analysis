🚢 APL Logistics: Global Supply Chain Risk Analysis
Internship Project 2 | Unified Mentor

📌 Project Overview
This project focuses on identifying and mitigating global supply chain disruptions for APL Logistics. Using Python and Streamlit, I developed a risk-assessment dashboard that identifies regional bottlenecks and correlates shipping modes with delivery failures.

The goal of this analysis is to provide data-driven insights that can reduce perceived failure rates from 57% to <10% through strategic interventions.

🚀 Key Features & Analytics
Geospatial Risk Mapping: Visualizes "Critical Zones" in the USA and LATAM markets where delay volumes are highest.

Root Cause Diagnostics: A heatmap-based correlation between "Standard Class" shipping and a 60% late delivery rate.

SLA Compliance Tracking: Identifies the 1.6-day latency gap between promised and actual delivery times.

Strategic Action Alerts: A dedicated interface for real-time recommendations, such as implementing a "VIP Lane" for corporate revenue protection.

🛠️ Tech Stack & Methodology
Language: Python 3.x

Library Suite: Pandas for data wrangling, Plotly for interactive geospatial maps, and Streamlit for the web interface.

Data Source: Comprehensive logistics dataset including shipping modes, regional transit times, and department-level performance.

📊 Business Impact
By utilizing this dashboard, logistics managers can:

Optimize Shipping Tiers: Transition underperforming "Standard Class" contracts to more efficient carriers.

Calibrate Promises: Adjust SLA expectations from 4 days to 6 days to align with real-world transit data.

Protect Revenue: Prioritize high-value B2B segments to avoid contract penalties.

📂 File Structure:
├── apl_app.py            # Main interactive dashboard script
├── logistics_data.csv    # Global shipment dataset
├── requirements.txt      # Environment dependencies
├── Instructions.pdf      # Project guidelines and constraints
└── README.md             # Technical documentation

⚙️ Setup Instructions
Clone the Repo: git clone https://github.com/minniepark-me/APL-Logistics-Risk-Analysis.git

Install Requirements: pip install -r requirements.txt

Launch Dashboard: streamlit run apl_app.py
