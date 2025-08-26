import sys, os, base64
from io import BytesIO
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from scraper.api_scraper import APIScraper
from processors.filter import LeadFilter
from processors.tagger import LeadTagger
from processors.scorer import LeadScorer

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Caprae Lead Scraper Advanced", layout="wide", page_icon="💼")
CAPRAE_PRIMARY = "#1B3A57"
CAPRAE_SECONDARY = "#4A90E2"

st.markdown(f"<h1 style='color:{CAPRAE_PRIMARY}'>💼 Caprae Lead Scraper Advanced Demo</h1>", unsafe_allow_html=True)

# ----------------------------
# Fetch & process leads
# ----------------------------
scraper = APIScraper()
leads = scraper.fetch(results=200)
lead_filter = LeadFilter()
leads = lead_filter.deduplicate(leads)

scorer = LeadScorer(target_cities=["Jakarta"], target_industries=["Tech"])
leads = scorer.apply(leads)
tagger = LeadTagger()
leads = tagger.tag_industry(leads)
leads = tagger.add_tag_high_potential(leads)

df = pd.DataFrame([lead.to_dict() for lead in leads])

# ----------------------------
# Sidebar filters
# ----------------------------
cities = ["All"] + sorted(df["location"].unique())
industries = ["All"] + sorted(df["industry"].unique())
selected_city = st.sidebar.selectbox("Filter by City", cities)
selected_industry = st.sidebar.selectbox("Filter by Industry", industries)

filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_city]
if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["industry"] == selected_industry]

# Sort High Potential on top
filtered_df["high_potential_flag"] = filtered_df["tags"].apply(lambda x: "High Potential" in x)
filtered_df = filtered_df.sort_values(by=["high_potential_flag", "score"], ascending=[False, False])

# Reset index + No column
filtered_df_display = filtered_df.reset_index(drop=True)
if "No" not in filtered_df_display.columns:
    filtered_df_display.insert(0, "No", range(1, len(filtered_df_display)+1))

# ----------------------------
# Render badges with top 10 highlight and missing info
# ----------------------------
def render_badges(row):
    badges = []
    # Missing info check
    if not row["industry"]:
        badges.append("<span style='color:red; font-weight:bold;'>⚠️ Missing info</span>")
    else:
        if "High Potential" in row["tags"]:
            if row["No"] <= 10:
                # Highlight top 10
                badges.append(
                    f"<span title='High Potential: Top lead!' style='background-color:#FF4500; color:white; padding:2px 5px; border-radius:5px; cursor: help;'>🔥 High Potential</span>"
                )
            else:
                badges.append(
                    f"<span title='High Potential: Lead has high chance' style='background-color:#FF6B6B; color:white; padding:2px 5px; border-radius:5px; cursor: help;'>🔥 High Potential</span>"
                )
        badges.append(
            f"<span title='Industry' style='background-color:{CAPRAE_SECONDARY}; color:white; padding:2px 5px; border-radius:5px; cursor: help;'>{row['industry']}</span>"
        )
    return " ".join(badges)

filtered_df_display["Tags / Industry"] = filtered_df_display.apply(render_badges, axis=1)

# ----------------------------
# Download functions
# ----------------------------
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Leads')
    return output.getvalue()

csv_data = convert_df_to_csv(filtered_df_display)
excel_data = convert_df_to_excel(filtered_df_display)

# ----------------------------
# Metrics cards
# ----------------------------
total_leads = len(filtered_df)
jakarta_count = len(filtered_df[filtered_df["location"]=="Jakarta"])
tech_count = len(filtered_df[filtered_df["industry"]=="Tech"])
avg_score = filtered_df["score"].mean() if total_leads > 0 else 0

card_style = f"""
<div style='padding:20px; margin:5px; border-radius:10px; 
            background-color:white; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); 
            text-align:center'>
    {{content}}
</div>
"""

cols = st.columns(4)
cols[0].markdown(card_style.format(content=f"<h3 style='color:{CAPRAE_PRIMARY}'>{total_leads}</h3><p>Total Leads</p>"), unsafe_allow_html=True)
cols[1].markdown(card_style.format(content=f"<h3 style='color:{CAPRAE_SECONDARY}'>{jakarta_count}</h3><p>Leads from Jakarta</p>"), unsafe_allow_html=True)
cols[2].markdown(card_style.format(content=f"<h3 style='color:{CAPRAE_SECONDARY}'>{tech_count}</h3><p>Tech Industry Leads</p>"), unsafe_allow_html=True)
cols[3].markdown(card_style.format(content=f"<h3 style='color:{CAPRAE_PRIMARY}'>{avg_score:.1f}</h3><p>Average Score</p>"), unsafe_allow_html=True)

# ----------------------------
# Pagination
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1
PAGE_SIZE = 20
total_pages = math.ceil(len(filtered_df_display) / PAGE_SIZE)

