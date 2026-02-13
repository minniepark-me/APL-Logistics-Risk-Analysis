import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Global Logistics Control Tower", layout="wide")

# --- CUSTOM CSS: "DEEP NAVY COMMAND" THEME ---
st.markdown("""
<style>
    /* Main Background - DEEP OCEAN NAVY (Not Black!) */
    .stApp {
        background-color: #001529;
    }
    
    /* Font: Monospace for that "Control Tower" vibe */
    h1, h2, h3, div, p, span {
        font-family: 'Courier New', Courier, monospace !important;
        color: #E6F7FF !important; /* Soft Blue-White Text */
    }
    
    /* Metrics Box - Lighter Navy with Cyan Border */
    div[data-testid="metric-container"] {
        background-color: #002B4D; /* Lighter Navy */
        border: 1px solid #1890FF; /* Bright Cyan Border */
        padding: 10px;
        border-radius: 6px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric Values - Bright Cyan/Electric Blue */
    div[data-testid="stMetricValue"] {
        color: #40A9FF !important;
    }
    
    /* Sidebar - Very Dark Navy */
    section[data-testid="stSidebar"] {
        background-color: #000C17;
        border-right: 1px solid #002B4D;
    }
    
    /* Sidebar Text */
    .css-17lntkn, label {
        color: #40A9FF !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚓ APL LOGISTICS: OCEAN COMMAND")
st.markdown("### /// STATUS: LIVE TRACKING ACTIVE ///")

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('APL_Logistics.csv', encoding='ISO-8859-1')
    df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df['Delivery_Gap'] = df['Days_for_shipping_real'] - df['Days_for_shipment_scheduled']
    df['Delivery_Status_Label'] = np.where(df['Delivery_Gap'] > 0, 'Delayed', 'On Time')
    df['Late_Risk'] = np.where(df['Late_delivery_risk'] == 1, 'High Risk', 'Low Risk')
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("### [SYSTEM_FILTERS]")

selected_market = st.sidebar.multiselect(
    "> REGION SELECT", 
    options=df['Market'].unique(),
    default=df['Market'].unique() 
)

selected_mode = st.sidebar.multiselect(
    "> MODE SELECT",
    options=df['Shipping_Mode'].unique(),
    default=df['Shipping_Mode'].unique()
)

selected_segment = st.sidebar.multiselect(
    "> SEGMENT SELECT",
    options=df['Customer_Segment'].unique(),
    default=df['Customer_Segment'].unique()
)

filtered_df = df[
    (df['Market'].isin(selected_market)) & 
    (df['Shipping_Mode'].isin(selected_mode)) &
    (df['Customer_Segment'].isin(selected_segment))
]

# 3. KPIs ROW (With Icons)
if len(filtered_df) == 0:
    st.error("⚠️ DATA LINK SEVERED. ADJUST FILTERS.")
    st.stop()

total_orders = len(filtered_df)
delayed_orders = len(filtered_df[filtered_df['Delivery_Status_Label'] == 'Delayed'])
on_time_pct = ((total_orders - delayed_orders) / total_orders) * 100
avg_delay = filtered_df[filtered_df['Delivery_Gap'] > 0]['Delivery_Gap'].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 TOTAL_CARGO", f"{total_orders:,}")
c2.metric("⚓ ON_TIME_RATE", f"{on_time_pct:.2f}%")
c3.metric("⏳ AVG_LATENCY", f"{avg_delay:.1f} Days")
c4.metric("🚨 CRITICAL_RISK", f"{len(filtered_df[filtered_df['Late_Risk']=='High Risk']):,}")

st.divider()

# 4. PRIMARY VISUALS (Deep Navy Theme)

col_left, col_right = st.columns(2) 

with col_left:
    st.subheader("🗺️ GLOBAL_LOGISTICS_MAP")
    country_data = filtered_df.groupby('Order_Country')['Sales'].sum().reset_index()
    
    fig_map = px.choropleth(
        country_data, 
        locations='Order_Country', 
        locationmode='country names',
        color='Sales',
        title="[MAP_VIEW]: SALES_VOLUME",
        color_continuous_scale='Tealgrn', # Green/Teal looks great on Navy
        template='plotly_dark',
        labels={'Sales': 'VOLUME ($)'}
    )
    # Background set to Transparent so it shows the Navy Blue
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        margin={"r":0,"t":40,"l":0,"b":0},
        height=550 
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.subheader("🔥 BOTTLENECK_MATRIX")
    
    # LOGIC FIX: We filter for only POSITIVE delays (Real Lateness)
    # We count the VOLUME (size) of delays, not just the average.
    # This ensures Standard Class (High Volume) becomes RED.
    real_delays = filtered_df[filtered_df['Delivery_Gap'] > 0]
    
    fig_matrix = px.density_heatmap(
        real_delays, 
        x='Shipping_Mode', 
        y='Department_Name', 
        # Removing 'z' and 'histfunc' makes it count the VOLUME (Frequency)
        # Standard Class has the most volume, so it will now be DARK RED.
        title="[MATRIX_VIEW]: DELAY_VOLUME_INTENSITY",
        color_continuous_scale='Reds', # Red = High Volume of Delays
        text_auto=True,
        template='plotly_dark',
        labels={'Shipping_Mode': 'MODE', 'Department_Name': 'DEPT', 'count': 'FAILURES'}
    )
    
    fig_matrix.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        height=550
    )
    st.plotly_chart(fig_matrix, use_container_width=True)
# 5. SECONDARY VISUALS
st.divider()
c3, c4 = st.columns(2)

with c3:
    st.subheader("📉 DELIVERY_VELOCITY")
    sample_scatter = filtered_df.sample(min(1000, len(filtered_df)))
    
    fig_scatter = px.scatter(
        sample_scatter, 
        x='Days_for_shipment_scheduled', 
        y='Days_for_shipping_real', 
        color='Shipping_Mode',
        title="[SCATTER]: SCHEDULED_VS_REAL",
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={'Days_for_shipment_scheduled': 'SCHEDULED', 'Days_for_shipping_real': 'REAL', 'Shipping_Mode': 'MODE'}
    )
    fig_scatter.add_shape(type="line", x0=0, y0=0, x1=6, y1=6, line=dict(color="#FF0000", dash="dash"))
    fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with c4:
    st.subheader("📊 SEGMENT_LOAD")
    delayed_only = filtered_df[filtered_df['Delivery_Status_Label'] == 'Delayed']
    segment_delay = delayed_only['Customer_Segment'].value_counts().reset_index()
    segment_delay.columns = ['Segment', 'Delayed_Count']
    
    fig_bar = px.bar(
        segment_delay, 
        x='Segment', 
        y='Delayed_Count', 
        color='Segment', 
        title="[BAR]: DELAY_VOLUME",
        text_auto=True,
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'Segment': 'CUSTOMER_TYPE', 'Delayed_Count': 'COUNT'}
    )
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. DOWNLOAD
st.divider()
st.subheader("💾 DATA_EXPORT_LOG")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="[DOWNLOAD_CSV]",
    data=csv,
    file_name='APL_Logistics_Report.csv',
    mime='text/csv',
)
