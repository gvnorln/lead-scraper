# 💼 Caprae Lead Scraper - Developer Intern Pre-Work

**Developer Intern Interview Pre-Work**  
*Private & Confidential*  

**Prepared by:** Gio  

---

## 📌 Note from the Founder

> Caprae Capital looks for candidates with **character, courage, creativity**, and a burning desire to master their craft. This pre-work assesses your **AI-readiness, problem-solving, and business impact thinking** beyond academic pedigree or prior experience.  

---

## 🧠 Project Overview

**Project:** Lead Scraper & Scoring Tool  
**Goal:** Enhance lead generation process by providing **actionable insights** for sales teams using **filtering, scoring, tagging, and visual analytics**.  

**Key Features Implemented:**
- Fetch leads via API, fallback to cached data if API fails  
- Deduplication & lead scoring based on target cities and industries  
- Tagging High Potential leads  
- Filter by **City** / **Industry**  
- Paginated table display with badges for tags/industry  
- Download filtered leads as CSV or Excel  
- Interactive visualizations using Plotly  
- Automated summary report of key metrics  

**Future Enhancements (Planned):**
- Prioritization & sorting of high-impact leads  
- Smart workflow & simulated CRM integration  
- Advanced enrichment (company size, detailed industry classification, missing info flags)  
- UX/UI improvements: hover effects, tooltips, responsive layout  
- Async fetching & email/company validation for scalability  

---

## 1. Development Challenge Overview

**Reference Tool:** [SaaSquatch Leads](https://www.saasquatchleads.com/)  

**Challenge Approach:**
- Focused on improving **business impact** in 5 hours  
- Implemented **quality-first features**: lead scoring, tagging, and actionable visual insights  
- Enhanced **UX/UI** for better readability and navigation  

**Rationale:**  
The added features allow sales teams to quickly identify high-potential leads, understand industry distribution, and export actionable data — aligning with Caprae’s business goals.

---

## 2. Submission Requirement

- **GitHub Repository:** Contains full Streamlit app code and README  
- **Video Walkthrough:** 1–2 minutes explaining project, value, and decisions  
- **Demo Link (optional):** Streamlit app walkthrough

---

## 3. Evaluation Criteria Mapping

| Category | Status in Project | Notes / Planned Improvements |
|----------|-----------------|-----------------------------|
| **Business Use Case Understanding** | ✅ Leads scoring, high potential tagging | Add priority sorting, CRM integration simulation |
| **UX/UI** | ✅ Cards, badges, charts, sidebar filters | Add hover effects, tooltips, responsive table layout |
| **Technicality** | ✅ Deduplication, scoring, tagging, API fetch | Add async fetching, validation, cached fallback, unit tests |
| **Design** | ✅ Color theme, cards, badges, charts | Branding, polished spacing, mobile-friendly |
| **Creativity** | ✅ Automated report, download buttons | Smart filtering, scenario-based ranking, CRM workflow simulation |

---

## 4. Business Understanding

**Caprae’s Mission:**  
Caprae Capital leverages **AI and data-driven insights** to help companies unlock growth and efficiency post-acquisition. The focus is on real-world value creation beyond financial engineering.

**How Caprae is Changing the ETA/PE Space:**  
Unlike traditional PE firms, Caprae implements **AI-powered tools and SaaS/MaaS models** to improve decision-making, identify high-value leads, and streamline operations post-acquisition, turning good businesses into great ones.

---

## 5. Optional Reapplicant Questions

> These are answered if applicable; can also be used to demonstrate thinking.

**1. What do you think is Caprae’s unfair advantage?**  
Caprae’s unfair advantage is its **founder/operator-first approach** combined with AI-driven decision-making. By focusing on post-acquisition growth and leveraging data intelligence, Caprae can extract higher value than traditional PE players.

**2. What does “To become a legend, you must take down legends” mean to you?**  
It signifies the importance of **challenging the status quo**, learning from the best, and pushing oneself to outperform existing industry leaders by innovation, strategy, and execution.

**3. What do you think Caprae’s culture will be like?**  
A **high-performance, curiosity-driven, and founder/operator mindset culture**, valuing creativity, independent thinking, and hands-on problem solving, while rewarding initiative and impact.

---

## 6. Setup & Installation

```bash
# Clone repository
git clone https://github.com/username/lead-scraper.git
cd lead-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run ui/streamlit_app.py

## 7. Demo & Video Link

- **Video Walkthrough (1–2 min):** [YouTube/Drive link](https://youtu.be/your-video-link)  
- **Live Demo (Streamlit App):** [Click here to try the app](https://share.streamlit.io/username/lead-scraper/main/ui/streamlit_app.py)
