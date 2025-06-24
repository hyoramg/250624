import streamlit as st
import pandas as pd

st.title("👵 고령화 지수 · 👶 유소년 비율 · 💼 부양비 지수 분석")
st.markdown("2025년 5월 기준 연령별 인구 현황 데이터를 바탕으로 주요 인구 지표를 계산합니다.")

uploaded_file = st.file_uploader("CSV 파일 업로드 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file, encoding="EUC-KR")
    
    # '2025년05월_계_총인구수' → '총인구수'로 열 이름 변경
    df = df_raw.rename(columns={"2025년05월_계_총인구수": "총인구수"})

    # 연령별 열 찾기
    age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    
    # 열 이름 정제: "2025년05월_계_0세" → 0, "2025년05월_계_100세 이상" → 100
    new_age_columns = []
    for col in age_columns:
        age_str = col.replace("2025년05월_계_", "").replace("세", "").replace(" 이상", "")
        new_age_columns.append(int(age_str) if age_str.isdigit() else 100)
    
    rename_dict = dict(zip(age_columns, new_age_columns))
    df = df.rename(columns=rename_dict)

    # 필요한 열만 추출
    df = df[["총인구수"] + new_age_columns]
    df = df.sort_index(axis=1)

    # 연령별 인구 추출 (첫 번째 행 기준)
    age_population = df.iloc[0, 1:]

    # 연령대별 인구 계산
    youth = age_population[age_population.index <= 14].sum()
    working = age_population[(age_population.index >= 15) & (age_population.index <= 64)].sum()
    old = age_population[age_population.index >= 65].sum()

    # 지표 계산
    aging_index = round((old / youth) * 100, 2) if youth != 0 else None
    dependency_ratio = round(((youth + old) / working) * 100, 2) if working != 0 else None

    st.subheader("📌 인구 지표 결과")
    st.write(f"👶 **유소년 인구 (0~14세):** {youth:,}명")
    st.write(f"💼 **생산 가능 인구 (15~64세):** {working:,}명")
    st.write(f"👵 **고령 인구 (65세 이상):** {old:,}명")
    st.markdown(f"➡️ **고령화 지수:** {aging_index} (65세 이상 ÷ 14세 이하 × 100)")
    st.markdown(f"➡️ **부양비 지수:** {dependency_ratio} ((14세 이하 + 65세 이상) ÷ 15~64세 × 100)")

    st.subheader("📈 연령별 인구 시각화")
    st.line_chart(age_population)

    st.subheader("🗂️ 원본 데이터 미리보기")
    st.dataframe(df_raw.head())
