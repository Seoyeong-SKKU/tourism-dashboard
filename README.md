# 🇰🇷 Korea Hidden Spots — Tourism Dashboard

A multilingual interactive dashboard that helps repeat foreign visitors discover hidden local spots in Korea — places that locals love but rarely appear on typical tourist maps.

🔗 **Live App**: [tourism-dashboard-etbta58waijrx9xxhrr6is.streamlit.app](https://tourism-dashboard-etbta58waijrx9xxhrr6is.streamlit.app/)

-----

## 💡 Motivation

Over 50% of foreign visitors to Korea are repeat visitors — yet most follow the same itinerary every time (Myeongdong, Gwanghwamun, Seongsu, Namsan Tower). This project bridges the information gap by visualizing where locals actually go, helping repeat visitors explore Korea beyond the tourist trail.

-----

## 📊 Data Sources

- **Korea Tourism Data Lab** (한국관광데이터랩) — foreign visitor trends, nationality ratios, revisit rates, TOP 100 attractions for Korean and foreign visitors
- **Google Trends** — SNS trend scores collected via Python’s `pytrends` library
- **Custom Hidden Score Dataset** — built with Claude, scoring attractions by Korean interest vs. foreign visitor volume
- **Coverage**: 14 Excel files, 200+ locations, 2 cities (Seoul & Busan)
- **Main period**: May 2025 – April 2026 | Trend/revisit data: 2015–2026

-----

## 🗂️ Dashboard Sections

|Section            |Description                                                                                                     |
|-------------------|----------------------------------------------------------------------------------------------------------------|
|**Home**           |Foreign visitor trends, nationality breakdown (pie chart), revisit rate graph                                   |
|**Overview**       |Auto-slideshow by city, TOP 10 attractions carousel, interactive map comparing Korean vs. foreign interest spots|
|**Rankings**       |TOP 50 lists for Seoul & Busan, split by Korean/foreign interest; foreign tab includes tourism consumption data |
|**Recommendations**|Flip cards for hidden score spots, local restaurants, and SNS-trending locations (Google Trends >= 30)          |

-----

## 🌐 Supported Languages

Korean · English · 日本語 · 中文

Languages were selected based on the nationality breakdown of foreign visitors to Korea.

-----

## 🔍 Key Features

- **Hidden Score**: Ranks attractions higher when Korean interest is high but foreign visits are low
- **Interactive Map**: Blue = Korean-favored spots, Red = foreign-favored spots, Purple = shared spots
- **Flip Cards**: Hover to reveal detailed info for recommended places
- **Multilingual UI**: Full language switching across all tabs and charts

-----

## 🛠️ Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io/)
- **Data Processing**: Python, Pandas
- **Visualization**: Plotly, Folium
- **Trend Data**: pytrends (Google Trends API)
- **Deployment**: Streamlit Cloud

-----

## 🚀 Run Locally

```bash
git clone https://github.com/Seoyeong-SKKU/tourism-dashboard.git
cd tourism-dashboard
pip install -r requirements.txt
streamlit run app.py
```

-----

## 📁 Project Structure

```
tourism-dashboard/
├── app.py                  # Main Streamlit app
├── google_trends.py        # Google Trends data collection
├── requirements.txt
├── style.css
├── data/                   # Excel & CSV data files
└── .streamlit/             # Streamlit config
```

-----

## 👩‍💻 Author

**Seoyeong Kim** — Sungkyunkwan University  
Built as a data visualization course project, 2026.
