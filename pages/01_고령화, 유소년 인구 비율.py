import streamlit as st
import pandas as pd

st.title("📊 2025년 5월 연령별 인구 분석")
st.markdown("**고령화 지수 · 유소년 인구 비율 · 부양비 지수**를 분석하고 시각화합니다.")

# CSV 파일 업로드
uploaded_file = st.file_uploader("연령별 인구 CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file:
    # 데이터 불러오기 (EUC-KR 인코딩)
    df_raw = pd.read_csv(uploaded_file, encoding="EUC-KR")
    st.subheader("📄 원본 데이터 (일부)")
    st.dataframe(df_raw.head())

    # 연령별 열만 추출
    age_columns = [col for col in df_raw.columns if col.startswith("2025년05월_계_")]
    df = df_raw[["총인구수"] + age_columns].copy()

    # 열 이름 전처리 (2025년05월_계_0세 → 0)
    df.columns = ["총인구수"] + [col.replace("2025년05월_계_", "").replace("세", "").replace("이상", "") for col in age_columns]
    df.columns = ["총인구수"] + [int(c) if c.isdigit() else 100 for c in df.columns[1:]]

    # 열 이름이 숫자인 경우 정렬
    df = df.sort_index(axis=1)

    # 연령별 인구 시리즈
    age_population = df.iloc[0, 1:]  # 총인구수 제외

    # 인구 집계
    youth = age_population[age_population.index <= 14].sum()
    working = age_population[(age_population.index >= 15) & (age_population.index <= 64)].sum()
    old = age_population[age_population.index >= 65].sum()

    # 지표 계산
    aging_index = round((old / youth) * 100, 2) if youth != 0 else 0
    youth_ratio = round((youth / df["총인구수"][0]) * 100, 2)
    dependency_ratio = round(((youth + old) / working) * 100, 2) if working != 0 else 0

    st.subheader("📌 인구 구성 지표")
    st.markdown(f"- **총인구수:** {df['총인구수'][0]:,}명")
    st.markdown(f"- **유소년 인구 비율 (0~14세):** {youth_ratio}%")
    st.markdown(f"- **고령화 지수 (65세 이상 ÷ 14세 이하):** {aging_index}")
    st.markdown(f"- **부양비 지수 ((0~14세 + 65세 이상) ÷ 15~64세):** {dependency_ratio}")

    st.subheader("📈 연령별 인구 추이 (0세 ~ 100세 이상)")
    st.line_chart(age_population)
