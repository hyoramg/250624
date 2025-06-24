import streamlit as st
import pandas as pd

st.title("서울특별시 구별 고령화 지수 분석")

# 기본 파일 이름
DEFAULT_FILE = "202505_202505_연령별인구현황_월간.csv"

# 파일 업로드 or 기본 사용
uploaded_file = st.file_uploader("CSV 파일 업로드 (EUC-KR)", type="csv")
file_to_use = uploaded_file if uploaded_file is not None else DEFAULT_FILE

try:
    # 파일 읽기
    df = pd.read_csv(file_to_use, encoding="euc-kr")

    # 열 이름 정리
    df.columns = [col.replace("2025년05월_계_", "") if "2025년05월_계_" in col else col for col in df.columns]
    df = df.rename(columns={"2025년05월_계_총인구수": "총인구수"}) if "2025년05월_계_총인구수" in df.columns else df

    # 서울특별시 구만 추출
    df["구"] = df["행정구역"].str.extract(r"(서울특별시\s+\S+구)")
    df = df[df["구"].notnull()].copy()

    # 연령 열 추출
    age_0_14_cols = [f"{i}세" for i in range(0, 15)]
    age_65_up_cols = [f"{i}세" for i in range(65, 100)] + ["100세 이상"]
    all_age_cols = age_0_14_cols + age_65_up_cols
    df[all_age_cols] = df[all_age_cols].apply(pd.to_numeric, errors="coerce")

    # 구별 합계
    grouped = df.groupby("구")[all_age_cols].sum()
    age_0_14 = grouped[age_0_14_cols].sum(axis=1)
    age_65_up = grouped[age_65_up_cols].sum(axis=1)

    # 고령화 지수 계산
    aging_index = (age_65_up / age_0_14 * 100).round(2)
    aging_index_sorted = aging_index.sort_values(ascending=False)

    # 결과 출력
    st.subheader("서울시 구별 고령화 지수 (단위: %)")
    st.dataframe(aging_index_sorted)

    st.subheader("고령화 지수 시각화")
    st.bar_chart(aging_index_sorted)

except Exception as e:
    st.error(f"파일을 불러오는 데 실패했습니다: {e}")
