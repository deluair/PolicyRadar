"""
PolicyRadar Streamlit Dashboard.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="PolicyRadar Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .alert-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE_URL = "http://api:8000/api/v1"


def fetch_api_data(endpoint: str, params: dict = None):
    """Fetch data from API endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return None


def generate_synthetic_data():
    """Generate synthetic data for demonstration."""
    # Generate synthetic policies
    jurisdictions = ["US", "EU", "UK", "JP", "CN", "CA", "AU", "IN", "BR", "MX"]
    industries = ["financial_services", "technology", "energy", "healthcare", "manufacturing"]
    statuses = ["DRAFT", "PROPOSED", "ENACTED", "IMPLEMENTED"]
    
    policies_data = []
    for i in range(100):
        policies_data.append({
            "id": i + 1,
            "title": f"Policy {i+1}",
            "jurisdiction": np.random.choice(jurisdictions),
            "industry": np.random.choice(industries),
            "status": np.random.choice(statuses),
            "estimated_impact": np.random.uniform(-500, 500),
            "impact_confidence": np.random.uniform(0.5, 0.9)
        })
    
    # Generate synthetic companies
    companies_data = []
    for i in range(50):
        companies_data.append({
            "id": i + 1,
            "name": f"Company {i+1}",
            "industry": np.random.choice(industries),
            "headquarters_country": np.random.choice(jurisdictions),
            "market_cap": np.random.uniform(1000, 50000),
            "revenue": np.random.uniform(500, 25000)
        })
    
    return pd.DataFrame(policies_data), pd.DataFrame(companies_data)


def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 PolicyRadar Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Overview", "Policies", "Companies", "Impact Analysis", "Predictions", "Analytics"]
    )
    
    # Date filters
    st.sidebar.title("Filters")
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=365),
        max_value=datetime.now()
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=datetime.now(),
        max_value=datetime.now()
    )
    
    jurisdiction_filter = st.sidebar.multiselect(
        "Jurisdiction",
        ["US", "EU", "UK", "JP", "CN", "CA", "AU", "IN", "BR", "MX"],
        default=["US", "EU", "UK"]
    )
    
    industry_filter = st.sidebar.multiselect(
        "Industry",
        ["financial_services", "technology", "energy", "healthcare", "manufacturing"],
        default=["financial_services", "technology"]
    )
    
    # Fetch or generate data
    try:
        dashboard_summary = fetch_api_data("/dashboard/summary")
        if dashboard_summary is None:
            # Use synthetic data if API is not available
            dashboard_summary = {
                "total_policies": 1250,
                "active_policies": 890,
                "high_risk_policies": 45,
                "total_companies": 500,
                "affected_companies": 320,
                "total_impact_assessments": 2800,
                "average_impact": -15.5,
                "prediction_accuracy": 0.82,
                "recent_alerts": [
                    {
                        "id": 1,
                        "type": "policy_change",
                        "title": "Basel III Implementation Update",
                        "severity": "high",
                        "timestamp": datetime.utcnow() - timedelta(hours=2)
                    },
                    {
                        "id": 2,
                        "type": "impact_alert",
                        "title": "Trade Tariff Impact on Manufacturing",
                        "severity": "medium",
                        "timestamp": datetime.utcnow() - timedelta(hours=6)
                    }
                ],
                "risk_distribution": {
                    "low": 45,
                    "medium": 35,
                    "high": 15,
                    "critical": 5
                }
            }
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")
        return
    
    # Page routing
    if page == "Overview":
        show_overview_page(dashboard_summary)
    elif page == "Policies":
        show_policies_page()
    elif page == "Companies":
        show_companies_page()
    elif page == "Impact Analysis":
        show_impact_analysis_page()
    elif page == "Predictions":
        show_predictions_page()
    elif page == "Analytics":
        show_analytics_page()


