# ============================================
# app.py
# Hidden Korea Dashboard
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import os

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Hidden Korea",
    page_icon="🌸",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

.main {
    background-color: #FFFDFB;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #FFE8E8 0%,
        #FFF6F0 100%
    );
}

.sidebar-title {
    font-size: 28px;
    font-weight: 700;
    color: #FF6B6B;
}

.big-title {
    font-size: 52px;
    font-weight: 700;
    color: #2D3436;
    margin-bottom: 10px;
}

.sub-title {
    font-size: 22px;
    color: #636E72;
    margin-bottom: 20px;
}

.description {
    font-size: 18px;
    line-height: 1.8;
    color: #555;
}

.pastel-card {
    background: white;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.rank-card {
    background: white;
    border-radius: 22px;
    padding: 16px;
    transition: 0.3s;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 14px;
}

.rank-card:hover {
    transform: translateY(-5px);
}

.flip-card {
    background-color: transparent;
    width: 100%;
    height: 320px;
    perspective: 1000px;
    margin-bottom: 25px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s;
    transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 24px;
    backface-visibility: hidden;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.flip-card-front {
    background: white;
}

.flip-card-back {
    background: linear-gradient(
        135deg,
        #FFE5EC,
        #E3F2FD
    );
    transform: rotateY(180deg);
    padding: 30px;
}

.flip-title {
    font-size: 24px;
    font-weight: 700;
}

.flip-desc {
    font-size: 17px;
    margin-top: 15px;
}

.hot-card {
    background: linear-gradient(
        135deg,
        #FFE0E9,
        #FFF3E0
    );
    padding: 20px;
    border-radius: 24px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.note {
    font-size: 14px;
    color: gray;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# LANGUAGE
# ============================================

translations = {

    "한국어": {
        "home": "홈",
        "overview": "개요",
        "korean": "한국인 관심 관광지",
        "foreign": "외국인 관심 관광지",
        "recommend": "추천 관광지",
        "title": "한국의 숨겨진 장소 추천 🌸",
        "subtitle": "뻔한 한국 관광지, 이제는 지겹지 않으신가요?",
    },

    "English": {
        "home": "Home",
        "overview": "Overview",
        "korean": "Korean Tourist Spots",
        "foreign": "Foreign Tourist Spots",
        "recommend": "Recommendations",
        "title": "Hidden Korea Recommendations 🌸",
        "subtitle": "Tired of visiting the same tourist spots in Korea?",
    },

    "Japanese": {
        "home": "ホーム",
        "overview": "概要",
        "korean": "韓国人人気観光地",
        "foreign": "外国人人気観光地",
        "recommend": "おすすめ観光地",
        "title": "韓国の隠れた名所おすすめ 🌸",
        "subtitle": "定番の韓国観光地に飽きていませんか？",
    },

    "Chinese": {
        "home": "主页",
        "overview": "概览",
        "korean": "韩国人热门景点",
        "foreign": "外国人热门景点",
        "recommend": "推荐景点",
        "title": "韩国隐藏景点推荐 🌸",
        "subtitle": "是否已经厌倦了千篇一律的韩国旅游景点？",
    }

}

# ============================================
# SIDEBAR
# ============================================

language = st.sidebar.selectbox(
    "Language",
    ["한국어", "English", "Japanese", "Chinese"]
)

t = translations[language]

menu = st.sidebar.radio(
    "MENU",
    [
        t["home"],
        t["overview"],
        t["korean"],
        t["foreign"],
        t["recommend"]
    ]
)

# ============================================
# DATA LOAD
# ============================================

@st.cache_data
def load_excel(path):
    return pd.read_excel(path)

foreign_seoul = load_excel("foreign_top 100 (Seoul)(3).xlsx")
foreign_busan = load_excel("foreign_top 100 (Busan)(3).xlsx")

korean_seoul = load_excel("korean_top 100 (Seoul)(3).xlsx")
korean_busan = load_excel("korean_top 100 (Busan)(3).xlsx")

hidden_seoul = load_excel("hidden_score_seoul(1).xlsx")
hidden_busan = load_excel("hidden_score_busan(1).xlsx")

visitor_df = load_excel("방한 외래관광객 추이(6)(1).xlsx")
travel_summary = load_excel("travel_summary_clean.xlsx")
revisit_df = load_excel("재방문율(6)(1).xlsx")

consumption_df = load_excel("관광 소비(2)(1).xlsx")

google_seoul = load_excel("seoul_google_trends_top50.xlsx")
google_busan = load_excel("busan_google_trends_top50.xlsx")

restaurant_seoul = load_excel("서울 지역맛집_한국인(2)(1).xlsx")
restaurant_busan = load_excel("부산 지역맛집_한국인(2)(1).xlsx")

# ============================================
# HOME
# ============================================

if menu == t["home"]:

    st.markdown(
        f"""
        <div class="big-title">
        {t["title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sub-title">
        {t["subtitle"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="description">
    최근 한국 재방문 관광객이 꾸준히 증가하고 있습니다.
    하지만 매번 비슷한 관광지만 방문하고 있지는 않으신가요?
    <br><br>
    이 사이트는 한국관광데이터랩 데이터를 분석하여,
    한국인과 외국인의 관심 관광지가 어떻게 다른지 비교하고,
    숨겨진 한국 여행지를 추천해드립니다 ✨
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ========================================
    # VISITOR GRAPH
    # ========================================

    st.subheader("📈 외래관광객 추이 분석")

    fig = px.line(
        visitor_df,
        x=visitor_df.columns[0],
        y=visitor_df.columns[1],
        markers=True
    )

    max_idx = visitor_df.iloc[:,1].idxmax()

    fig.add_trace(
        go.Scatter(
            x=[visitor_df.iloc[max_idx,0]],
            y=[visitor_df.iloc[max_idx,1]],
            mode='markers',
            marker=dict(
                size=16,
                color='red'
            ),
            name='Peak'
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption("※ 2023.05 ~ 2026.04 데이터 활용")

    # ========================================
    # TRAVEL SUMMARY
    # ========================================

    st.subheader("🌎 방한여행 요약")

    st.dataframe(
        travel_summary.head(10),
        use_container_width=True
    )

    st.caption("※ 2023.05 ~ 2026.04 데이터 활용")

    # ========================================
    # REVISIT
    # ========================================

    st.subheader("🔁 재방문율 분석")

    fig2 = px.line(
        revisit_df,
        x=revisit_df.columns[0],
        y=revisit_df.columns[1],
        markers=True
    )

    fig2.add_hline(
        y=50,
        line_dash="dash",
        line_color="red"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.caption("※ 2015 ~ 2024 데이터 활용")

# ============================================
# OVERVIEW
# ============================================

elif menu == t["overview"]:

    city = st.selectbox(
        "CITY",
        ["Seoul", "Busan"]
    )

    if city == "Seoul":

        st.markdown("""
        <div class="big-title">
        SEOUL ✨
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="description">
        Seoul is a city where tradition and modernity coexist beautifully.
        From historic palaces to trendy cafés,
        the city offers countless hidden gems waiting to be discovered.
        </div>
        """, unsafe_allow_html=True)

        image_dir = [
            "images/seoul1.jpg",
            "images/seoul2.jpg",
            "images/seoul3.jpg",
            "images/seoul4.jpg",
            "images/seoul5.jpg",
        ]

        korean_df = korean_seoul
        foreign_df = foreign_seoul

    else:

        st.markdown("""
        <div class="big-title">
        BUSAN 🌊
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="description">
        Busan is Korea’s vibrant coastal city,
        known for its beaches, colorful villages,
        seafood markets, and artistic atmosphere.
        </div>
        """, unsafe_allow_html=True)

        image_dir = [
            "images/busan1.jpg",
            "images/busan2.jpg",
            "images/busan3.jpg",
            "images/busan4.jpg",
            "images/busan5.jpg",
        ]

        korean_df = korean_busan
        foreign_df = foreign_busan

    carousel_items = []

    for img in image_dir:
        carousel_items.append(
            dict(
                title="",
                text="",
                img=img
            )
        )

    st.image(
        image_dir,
        use_container_width=True
    )

    st.divider()

    # ========================================
    # TOP10
    # ========================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🇰🇷 Korean TOP10")

        for i, row in korean_df.head(10).iterrows():

            st.markdown(
                f"""
                <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                <div class="rank-card">
                    <h3>#{i+1} {row['place_kr']}</h3>
                    <p>{row['category_kr']}</p>
                </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    with col2:

        st.subheader("🌍 Foreigner TOP10")

        for i, row in foreign_df.head(10).iterrows():

            st.markdown(
                f"""
                <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                <div class="rank-card">
                    <h3>#{i+1} {row['place_kr']}</h3>
                    <p>{row['category_kr']}</p>
                </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # ========================================
    # MAP
    # ========================================

    st.subheader("🗺️ Interest Map")

    korean_top10 = korean_df.head(10).copy()
    foreign_top10 = foreign_df.head(10).copy()

    korean_top10["type"] = "Korean"
    foreign_top10["type"] = "Foreigner"

    map_df = pd.concat(
        [korean_top10, foreign_top10]
    )

    def color_picker(x):
        if x == "Korean":
            return [255,0,0]
        elif x == "Foreigner":
            return [0,0,255]
        else:
            return [128,0,128]

    map_df["color"] = map_df["type"].apply(color_picker)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=120,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=37.56,
        longitude=126.97,
        zoom=10
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{place_kr}"}
    )

    st.pydeck_chart(deck)

    st.markdown("""
    🔴 Korean 관심 관광지  
    🔵 Foreigner 관심 관광지  
    🟣 비슷한 관심도 관광지
    """)

# ============================================
# KOREAN TOP50
# ============================================

elif menu == t["korean"]:

    filter_type = st.tabs([
        "TOP50",
        "SNS TOP50"
    ])

    # ========================================
    # TOP50
    # ========================================

    with filter_type[0]:

        city = st.selectbox(
            "CITY",
            ["Seoul", "Busan"]
        )

        df = korean_seoul if city == "Seoul" else korean_busan

        for i, row in df.head(50).iterrows():

            st.markdown(
                f"""
                <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                <div class="rank-card">
                    <h3>#{i+1} {row['place_kr']}</h3>
                    <p>{row['category_kr']}</p>
                </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    # ========================================
    # SNS TOP50
    # ========================================

    with filter_type[1]:

        city = st.selectbox(
            "SNS CITY",
            ["Seoul", "Busan"]
        )

        gdf = google_seoul if city == "Seoul" else google_busan

        st.subheader("🔥 Google Hot Trends")

        cols = st.columns(5)

        for idx, row in gdf.head(5).iterrows():

            with cols[idx]:

                st.markdown(
                    f"""
                    <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                    <div class="hot-card">
                        <h3>#{idx+1}</h3>
                        <p>{row['place_kr']}</p>
                        <small>{row['category_kr']}</small>
                        <br>
                        <b>Trend Score: {row['google_trend_score']}</b>
                    </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        for i, row in gdf.head(50).iterrows():

            st.markdown(
                f"""
                <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                <div class="rank-card">
                    <h3>#{i+1} {row['place_kr']}</h3>
                    <p>{row['category_kr']}</p>
                </div>
                </a>
                """,
                unsafe_allow_html=True
            )

        st.caption("※ Google Trends 데이터를 활용한 분석")

# ============================================
# FOREIGN
# ============================================

elif menu == t["foreign"]:

    tab1, tab2 = st.tabs([
        "TOP50",
        "Tourism Consumption"
    ])

    with tab1:

        city = st.selectbox(
            "CITY",
            ["Seoul", "Busan"]
        )

        df = foreign_seoul if city == "Seoul" else foreign_busan

        for i, row in df.head(50).iterrows():

            st.markdown(
                f"""
                <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                <div class="rank-card">
                    <h3>#{i+1} {row['place_kr']}</h3>
                    <p>{row['category_kr']}</p>
                </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    with tab2:

        fig = px.pie(
            consumption_df,
            names=consumption_df.columns[0],
            values=consumption_df.columns[1]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================
# RECOMMENDATION
# ============================================

elif menu == t["recommend"]:

    tab1, tab2 = st.tabs([
        "관광지 + 맛집",
        "SNS 추천"
    ])

    # ========================================
    # 관광지 + 맛집
    # ========================================

    with tab1:

        city = st.selectbox(
            "CITY",
            ["Seoul", "Busan"]
        )

        content = st.selectbox(
            "TYPE",
            ["Tour", "Restaurant"]
        )

        if city == "Seoul":

            if content == "Tour":
                df = hidden_seoul.sort_values(
                    "hidden_score",
                    ascending=False
                ).head(7)

            else:
                df = restaurant_seoul.head(7)

        else:

            if content == "Tour":
                df = hidden_busan.sort_values(
                    "hidden_score",
                    ascending=False
                ).head(7)

            else:
                df = restaurant_busan.head(7)

        cols = st.columns(3)

        for idx, row in df.iterrows():

            with cols[idx % 3]:

                st.markdown(
                    f"""
                    <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                    <div class="flip-card">
                        <div class="flip-card-inner">

                            <div class="flip-card-front">
                                <img src="{row['image_url']}"
                                style="
                                width:100%;
                                height:240px;
                                object-fit:cover;
                                ">
                                <div style="padding:15px;">
                                    <h4>{row['place_kr']}</h4>
                                </div>
                            </div>

                            <div class="flip-card-back">
                                <div class="flip-title">
                                {row['place_kr']}
                                </div>

                                <div class="flip-desc">
                                📍 {row['district_kr']}
                                <br><br>
                                🏷️ {row['category_kr']}
                                </div>
                            </div>

                        </div>
                    </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

    # ========================================
    # SNS 추천
    # ========================================

    with tab2:

        city = st.selectbox(
            "SNS CITY",
            ["Seoul", "Busan"]
        )

        if city == "Seoul":
            df = google_seoul
        else:
            df = google_busan

        category = st.selectbox(
            "CATEGORY",
            ["All"] + list(df["category_kr"].dropna().unique())
        )

        if category != "All":
            df = df[df["category_kr"] == category]

        top7 = df.sort_values(
            "google_trend_score",
            ascending=False
        ).head(7)

        cols = st.columns(3)

        for idx, row in top7.iterrows():

            with cols[idx % 3]:

                st.markdown(
                    f"""
                    <a href="{row['place_url']}" target="_blank" style="text-decoration:none;">
                    <div class="hot-card">
                        <h3>{row['place_kr']}</h3>
                        <p>{row['category_kr']}</p>
                        <b>🔥 {row['google_trend_score']}</b>
                    </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

# ============================================
# END
# ============================================