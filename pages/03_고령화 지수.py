import streamlit as st
import pandas as pd

# CSV 파일 업로드
st.title("2025년 5월 연령별 인구 현황 분석")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # EUC-KR로 읽기
    df = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 열 이름 전처리
    df = df.rename(columns=lambda x: x.replace("2025년05월_계_", "") if "2025년05월_계_" in x else x)
    df = df.rename(columns={"2025년05월_계_총인구수": "총인구수"}) if "2025년05월_계_총인구수" in df.columns else df

    # 연령 컬럼만 추출
    age_columns = [col for col in df.columns if col.isdigit()]
    df_age = df[age_columns].copy()
    df_age = df_age.apply(pd.to_numeric, errors='coerce')  # 숫자로 변환

    # 인구 집계
    age_0_14 = df_age.loc[:, '0':'14'].sum(axis=1)
    age_15_64 = df_age.loc[:, '15':'64'].sum(axis=1)
    age_65_up = df_age.loc[:, '65':].sum(axis=1)

    # 지수 계산
    aging_index = (age_65_up / age_0_14 * 100).round(2)
    dependency_ratio = ((age_0_14 + age_65_up) / age_15_64 * 100).round(2)

    # 원본 데이터 표시
    st.subheader("원본 데이터")
    st.dataframe(df)

    # 고령화 지수 시각화
    st.subheader("고령화 지수 (65세 이상 ÷ 14세 이하 × 100)")
    st.line_chart(aging_index)

    # 부양비 지수 시각화
    st.subheader("부양비 지수 ((14세 이하 + 65세 이상) ÷ 15~64세 × 100)")
    st.line_chart(dependency_ratio)

    # 지수 테이블 요약
    st.subheader("지수 요약")
    st.dataframe(pd.DataFrame({
        '고령화 지수': aging_index,
        '부양비 지수': dependency_ratio
    }))
else:
    st.warning("CSV 파일을 먼저 업로드해 주세요.")
