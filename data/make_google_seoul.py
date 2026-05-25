"""
구글 트렌드 서울 TOP 50 데이터 수집 스크립트
실행 전: pip install pytrends openpyxl pandas
실행 방법: python make_google_seoul.py
"""

import time
import pandas as pd
from pytrends.request import TrendReq

# ── 서울 TOP 50 장소 목록 ─────────────────────────────────────────────────────
PLACES = [
    ("서대문형무소역사관", "Seodaemun Prison History Hall"),
    ("서순라길",           "Seosulla-gil"),
    ("길상사(서울)",       "Gilsangsa Temple Seoul"),
    ("북촌한옥마을",       "Bukchon Hanok Village"),
    ("남산서울타워",       "N Seoul Tower"),
    ("국립중앙박물관",     "National Museum of Korea"),
    ("레일크루즈 해랑열차","Rail Cruise Haerang Train"),
    ("국립대한민국임시정부기념관", "National Memorial Korean Provisional Government"),
    ("서울 연산군묘",      "Yeonsangun Royal Tomb Seoul"),
    ("서울숲",             "Seoul Forest"),
    ("의열사(용산)",       "Uiyeolsa Shrine Yongsan"),
    ("하이커 그라운드",    "HiKR Ground"),
    ("경복궁",             "Gyeongbokgung Palace"),
    ("서울 경교장",        "Gyeonggyojang House"),
    ("종로3가 포장마차 거리", "Jongno 3-ga Pocha Street"),
    ("서해금빛열차",       "Seohae Geumbit Train"),
    ("창경궁",             "Changgyeonggung Palace"),
    ("덕수궁",             "Deoksugung Palace"),
    ("탑골공원",           "Tapgol Park"),
    ("스위트파크 롯데 어린이 식품체험관", "Sweet Park Lotte Children Food Experience"),
    ("동대문역사문화공원", "Dongdaemun History Culture Park"),
    ("명동",               "Myeongdong"),
    ("딜쿠샤",             "Dilkusha"),
    ("3.1독립선언기념탑",  "March 1st Independence Movement Memorial Tower"),
    ("롯데월드타워 서울스카이", "Lotte World Tower Seoul Sky"),
    ("하늘공원",           "Haneul Park"),
    ("도선사(서울)",       "Doseonsa Temple Seoul"),
    ("그라운드시소 서촌",  "Ground Seesaw Seochon"),
    ("창덕궁과 후원",      "Changdeokgung Palace Huwon"),
    ("서울 한양도성 순성길", "Seoul City Wall Trail"),
    ("대원군별장(석파정)", "Daewongun Villa Seokpajeong"),
    ("서울공예박물관",     "Seoul Museum of Craft Art"),
    ("한강",               "Hangang River"),
    ("양재꽃시장",         "Yangjae Flower Market"),
    ("익선동 한옥거리",    "Ikseon-dong Hanok Street"),
    ("간송미술관(서울 보화각)", "Kansong Art Museum Seoul"),
    ("홍제폭포",           "Hongje Falls"),
    ("서울식물원",         "Seoul Botanic Park"),
    ("문래창작촌",         "Mullae Art Village"),
    ("푸른수목원",         "Pureun Arboretum"),
    ("낙산공원",           "Naksan Park"),
    ("T1 HQ SHOP",         "T1 HQ SHOP"),
    ("홍대",               "Hongdae"),
    ("롯데월드 어드벤처",  "Lotte World Adventure"),
    ("반포대교 달빛무지개분수", "Banpo Bridge Moonlight Rainbow Fountain"),
    ("충무공 이순신 동상",  "Statue of Admiral Yi Sun-sin"),
    ("성수동 카페거리",    "Seongsu-dong Cafe Street"),
    ("청계천",             "Cheonggyecheon Stream"),
    ("경희궁",             "Gyeonghuigung Palace"),
    ("북한산 백운대(우이동)", "Baegundae Peak Bukhansan"),
]

def get_trend_score(pytrends, keyword, retries=3):
    """
    단일 키워드의 최근 12개월 평균 트렌드 점수 반환
    실패 시 0 반환
    """
    for attempt in range(retries):
        try:
            pytrends.build_payload(
                [keyword],
                cat=0,
                timeframe="today 12-m",  # 최근 12개월
                geo="KR",               # 한국 기준
                gprop=""
            )
            df = pytrends.interest_over_time()
            if df.empty:
                return 0.0
            score = round(float(df[keyword].mean()), 2)
            return score
        except Exception as e:
            print(f"  ⚠️  {keyword} 시도 {attempt+1} 실패: {e}")
            time.sleep(10 * (attempt + 1))
    return 0.0


def main():
    pytrends = TrendReq(hl="ko-KR", tz=540, timeout=(10, 30), retries=3, backoff_factor=0.5)

    results = []
    total = len(PLACES)

    for i, (place_kr, place_en) in enumerate(PLACES, 1):
        print(f"[{i:02d}/{total}] {place_kr} ({place_en}) 수집 중...")

        # 한국어 키워드로 먼저 시도
        score = get_trend_score(pytrends, place_kr)

        # 0이면 영어로 재시도
        if score == 0.0:
            print(f"  → 한국어 점수 0, 영어로 재시도...")
            score = get_trend_score(pytrends, place_en)

        print(f"  → score: {score}")
        results.append({"place_kr": place_kr, "google_trend_score": score})

        # API 제한 방지: 요청 사이 간격
        time.sleep(3)

    # 점수 높은 순 정렬
    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values("google_trend_score", ascending=False).reset_index(drop=True)

    # 저장
    output_path = "google_seoul.xlsx"
    df_result.to_excel(output_path, index=False)
    print(f"\n✅ 완료! {output_path} 저장됨")
    print(df_result.head(10))


if __name__ == "__main__":
    main()