def show_overview_page(dashboard_summary):
    """Show overview page."""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Policies",
            value=dashboard_summary["total_policies"],
            delta=25
        )
    
    with col2:
        st.metric(
            label="Active Policies",
            value=dashboard_summary["active_policies"],
            delta=12
        )
    
    with col3:
        st.metric(
            label="High Risk Policies",
            value=dashboard_summary["high_risk_policies"],
            delta=-5,
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Prediction Accuracy",
            value=f"{dashboard_summary['prediction_accuracy']:.1%}",
            delta=0.02
        )
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution pie chart
        risk_data = dashboard_summary["risk_distribution"]
        fig_risk = px.pie(
            values=list(risk_data.values()),
            names=list(risk_data.keys()),
            title="Policy Risk Distribution",
            color_discrete_map={
                "low": "#4caf50",
                "medium": "#ff9800",
                "high": "#f44336",
                "critical": "#9c27b0"
            }
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Impact trend
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        impact_trend = np.random.normal(-15, 5, 30).cumsum()
        
        fig_impact = px.line(
            x=dates,
            y=impact_trend,
            title="Average Impact Trend (30 Days)",
            labels={"x": "Date", "y": "Impact (USD Millions)"}
        )
        fig_impact.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_impact, use_container_width=True)
    
    # Recent alerts
    st.subheader("Recent Alerts")
    for alert in dashboard_summary["recent_alerts"]:
        alert_class = f"alert-{alert['severity']}"
        st.markdown(f"""
        <div class="metric-card {alert_class}">
            <strong>{alert['title']}</strong><br>
            Type: {alert['type'].replace('_', ' ').title()}<br>
            Severity: {alert['severity'].title()}<br>
            Time: {alert['timestamp']}
        </div>
        """, unsafe_allow_html=True)


def show_policies_page():
    """Show policies page."""
    st.header("Policy Management")
    
    # Generate synthetic policies data
    policies_df, _ = generate_synthetic_data()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_jurisdiction = st.selectbox("Jurisdiction", ["All"] + list(policies_df["jurisdiction"].unique()))
    with col2:
        selected_industry = st.selectbox("Industry", ["All"] + list(policies_df["industry"].unique()))
    with col3:
        selected_status = st.selectbox("Status", ["All"] + list(policies_df["status"].unique()))
    
    # Filter data
    filtered_df = policies_df.copy()
    if selected_jurisdiction != "All":
        filtered_df = filtered_df[filtered_df["jurisdiction"] == selected_jurisdiction]
    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df["industry"] == selected_industry]
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Impact by jurisdiction
        impact_by_jurisdiction = filtered_df.groupby("jurisdiction")["estimated_impact"].mean()
        fig_jurisdiction = px.bar(
            x=impact_by_jurisdiction.index,
            y=impact_by_jurisdiction.values,
            title="Average Impact by Jurisdiction",
            labels={"x": "Jurisdiction", "y": "Average Impact (USD Millions)"}
        )
        fig_jurisdiction.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_jurisdiction, use_container_width=True)
    
    with col2:
        # Impact by industry
        impact_by_industry = filtered_df.groupby("industry")["estimated_impact"].mean()
        fig_industry = px.bar(
            x=impact_by_industry.index,
            y=impact_by_industry.values,
            title="Average Impact by Industry",
            labels={"x": "Industry", "y": "Average Impact (USD Millions)"}
        )
        fig_industry.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_industry, use_container_width=True)
    
    # Policy table
    st.subheader("Policy Details")
    st.dataframe(filtered_df, use_container_width=True)


def show_companies_page():
    """Show companies page."""
    st.header("Company Analysis")
    
    # Generate synthetic companies data
    _, companies_df = generate_synthetic_data()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Market cap distribution
        fig_market_cap = px.histogram(
            companies_df,
            x="market_cap",
            title="Market Cap Distribution",
            labels={"market_cap": "Market Cap (USD Millions)"}
        )
        st.plotly_chart(fig_market_cap, use_container_width=True)
    
    with col2:
        # Revenue by industry
        revenue_by_industry = companies_df.groupby("industry")["revenue"].mean()
        fig_revenue = px.bar(
            x=revenue_by_industry.index,
            y=revenue_by_industry.values,
            title="Average Revenue by Industry",
            labels={"x": "Industry", "y": "Average Revenue (USD Millions)"}
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Company table
    st.subheader("Company Details")
    st.dataframe(companies_df, use_container_width=True)


def show_impact_analysis_page():
    """Show impact analysis page."""
    st.header("Impact Analysis")
    
    # Generate synthetic impact data
    impact_data = []
    for i in range(100):
        impact_data.append({
            "policy_id": i + 1,
            "company_id": np.random.randint(1, 51),
            "overall_impact": np.random.uniform(-200, 200),
            "revenue_impact": np.random.uniform(-100, 100),
            "cost_impact": np.random.uniform(-50, 50),
            "risk_level": np.random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        })
    
    impact_df = pd.DataFrame(impact_data)
    
    # Impact distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig_impact_dist = px.histogram(
            impact_df,
            x="overall_impact",
            title="Impact Distribution",
            labels={"overall_impact": "Overall Impact (USD Millions)"}
        )
        fig_impact_dist.add_vline(x=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_impact_dist, use_container_width=True)
    
    with col2:
        # Risk level distribution
        risk_counts = impact_df["risk_level"].value_counts()
        fig_risk = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Level Distribution"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Impact breakdown
    st.subheader("Impact Breakdown")
    impact_breakdown = impact_df[["revenue_impact", "cost_impact"]].mean()
    fig_breakdown = px.bar(
        x=impact_breakdown.index,
        y=impact_breakdown.values,
        title="Average Impact Breakdown",
        labels={"x": "Impact Type", "y": "Average Impact (USD Millions)"}
    )
    fig_breakdown.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_breakdown, use_container_width=True)


