import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Korea Hidden Gems",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Image helper ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent if (BASE_DIR.parent / "data").exists() else BASE_DIR

@st.cache_data(show_spinner=False)
def get_image_base64(image_path):
    try:
        if not image_path or str(image_path) in ("", "nan"):
            return ""
        for base in [BASE_DIR, ROOT_DIR, Path.cwd()]:
            p = (base / "data" / str(image_path)) if (base / "data" / str(image_path)).exists() else (base / str(image_path))
            if p.exists():
                with open(p, "rb") as f:
                    img_data = base64.b64encode(f.read()).decode()
                ext = p.suffix.lower().lstrip(".")
                if ext in ("jpg", "JPG", "JPEG"):
                    ext = "jpeg"
                elif ext == "PNG":
                    ext = "png"
                return f"data:image/{ext};base64,{img_data}"
        return ""
    except:
        return ""

# ── Card CSS ──────────────────────────────────────────────────────────────────
CARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:20px; padding:8px 0; }
.flip-card { width:100%; height:260px; perspective:1000px; cursor:pointer; }
.flip-card-inner { position:relative; width:100%; height:100%; transition:transform 0.6s; transform-style:preserve-3d; }
.flip-card:hover .flip-card-inner { transform:rotateY(180deg); }
.flip-card-front, .flip-card-back { position:absolute; width:100%; height:100%; -webkit-backface-visibility:hidden; backface-visibility:hidden; border-radius:16px; overflow:hidden; }
.flip-card-front { background:#fff; box-shadow:0 4px 16px rgba(0,0,0,0.08); }
.flip-card-front img { width:100%; height:170px; object-fit:cover; }
.flip-card-front .card-name { padding:10px 12px; font-size:0.85rem; font-weight:600; color:#333; }
.flip-card-back { transform:rotateY(180deg); display:flex; flex-direction:column; justify-content:center; align-items:center; padding:20px; color:white; text-align:center; }
.flip-card-back .back-name { font-size:1.05rem; font-weight:700; margin-bottom:8px; }
.flip-card-back .back-district { font-size:0.78rem; opacity:0.85; margin-bottom:6px; }
.flip-card-back .back-cat { font-size:0.78rem; background:rgba(255,255,255,0.25); padding:3px 10px; border-radius:20px; margin-bottom:14px; }
.flip-card-back a { background:white; color:#d64f6e; padding:7px 18px; border-radius:20px; font-size:0.8rem; font-weight:600; text-decoration:none; }
</style>
"""

def render_cards(cards_html, height=620):
    components.html(CARD_CSS + cards_html, height=height, scrolling=True)

# ── Translations ──────────────────────────────────────────────────────────────
T = {
    "ko": {
        "lang_label": "언어 선택",
        "menu_home": "홈", "menu_overview": "개요",
        "menu_korean": "한국인 관심 관광지 TOP 50",
        "menu_foreign": "외국인 관심 관광지 TOP 50",
        "menu_recommend": "추천 관광지",
        "home_title": "한국의 숨겨진 장소 추천",
        "home_subtitle": "뻔한 한국 관광지 지겹지 않으신가요?",
        "home_desc": "방한 재방문객이 늘어나는 요즘, 매번 똑같은 장소만 방문하는 건 이제 그만! 한국관광데이터랩 데이터 분석을 통해 한국인 관심 관광지 랭킹과 외국인 관심 관광지 랭킹이 꽤 다르다는 사실을 발견했습니다.",
        "filter_visitor": "외래관광객 추이", "filter_summary": "국적별 방한 비율", "filter_revisit": "재방문율",
        "chart_visitor": "방한 외래관광객 추이", "chart_summary": "방한여행 요약 (국적별)", "chart_revisit": "재방문율 추이",
        "visitor_note": "데이터 출처: 한국관광데이터랩 (2023.05 ~ 2026.04)",
        "revisit_note": "데이터 출처: 한국관광데이터랩 (2015 ~ 2024)",
        "summary_note": "데이터 출처: 한국관광데이터랩 (2023.05 ~ 2026.04)",
        "seoul": "서울", "busan": "부산",
        "korean_interest": "한국인 관심 관광지 TOP 10",
        "foreign_interest": "외국인 관심 관광지 TOP 10",
        "korean_legend": "한국인 관심", "foreign_legend": "외국인 관심", "both_legend": "공통 관심",
        "filter_interest": "관심 관광지 TOP 50",
        "filter_foreign_interest": "관심 관광지 TOP 50", "filter_consumption": "관광소비 분석",
        "consumption_title": "외국인 관광소비 현황",
        "sns_hot": "구글 핫 트렌드 TOP 5", "google_note": "데이터 출처: Google Trends",
        "attraction": "관광지", "food": "맛집", "tab_sns": "SNS 추천",
        "all_cat": "전체", "cat_filter": "카테고리",
        "flip_hint": "카드에 마우스를 올려보세요",
        "rec_title": "카테고리별 추천 관광지", "rec_subtitle": "히든 점수 기반 TOP 70",
        "sns_rec_title": "SNS 인기 관광지 추천", "sns_rec_subtitle": "구글 트렌드 점수 기반 추천",
        "visit_btn": "방문하기",
        "overview_seoul_desc": "서울은 5천 년의 역사와 최첨단 현대 문화가 공존하는 대한민국의 수도입니다.",
        "overview_busan_desc": "부산은 대한민국 제2의 도시이자 아름다운 해안 도시입니다.",
    },
    "en": {
        "lang_label": "Language",
        "menu_home": "Home", "menu_overview": "Overview",
        "menu_korean": "Korean Top 50", "menu_foreign": "Foreigner Top 50",
        "menu_recommend": "Recommendations",
        "home_title": "Hidden Gems of Korea",
        "home_subtitle": "Tired of the same old tourist spots?",
        "home_desc": "With repeat visitors to Korea on the rise, it's time to explore beyond the usual routes! Through data analysis from Korea Tourism Data Lab, we found that what Koreans enjoy and what foreign tourists visit are surprisingly different.",
        "filter_visitor": "Visitor Trend", "filter_summary": "Nationality Breakdown", "filter_revisit": "Revisit Rate",
        "chart_visitor": "Foreign Visitor Trend", "chart_summary": "Visitor Summary by Nationality", "chart_revisit": "Revisit Rate Trend",
        "visitor_note": "Data Source: Korea Tourism Data Lab (May 2023 ~ Apr 2026)",
        "revisit_note": "Data Source: Korea Tourism Data Lab (2015 ~ 2024)",
        "summary_note": "Data Source: Korea Tourism Data Lab (May 2023 ~ Apr 2026)",
        "seoul": "Seoul", "busan": "Busan",
        "korean_interest": "Korean Interest TOP 10",
        "foreign_interest": "Foreign Interest TOP 10",
        "korean_legend": "Korean Interest", "foreign_legend": "Foreign Interest", "both_legend": "Common Interest",
        "filter_interest": "Interest TOP 50",
        "filter_foreign_interest": "Interest TOP 50", "filter_consumption": "Tourism Consumption",
        "consumption_title": "Foreign Tourist Spending",
        "sns_hot": "Google Hot Trends TOP 5", "google_note": "Data Source: Google Trends",
        "attraction": "Attraction", "food": "Restaurant", "tab_sns": "SNS Picks",
        "all_cat": "All", "cat_filter": "Category",
        "flip_hint": "Hover over a card",
        "rec_title": "Recommended by Category", "rec_subtitle": "TOP 70 based on hidden score",
        "sns_rec_title": "SNS Popular Attractions", "sns_rec_subtitle": "Based on Google Trends score",
        "visit_btn": "Visit",
        "overview_seoul_desc": "Seoul is South Korea's capital where 5,000 years of history meets cutting-edge modern culture.",
        "overview_busan_desc": "Busan is South Korea's second largest city and a stunning coastal metropolis.",
    },
    "ja": {
        "lang_label": "言語選択",
        "menu_home": "ホーム", "menu_overview": "概要",
        "menu_korean": "韓国人の注目スポット TOP 50", "menu_foreign": "外国人の注目スポット TOP 50",
        "menu_recommend": "おすすめ観光地",
        "home_title": "韓国の隠れた名所を探そう",
        "home_subtitle": "定番の観光地に飽きていませんか？",
        "home_desc": "韓国を何度も訪れる旅行者が増えている今、毎回同じ場所だけを訪れるのはもったいない！",
        "filter_visitor": "訪韓客の推移", "filter_summary": "国籍別内訳", "filter_revisit": "再訪率",
        "chart_visitor": "訪韓外国人観光客の推移", "chart_summary": "国籍別旅行者まとめ", "chart_revisit": "再訪率の推移",
        "visitor_note": "データ出典：韓国観光データラボ", "revisit_note": "データ出典：韓国観光データラボ", "summary_note": "データ出典：韓国観光データラボ",
        "seoul": "ソウル", "busan": "釜山",
        "korean_interest": "韓国人の注目スポット TOP 10", "foreign_interest": "外国人の注目スポット TOP 10",
        "korean_legend": "韓国人人気", "foreign_legend": "外国人人気", "both_legend": "共通人気",
        "filter_interest": "注目スポット TOP 50",
        "filter_foreign_interest": "注目スポット TOP 50", "filter_consumption": "観光消費分析",
        "consumption_title": "外国人観光消費状況",
        "sns_hot": "Googleホットトレンド TOP 5", "google_note": "データ出典：Google Trends",
        "attraction": "観光地", "food": "グルメ", "tab_sns": "SNSおすすめ",
        "all_cat": "すべて", "cat_filter": "カテゴリー",
        "flip_hint": "カードにマウスを乗せてみて",
        "rec_title": "カテゴリー別おすすめ観光地", "rec_subtitle": "隠れたスコア上位TOP 70",
        "sns_rec_title": "SNS人気観光地おすすめ", "sns_rec_subtitle": "Googleトレンドスコア基準",
        "visit_btn": "訪問する",
        "overview_seoul_desc": "ソウルは5000年の歴史と最先端の現代文化が共存する大韓民国の首都です。",
        "overview_busan_desc": "釜山は大韓民国第2の都市であり、美しい海岸都市です。",
    },
    "zh": {
        "lang_label": "选择语言",
        "menu_home": "首页", "menu_overview": "概览",
        "menu_korean": "韩国人热门景点 TOP 50", "menu_foreign": "外国人热门景点 TOP 50",
        "menu_recommend": "推荐景点",
        "home_title": "探索韩国隐藏宝藏",
        "home_subtitle": "厌倦了千篇一律的韩国景点？",
        "home_desc": "随着多次访韩游客不断增加，通过韩国旅游数据实验室的数据分析，我们发现韩国人和外国人的热门景点排名存在明显差异。",
        "filter_visitor": "游客趋势", "filter_summary": "国籍占比", "filter_revisit": "重游率",
        "chart_visitor": "外国游客趋势", "chart_summary": "访韩旅游国籍概览", "chart_revisit": "重游率趋势",
        "visitor_note": "数据来源：韩国旅游数据实验室", "revisit_note": "数据来源：韩国旅游数据实验室", "summary_note": "数据来源：韩国旅游数据实验室",
        "seoul": "首尔", "busan": "釜山",
        "korean_interest": "韩国人关注景点 TOP 10", "foreign_interest": "外国人关注景点 TOP 10",
        "korean_legend": "韩国人热门", "foreign_legend": "外国人热门", "both_legend": "共同热门",
        "filter_interest": "热门景点 TOP 50",
        "filter_foreign_interest": "热门景点 TOP 50", "filter_consumption": "旅游消费分析",
        "consumption_title": "外国游客消费情况",
        "sns_hot": "谷歌热搜 TOP 5", "google_note": "数据来源：Google Trends",
        "attraction": "景点", "food": "餐厅", "tab_sns": "SNS推荐",
        "all_cat": "全部", "cat_filter": "类别",
        "flip_hint": "将鼠标悬停在卡片上",
        "rec_title": "按类别推荐景点", "rec_subtitle": "基于隐藏分数的TOP 70",
        "sns_rec_title": "SNS热门景点推荐", "sns_rec_subtitle": "基于谷歌趋势分数",
        "visit_btn": "前往",
        "overview_seoul_desc": "首尔是韩国首都，5000年历史与尖端现代文化在这里和谐共存。",
        "overview_busan_desc": "釜山是韩国第二大城市，也是一座美丽的海岸城市。",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ko"
if "page" not in st.session_state:
    st.session_state.page = "home"

lang = st.session_state.lang
t = T[lang]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#fff5f5,#fff0fb); border-right:1px solid #ffe0e0; }
.sidebar-logo { text-align:center; padding:12px 0 8px; font-size:2.5rem; font-family:serif; }
.sidebar-title { text-align:center; font-weight:700; font-size:1rem; color:#d64f6e; margin-bottom:16px; }
.section-header { background:linear-gradient(90deg,#ffe8ee,#fff5fb); border-left:4px solid #d64f6e; padding:12px 16px; border-radius:0 12px 12px 0; margin:24px 0 16px; }
.section-header h3 { margin:0; color:#d64f6e; font-size:1.1rem; }
.rank-table-row { display:flex; align-items:center; padding:8px 14px; border-radius:10px; margin-bottom:6px; background:white; box-shadow:0 1px 6px rgba(0,0,0,0.05); }
.rank-table-row:hover { background:#fff5f8; }
.rank-table-num { font-weight:800; min-width:38px; font-size:1rem; color:#d64f6e; }
.rank-table-num.g { color:#FFB800; } .rank-table-num.s { color:#8E9BAD; } .rank-table-num.b { color:#C4855A; }
.rank-table-name { flex:1; font-weight:600; font-size:0.9rem; color:#222; }
.rank-table-dist { font-size:0.78rem; color:#999; margin:0 12px; min-width:72px; }
.rank-table-cat { font-size:0.73rem; padding:2px 8px; background:#fff0f3; color:#d64f6e; border-radius:10px; white-space:nowrap; }
.ov-card { background:white; border-radius:16px; box-shadow:0 4px 16px rgba(0,0,0,0.08); overflow:hidden; margin-bottom:12px; }
.ov-card-body { padding:12px 16px; }
.ov-card-rank { color:#d64f6e; font-weight:800; font-size:1rem; }
.ov-card-name { font-weight:700; font-size:1rem; margin:2px 0; }
.ov-card-cat { font-size:0.78rem; color:#888; }
.trend-card { background:white; border-radius:16px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.07); border:1.5px solid #ffe8ee; margin-bottom:8px; }
.trend-badge { display:inline-block; background:linear-gradient(90deg,#d64f6e,#f76ba3); color:white; border-radius:20px; padding:2px 10px; font-size:0.75rem; font-weight:700; margin-bottom:6px; }
.hero-banner { background:linear-gradient(135deg,#ffe8ee,#fff0fb,#e8f0ff); border-radius:24px; padding:40px 36px; margin-bottom:32px; }
.hero-title { font-size:2rem; font-weight:800; color:#d64f6e; margin-bottom:8px; }
.hero-subtitle { font-size:1rem; color:#555; margin-bottom:16px; font-weight:500; }
.hero-desc { font-size:0.88rem; color:#666; line-height:1.7; max-width:640px; }
.note-text { font-size:0.75rem; color:#aaa; margin-top:10px; font-style:italic; }
.map-legend { display:flex; gap:20px; margin:12px 0; flex-wrap:wrap; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:0.85rem; }
.legend-dot { width:12px; height:12px; border-radius:50%; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return {
        "visitor":       pd.read_excel("data/visitor.xlsx"),
        "summary":       pd.read_excel("data/summary.xlsx"),
        "revisit":       pd.read_excel("data/revisit.xlsx"),
        "korean_seoul":  pd.read_excel("data/korean_seoul.xlsx"),
        "korean_busan":  pd.read_excel("data/korean_busan.xlsx"),
        "foreign_seoul": pd.read_excel("data/foreign_seoul.xlsx"),
        "foreign_busan": pd.read_excel("data/foreign_busan.xlsx"),
        "hidden_seoul":  pd.read_excel("data/hidden_seoul.xlsx"),
        "hidden_busan":  pd.read_excel("data/hidden_busan.xlsx"),
        "food_seoul":    pd.read_excel("data/food_seoul.xlsx"),
        "food_busan":    pd.read_excel("data/food_busan.xlsx"),
        "google_seoul":  pd.read_excel("data/google_seoul.xlsx"),
        "google_busan":  pd.read_excel("data/google_busan.xlsx"),
        "consumption":   pd.read_excel("data/consumption.xlsx"),
    }

data = load_data()

# ── Helpers ───────────────────────────────────────────────────────────────────
LANG_MAP = {"ko":"kr","en":"en","ja":"jp","zh":"cn"}

def _get(row, keys):
    for k in keys:
        v = row.get(k)
        if v is not None and str(v) not in ("nan",""):
            return str(v)
    return ""

def place_name(row):
    s = LANG_MAP[lang]
    return _get(row, [f"place_{s}", "place_kr"])

def cat_name(row):
    s = LANG_MAP[lang]
    return _get(row, [f"category_{s}", "category_kr"])

def dist_name(row):
    s = LANG_MAP[lang]
    return _get(row, [f"district_{s}", "district_kr"])

def country_name(row):
    s = LANG_MAP[lang]
    return _get(row, [f"country_{s}", "country_kr"])

def food_name(row):
    s = LANG_MAP[lang]
    return _get(row, [f"name_{s}", "name_kr"])

def rank_color_t(r):
    return {1:"g",2:"s",3:"b"}.get(r,"")

PASTEL = ["#ff6b9d","#ffc5d9","#c3aed6","#8675a9","#f5a7c7","#ffd3e8","#b8e0ff","#a8d8ea","#ffeaa7","#fdcb6e"]
FOOD_CATS = {"한식","음식점","외국식","중식","일식","양식","카페","분식","해산물","식당"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">&#127472;&#127479;</div>', unsafe_allow_html=True)
    sidebar_title = {"ko":"한국의 숨겨진 장소","en":"Korea Hidden Gems","ja":"韓国の隠れた名所","zh":"韩国隐藏宝藏"}
    st.markdown(f'<div class="sidebar-title">{sidebar_title[lang]}</div>', unsafe_allow_html=True)

    lang_options = {"한국어":"ko","English":"en","日本語":"ja","中文":"zh"}
    sel_lang = st.selectbox(t["lang_label"], list(lang_options.keys()),
                            index=list(lang_options.values()).index(lang), key="lang_select")
    if lang_options[sel_lang] != lang:
        st.session_state.lang = lang_options[sel_lang]
        st.rerun()

    st.markdown("---")
    pages = [("home",t["menu_home"]),("overview",t["menu_overview"]),
             ("korean",t["menu_korean"]),("foreign",t["menu_foreign"]),("recommend",t["menu_recommend"])]
    for pk, pl in pages:
        is_active = st.session_state.page == pk
        if st.button(pl, key=f"nav_{pk}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = pk
            st.rerun()

page = st.session_state.page
t = T[lang]

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "home":
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">{t['home_title']}</div>
        <div class="hero-subtitle">{t['home_subtitle']}</div>
        <div class="hero-desc">{t['home_desc']}</div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([t["filter_visitor"], t["filter_summary"], t["filter_revisit"]])

    with tab1:
        st.markdown(f'<div class="section-header"><h3>{t["chart_visitor"]}</h3></div>', unsafe_allow_html=True)
        df_v = data["visitor"].copy()
        df_v["date"] = pd.to_datetime(df_v["date"].astype(str), format="%Y%m")
        fig = px.line(df_v, x="date", y="visitors", color_discrete_sequence=["#d64f6e"], template="plotly_white")
        fig.update_traces(mode="lines+markers", marker=dict(size=5), line=dict(width=2.5))
        fig.update_layout(hovermode="x unified", plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="note-text">{t["visitor_note"]}</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="section-header"><h3>{t["chart_summary"]}</h3></div>', unsafe_allow_html=True)
        df_s = data["summary"].copy()
        labels = [country_name(r) for _,r in df_s.iterrows()]
        fig = px.pie(df_s, values="visitors", names=labels, color_discrete_sequence=PASTEL, hole=0.35)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=True, margin=dict(t=20,b=20), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="note-text">{t["summary_note"]}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown(f'<div class="section-header"><h3>{t["chart_revisit"]}</h3></div>', unsafe_allow_html=True)
        df_r = data["revisit"].copy()
        fig = go.Figure(go.Bar(
            x=df_r["date"].astype(str), y=df_r["revisit_rate"],
            marker=dict(color=df_r["revisit_rate"], colorscale=[[0,"#ffc5d9"],[1,"#d64f6e"]], showscale=False),
            text=df_r["revisit_rate"].apply(lambda x: f"{x:.1f}%"), textposition="outside"))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=30,b=10), yaxis=dict(range=[0,90]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="note-text">{t["revisit_note"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "overview":
    city = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="ov_city", label_visibility="collapsed")
    st.markdown("---")

    if city == t["seoul"]:
        st.markdown(f"# {t['seoul']}")
        st.markdown(f"<p style='color:#666'>{t['overview_seoul_desc']}</p>", unsafe_allow_html=True)
        imgs = ["images/서울 1.jpeg","images/서울 2.jpeg","images/서울 3.jpeg","images/서울 4.jpg","images/서울 5.jpeg"]
        dot_color = "#d64f6e"
        k_df = data["korean_seoul"]; f_df = data["foreign_seoul"]
    else:
        st.markdown(f"# {t['busan']}")
        st.markdown(f"<p style='color:#666'>{t['overview_busan_desc']}</p>", unsafe_allow_html=True)
        imgs = ["images/부산 1.jpeg","images/부산 2.jpeg","images/부산 3.jpeg","images/부산 4.jpeg","images/부산 5.jpg"]
        dot_color = "#2980b9"
        k_df = data["korean_busan"]; f_df = data["foreign_busan"]

    b64s = [b for b in [get_image_base64(p) for p in imgs] if b]
    if b64s:
        img_tags = "".join([f'<img src="{b}" class="{"on" if i==0 else ""}">' for i,b in enumerate(b64s)])
        dot_tags = "".join([f'<span class="dot {"on" if i==0 else ""}" onclick="goTo({i})"></span>' for i in range(len(b64s))])
        components.html(f"""
        <style>
        .sw{{position:relative;width:100%;border-radius:16px;overflow:hidden;margin:16px 0 8px}}
        .sw img{{width:100%;height:320px;object-fit:cover;display:none}}
        .sw img.on{{display:block}}
        .dots{{text-align:center;padding:8px 0}}
        .dot{{display:inline-block;width:10px;height:10px;border-radius:50%;background:#ddd;margin:0 4px;cursor:pointer}}
        .dot.on{{background:{dot_color}}}
        </style>
        <div class="sw" id="sw">{img_tags}</div>
        <div class="dots" id="dots">{dot_tags}</div>
        <script>
        var imgs=document.querySelectorAll('#sw img'),dots=document.querySelectorAll('#dots .dot'),cur=0;
        function goTo(n){{imgs[cur].classList.remove('on');dots[cur].classList.remove('on');cur=n%imgs.length;imgs[cur].classList.add('on');dots[cur].classList.add('on');}}
        setInterval(function(){{goTo(cur+1);}},3000);
        </script>
        """, height=380)

    col1, col2 = st.columns(2)

    def render_top10(df, rank_col, label, key_prefix):
        st.markdown(f'<div class="section-header"><h3>{label}</h3></div>', unsafe_allow_html=True)
        top10 = df[df[rank_col]<=10].sort_values(rank_col).head(10)
        if f"{key_prefix}_idx" not in st.session_state:
            st.session_state[f"{key_prefix}_idx"] = 0
        idx = st.session_state[f"{key_prefix}_idx"] % len(top10)
        row = top10.iloc[idx]
        pname = place_name(row); cname = cat_name(row); dname = dist_name(row)
        url = row.get("place_url","#") or "#"
        rank = int(row[rank_col])
        img_b64 = get_image_base64(str(row.get("image","")))
        img_html = f'<img src="{img_b64}" style="width:100%;height:180px;object-fit:cover">' if img_b64 else '<div style="height:180px;background:linear-gradient(135deg,#ffe8ee,#f0e8ff);display:flex;align-items:center;justify-content:center;font-size:3rem;">&#127963;</div>'
        st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none"><div class="ov-card">{img_html}<div class="ov-card-body"><div class="ov-card-rank">#{rank}</div><div class="ov-card-name">{pname}</div><div class="ov-card-cat">{dname} · {cname}</div></div></div></a>', unsafe_allow_html=True)
        nc1,nc2,nc3 = st.columns([1,3,1])
        with nc1:
            if st.button("←", key=f"{key_prefix}_prev", use_container_width=True):
                st.session_state[f"{key_prefix}_idx"] = (idx-1) % len(top10); st.rerun()
        with nc2:
            st.markdown(f"<div style='text-align:center;color:#aaa;font-size:0.8rem;padding-top:8px'>{idx+1}/{len(top10)}</div>", unsafe_allow_html=True)
        with nc3:
            if st.button("→", key=f"{key_prefix}_next", use_container_width=True):
                st.session_state[f"{key_prefix}_idx"] = (idx+1) % len(top10); st.rerun()

    with col1: render_top10(k_df, "korean_interest_rank", t["korean_interest"], f"{city}_k")
    with col2: render_top10(f_df, "foreign_interest_rank", t["foreign_interest"], f"{city}_f")

    st.markdown("---")
    st.markdown(f'<div class="map-legend"><div class="legend-item"><div class="legend-dot" style="background:#e74c3c"></div>{t["korean_legend"]}</div><div class="legend-item"><div class="legend-dot" style="background:#2980b9"></div>{t["foreign_legend"]}</div><div class="legend-item"><div class="legend-dot" style="background:#8e44ad"></div>{t["both_legend"]}</div></div>', unsafe_allow_html=True)

    k_places = set(k_df[k_df["korean_interest_rank"]<=10]["place_kr"])
    f_places = set(f_df[f_df["foreign_interest_rank"]<=10]["place_kr"])
    map_rows = []
    for _,r in k_df[k_df["korean_interest_rank"]<=10].iterrows():
        if pd.notna(r.get("lat")) and pd.notna(r.get("lon")):
            map_rows.append({"lat":r["lat"],"lon":r["lon"],"name":place_name(r),"type":"both" if r["place_kr"] in f_places else "korean"})
    for _,r in f_df[f_df["foreign_interest_rank"]<=10].iterrows():
        if pd.notna(r.get("lat")) and pd.notna(r.get("lon")) and r["place_kr"] not in k_places:
            map_rows.append({"lat":r["lat"],"lon":r["lon"],"name":place_name(r),"type":"foreign"})
    if map_rows:
        map_df = pd.DataFrame(map_rows)
        fig_map = px.scatter_mapbox(map_df,lat="lat",lon="lon",hover_name="name",color="type",
            color_discrete_map={"korean":"#e74c3c","foreign":"#2980b9","both":"#8e44ad"},
            zoom=11,height=420,mapbox_style="carto-positron")
        fig_map.update_traces(marker=dict(size=14))
        fig_map.update_layout(margin=dict(t=0,b=0),showlegend=False)
        st.plotly_chart(fig_map, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# KOREAN TOP 50
# ══════════════════════════════════════════════════════════════════════════════
elif page == "korean":
    st.markdown(f"# {t['menu_korean']}")
    city_k = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="korean_city", label_visibility="collapsed")
    df = data["korean_seoul"] if city_k==t["seoul"] else data["korean_busan"]
    top50 = df[df["korean_interest_rank"]<=50].sort_values("korean_interest_rank").head(50)
    for _,row in top50.iterrows():
        rank = int(row["korean_interest_rank"])
        pname = place_name(row); cname = cat_name(row); dname = dist_name(row)
        url = row.get("place_url","")
        rc = rank_color_t(rank)
        name_html = f'<a href="{url}" target="_blank" style="color:#222;text-decoration:none">{pname}</a>' if url else pname
        st.markdown(f'<div class="rank-table-row"><div class="rank-table-num {rc}">#{rank}</div><div class="rank-table-name">{name_html}</div><div class="rank-table-dist">{dname}</div><div class="rank-table-cat">{cname}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOREIGN TOP 50
# ══════════════════════════════════════════════════════════════════════════════
elif page == "foreign":
    st.markdown(f"# {t['menu_foreign']}")
    ftab1, ftab2 = st.tabs([t["filter_foreign_interest"], t["filter_consumption"]])

    with ftab1:
        city_f = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="foreign_city", label_visibility="collapsed")
        df = data["foreign_seoul"] if city_f==t["seoul"] else data["foreign_busan"]
        top50 = df[df["foreign_interest_rank"]<=50].sort_values("foreign_interest_rank").head(50)
        for _,row in top50.iterrows():
            rank = int(row["foreign_interest_rank"])
            pname = place_name(row); cname = cat_name(row); dname = dist_name(row)
            url = row.get("place_url","")
            rc = rank_color_t(rank)
            name_html = f'<a href="{url}" target="_blank" style="color:#222;text-decoration:none">{pname}</a>' if url else pname
            st.markdown(f'<div class="rank-table-row"><div class="rank-table-num {rc}">#{rank}</div><div class="rank-table-name">{name_html}</div><div class="rank-table-dist">{dname}</div><div class="rank-table-cat">{cname}</div></div>', unsafe_allow_html=True)

    with ftab2:
        st.markdown(f'<div class="section-header"><h3>{t["consumption_title"]}</h3></div>', unsafe_allow_html=True)
        c_df = data["consumption"].copy()
        ml = f"main_category_{LANG_MAP[lang]}"
        if ml not in c_df.columns: ml = "main_category_kr"
        agg = c_df.groupby(ml)["main_ratio"].first().reset_index()
        agg.columns = ["category","ratio"]
        fig = px.pie(agg, values="ratio", names="category", color_discrete_sequence=PASTEL, hole=0.35)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=20,b=20), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
        sl = f"sub_category_{LANG_MAP[lang]}"
        if sl not in c_df.columns: sl = "sub_category_kr"
        for mc in agg["category"].tolist():
            sub = c_df[c_df[ml]==mc][[sl,"sub_ratio"]].drop_duplicates()
            if len(sub) > 1:
                with st.expander(f"{mc}"):
                    fig2 = px.bar(sub, x=sl, y="sub_ratio", color_discrete_sequence=["#d64f6e"],
                                  labels={sl:"","sub_ratio":"%"}, template="plotly_white")
                    fig2.update_layout(margin=dict(t=10,b=10))
                    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "recommend":
    st.markdown(f"# {t['menu_recommend']}")
    rtab1, rtab2, rtab3 = st.tabs([t["attraction"], t["food"], t["tab_sns"]])

    with rtab1:
        st.markdown(f"### {t['rec_title']}")
        st.markdown(f"<p style='color:#999;font-size:0.85rem'>{t['rec_subtitle']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#999;font-size:0.82rem'>{t['flip_hint']}</p>", unsafe_allow_html=True)
        city_r = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="rec_city", label_visibility="collapsed")
        h_df = data["hidden_seoul"] if city_r==t["seoul"] else data["hidden_busan"]
        h_filtered = h_df[~h_df["category_kr"].isin(FOOD_CATS)].dropna(subset=["category_kr"])
        top70 = h_filtered.sort_values("hidden_score", ascending=False).head(70)
        cats_raw = top70["category_kr"].dropna().unique().tolist()
        cat_label_map = {c: cat_name(top70[top70["category_kr"]==c].iloc[0]) for c in cats_raw}
        cat_options = [t["all_cat"]] + [cat_label_map[c] for c in cats_raw]
        cat_reverse = {v:k for k,v in cat_label_map.items()}
        sel_cat = st.selectbox(t["cat_filter"], cat_options, key="rec_cat")
        display_df = top70 if sel_cat==t["all_cat"] else top70[top70["category_kr"]==cat_reverse.get(sel_cat,sel_cat)]
        cards_html = '<div class="card-grid">'
        for _,row in display_df.iterrows():
            pname=place_name(row); cname=cat_name(row); dname=dist_name(row)
            score=int(row.get("hidden_score",0))
            url=row.get("place_url","#") or "#"
            img_b64=get_image_base64(str(row.get("image","")))
            img_html=f'<img src="{img_b64}" style="width:100%;height:170px;object-fit:cover">' if img_b64 else '<div style="height:170px;background:linear-gradient(135deg,#ffe8ee,#f0e8ff);display:flex;align-items:center;justify-content:center;font-size:2.5rem;">&#127963;</div>'
            cards_html+=f'<div class="flip-card"><div class="flip-card-inner"><div class="flip-card-front">{img_html}<div class="card-name">{pname}</div></div><div class="flip-card-back" style="background:linear-gradient(135deg,#d64f6e,#f76ba3)"><div class="back-name">{pname}</div><div class="back-district">{dname}</div><div class="back-cat">{cname}</div><div style="font-size:0.78rem;opacity:0.85;margin-bottom:10px">Hidden Score: {score}</div><a href="{url}" target="_blank">{t["visit_btn"]}</a></div></div></div>'
        cards_html+='</div>'
        render_cards(cards_html, height=2400 if sel_cat==t["all_cat"] else max(700,(len(display_df)//4+1)*320))

    with rtab2:
        st.markdown(f"### {t['food']}")
        st.markdown(f"<p style='color:#999;font-size:0.82rem'>{t['flip_hint']}</p>", unsafe_allow_html=True)
        city_f2 = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="rec_food_city", label_visibility="collapsed")
        f_df = data["food_seoul"] if city_f2==t["seoul"] else data["food_busan"]
        cats_raw = f_df["category_kr"].dropna().unique().tolist()
        cat_label_map = {c: _get(f_df[f_df["category_kr"]==c].iloc[0], [f"category_{LANG_MAP[lang]}","category_kr"]) for c in cats_raw}
        cat_options = [t["all_cat"]] + [cat_label_map[c] for c in cats_raw]
        cat_reverse = {v:k for k,v in cat_label_map.items()}
        sel_cat_f = st.selectbox(t["cat_filter"], cat_options, key="rec_food_cat")
        display_f = f_df if sel_cat_f==t["all_cat"] else f_df[f_df["category_kr"]==cat_reverse.get(sel_cat_f,sel_cat_f)]
        cards_html = '<div class="card-grid">'
        for _,row in display_f.iterrows():
            pname=food_name(row); cname=_get(row,[f"category_{LANG_MAP[lang]}","category_kr"]); dname=dist_name(row)
            url=row.get("place_url","#") or "#"
            img_b64=get_image_base64(str(row.get("image","")))
            img_html=f'<img src="{img_b64}" style="width:100%;height:170px;object-fit:cover">' if img_b64 else '<div style="height:170px;background:linear-gradient(135deg,#fff0e8,#ffe8f0);display:flex;align-items:center;justify-content:center;font-size:2.5rem;">&#127837;</div>'
            cards_html+=f'<div class="flip-card"><div class="flip-card-inner"><div class="flip-card-front">{img_html}<div class="card-name">{pname}</div></div><div class="flip-card-back" style="background:linear-gradient(135deg,#f76ba3,#ffa07a)"><div class="back-name">{pname}</div><div class="back-district">{dname}</div><div class="back-cat">{cname}</div><a href="{url}" target="_blank">{t["visit_btn"]}</a></div></div></div>'
        cards_html+='</div>'
        render_cards(cards_html, height=max(700,(len(display_f)//4+1)*320))

    with rtab3:
        st.markdown(f"### {t['sns_rec_title']}")
        st.markdown(f"<p style='color:#999;font-size:0.85rem'>{t['sns_rec_subtitle']}</p>", unsafe_allow_html=True)
        city_s = st.radio("도시", [t["seoul"],t["busan"]], horizontal=True, key="sns_city", label_visibility="collapsed")
        g_df = data["google_seoul"] if city_s==t["seoul"] else data["google_busan"]
        g_df = g_df[g_df["google_trend_score"]>=30].sort_values("google_trend_score",ascending=False).reset_index(drop=True)
        st.markdown(f'<div class="section-header"><h3>{t["sns_hot"]}</h3></div>', unsafe_allow_html=True)
        top5 = g_df.head(5)
        if len(top5) > 0:
            hot_cols = st.columns(min(len(top5),5))
            for i,(_,row) in enumerate(top5.iterrows()):
                pname=place_name(row); cname=cat_name(row)
                score=row.get("google_trend_score",0)
                url=row.get("place_url","") or f"https://www.google.com/search?q={pname}"
                with hot_cols[i]:
                    st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none"><div class="trend-card"><div class="trend-badge">#{i+1}</div><div style="font-weight:700;font-size:0.95rem;margin:4px 0">{pname}</div><div style="font-size:0.78rem;color:#888">{cname}</div><div style="font-size:0.82rem;color:#d64f6e;font-weight:600;margin-top:6px">score: {score}</div></div></a>', unsafe_allow_html=True)
        st.markdown("---")
        cats_raw = g_df["category_kr"].dropna().unique().tolist()
        cat_label_map = {c: cat_name(g_df[g_df["category_kr"]==c].iloc[0]) for c in cats_raw}
        cat_options = [t["all_cat"]] + [cat_label_map[c] for c in cats_raw]
        cat_reverse = {v:k for k,v in cat_label_map.items()}
        sel_cat_s = st.selectbox(t["cat_filter"], cat_options, key="sns_cat")
        filtered_s = g_df if sel_cat_s==t["all_cat"] else g_df[g_df["category_kr"]==cat_reverse.get(sel_cat_s,sel_cat_s)]
        st.markdown(f"<p style='color:#999;font-size:0.82rem'>{t['flip_hint']}</p>", unsafe_allow_html=True)
        cards_html = '<div class="card-grid">'
        for _,row in filtered_s.iterrows():
            pname=place_name(row); cname=cat_name(row); dname=dist_name(row)
            score=row.get("google_trend_score",0)
            url=row.get("place_url","") or f"https://www.google.com/search?q={pname}"
            img_b64=get_image_base64(str(row.get("image","")))
            img_html=f'<img src="{img_b64}" style="width:100%;height:170px;object-fit:cover">' if img_b64 else '<div style="height:170px;background:linear-gradient(135deg,#e8f4ff,#f0e8ff);display:flex;align-items:center;justify-content:center;font-size:2.5rem;">&#128241;</div>'
            cards_html+=f'<div class="flip-card"><div class="flip-card-inner"><div class="flip-card-front" style="background:#fff">{img_html}<div class="card-name">{pname}</div></div><div class="flip-card-back" style="background:linear-gradient(135deg,#6c5ce7,#a29bfe)"><div class="back-name">{pname}</div><div class="back-district">{dname}</div><div class="back-cat">{cname}</div><div style="font-size:0.82rem;margin-bottom:10px;opacity:0.9">Trend: {score}</div><a href="{url}" target="_blank">{t["visit_btn"]}</a></div></div></div>'
        cards_html+='</div>'
        render_cards(cards_html, height=max(700,(len(filtered_s)//4+1)*320))
        st.markdown(f'<div class="note-text">{t["google_note"]}</div>', unsafe_allow_html=True)