# ----------------------------
# CRM Sender
# ----------------------------
class CRMSender:
    def __init__(self, dataframe):
        self.df = dataframe

    def get_visible_high_potential_leads(self, page=1, page_size=20):
        start = (page - 1) * page_size
        end = start + page_size
        page_df = self.df.iloc[start:end]
        return page_df[page_df['tags'].apply(lambda x: "High Potential" in x)]

    def send_to_crm(self, page=1, page_size=20):
        leads_to_send = self.get_visible_high_potential_leads(page, page_size)
        num_leads = len(leads_to_send)
        leads_to_send = leads_to_send.copy()
        leads_to_send['CRM Status'] = 'Sent'
        return num_leads, leads_to_send

crm_sender = CRMSender(filtered_df_display)

# ----------------------------
# Display table with top 10 highlight
# ----------------------------
start_idx = (st.session_state.page - 1) * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
page_df = filtered_df_display.iloc[start_idx:end_idx]

def render_score_tooltip(row):
    return f"<span title='Score 0–100, higher = better' style='cursor: help;'>{row}</span>"

page_df["score"] = page_df["score"].apply(render_score_tooltip)

st.markdown(f"### Showing leads {start_idx+1} to {min(end_idx, len(filtered_df_display))} of {len(filtered_df_display)}")
st.markdown(
    page_df.to_html(
        escape=False,
        columns=["No","name","email","company","position","location","score","Tags / Industry"],
        index=False,
        table_id="leads_table"
    ),
    unsafe_allow_html=True
)

st.markdown("""
<style>
#leads_table tr:hover {background-color:#f0f8ff;}
#leads_table th, #leads_table td {padding:8px;}
#leads_table td:nth-child(8) {min-width:180px;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Pagination buttons + jump
# ----------------------------
cols = st.columns([1,2,2,2,1])
with cols[0]:
    if st.button("Previous"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
with cols[1]:
    st.markdown(f"Page {st.session_state.page} of {total_pages}")
with cols[2]:
    page_input = st.number_input("Jump to page", min_value=1, max_value=total_pages, value=st.session_state.page, step=1)
    if page_input != st.session_state.page:
        st.session_state.page = page_input
with cols[3]:
    if st.button("Next"):
        if st.session_state.page < total_pages:
            st.session_state.page += 1

# ----------------------------
# Send to CRM
# ----------------------------
if st.button("🔗 Send High Potential Leads to CRM (Simulated)"):
    num_sent, sent_df = crm_sender.send_to_crm(st.session_state.page, PAGE_SIZE)
    st.success(f"✅ {num_sent} High Potential leads sent to CRM (simulated).")
    if num_sent > 0:
        st.markdown(
            sent_df.to_html(
                escape=False,
                columns=["No","name","email","company","position","location","score","Tags / Industry"],
                index=False
            ),
            unsafe_allow_html=True
        )
    else:
        st.info("No High Potential leads on this page")

# ----------------------------
# Download buttons
# ----------------------------
csv_base64 = base64.b64encode(csv_data).decode()
excel_base64 = base64.b64encode(excel_data).decode()
st.markdown(
    f"""
    <div style='display:flex; gap:10px; margin-top:20px; margin-bottom:20px;'>
        <a href='data:file/csv;base64,{csv_base64}' download='leads.csv'>
            <button style='padding:10px 20px; border-radius:5px; background-color:{CAPRAE_SECONDARY}; color:white; border:none;'>⬇️ Download CSV</button>
        </a>
        <a href='data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}' download='leads.xlsx'>
            <button style='padding:10px 20px; border-radius:5px; background-color:{CAPRAE_SECONDARY}; color:white; border:none;'>⬇️ Download Excel</button>
        </a>
    </div>
    """, unsafe_allow_html=True
)

# ----------------------------
# Charts
# ----------------------------
st.subheader("📈 Leads Distribution by City")
fig_city = px.bar(filtered_df, x="location", y="score", color="score", text="score",
                  hover_data=["name", "company", "tags"], title="Leads by City",
                  color_continuous_scale="Blues")
st.plotly_chart(fig_city, use_container_width=True)

st.subheader("📈 Leads Distribution by Industry")
fig_industry = px.bar(filtered_df, x="industry", y="score", color="score", text="score",
                      hover_data=["name", "company", "tags"], title="Leads by Industry",
                      color_continuous_scale="Blues")
st.plotly_chart(fig_industry, use_container_width=True)

# ----------------------------
# Automated report
# ----------------------------
st.subheader("📝 Automated Report")
st.markdown(f"""
✅ Total Leads: {total_leads}  
🏙️ Leads from Jakarta: {jakarta_count} ({jakarta_count/total_leads*100:.1f}% if total>0)  
💻 Tech Industry Leads: {tech_count} ({tech_count/total_leads*100:.1f}% if total>0)  
📊 Average Score: {avg_score:.1f}
""")