def show_predictions_page():
    """Show predictions page."""
    st.header("Predictions & Forecasting")
    
    # Generate synthetic prediction data
    dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
    prediction_data = []
    
    for i, date in enumerate(dates):
        prediction_data.append({
            "date": date,
            "predicted_impact": np.random.uniform(-50, 50),
            "confidence": np.random.uniform(0.6, 0.95),
            "actual_impact": np.random.uniform(-50, 50) if i < 20 else None
        })
    
    pred_df = pd.DataFrame(prediction_data)
    
    # Prediction chart
    fig_pred = go.Figure()
    
    # Predicted values
    fig_pred.add_trace(go.Scatter(
        x=pred_df["date"],
        y=pred_df["predicted_impact"],
        mode="lines+markers",
        name="Predicted Impact",
        line=dict(color="blue")
    ))
    
    # Actual values (where available)
    actual_data = pred_df[pred_df["actual_impact"].notna()]
    fig_pred.add_trace(go.Scatter(
        x=actual_data["date"],
        y=actual_data["actual_impact"],
        mode="lines+markers",
        name="Actual Impact",
        line=dict(color="red")
    ))
    
    fig_pred.update_layout(
        title="Impact Predictions vs Actual",
        xaxis_title="Date",
        yaxis_title="Impact (USD Millions)"
    )
    fig_pred.add_hline(y=0, line_dash="dash", line_color="gray")
    
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Prediction accuracy
    if len(actual_data) > 0:
        accuracy = np.mean(np.abs(actual_data["predicted_impact"] - actual_data["actual_impact"]) < 10)
        st.metric("Prediction Accuracy", f"{accuracy:.1%}")


def show_analytics_page():
    """Show analytics page."""
    st.header("Advanced Analytics")
    
    # Generate synthetic analytics data
    months = pd.date_range(start=datetime.now() - timedelta(days=365), periods=12, freq='M')
    analytics_data = []
    
    for month in months:
        analytics_data.append({
            "month": month,
            "policy_count": np.random.randint(80, 120),
            "enacted_count": np.random.randint(50, 80),
            "average_impact": np.random.uniform(-20, -10),
            "high_risk_count": np.random.randint(5, 15)
        })
    
    analytics_df = pd.DataFrame(analytics_data)
    
    # Trends
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trends = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Policy Count", "Average Impact"),
            vertical_spacing=0.1
        )
        
        fig_trends.add_trace(
            go.Scatter(x=analytics_df["month"], y=analytics_df["policy_count"], name="Total Policies"),
            row=1, col=1
        )
        fig_trends.add_trace(
            go.Scatter(x=analytics_df["month"], y=analytics_df["enacted_count"], name="Enacted Policies"),
            row=1, col=1
        )
        fig_trends.add_trace(
            go.Scatter(x=analytics_df["month"], y=analytics_df["average_impact"], name="Average Impact"),
            row=2, col=1
        )
        
        fig_trends.update_layout(height=600, title_text="Policy Trends")
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        # Risk trends
        fig_risk_trend = px.line(
            analytics_df,
            x="month",
            y="high_risk_count",
            title="High Risk Policy Trend",
            labels={"high_risk_count": "High Risk Policies", "month": "Month"}
        )
        st.plotly_chart(fig_risk_trend, use_container_width=True)
    
    # Correlation analysis
    st.subheader("Correlation Analysis")
    correlation_matrix = analytics_df[["policy_count", "enacted_count", "average_impact", "high_risk_count"]].corr()
    fig_corr = px.imshow(
        correlation_matrix,
        title="Correlation Matrix",
        color_continuous_scale="RdBu"
    )
    st.plotly_chart(fig_corr, use_container_width=True)


if __name__ == "__main__":
    main() 