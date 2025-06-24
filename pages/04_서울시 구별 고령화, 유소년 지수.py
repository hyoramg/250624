import streamlit as st
import pandas as pd

st.title("서울특별시 구별 고령화 및 부양비 지수 분석")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 열 이름 전처리
    df = df.rename(columns=lambda x: x.replace("2025년05월_계_", "") if "2025년05월_계_" in x else x)
    df = df.rename(columns={"2025년05월_계_총인구수": "총인구수"}) if "2025년05월_계_총인구수" in df.columns else df

    # 행정구역에서 구 이름 추출
    df["구"] = df["행정구역"].str.extract(r"(서울특별시\s+\S+구)")

    # 서울특별시가 아닌 경우 제거
    df = df[df["구"].notnull()].copy()

    # 연령 컬럼만 추출
    age_columns = [col for col in df.columns if col.isdigit()]
    df[age_columns] = df[age_columns].apply(pd.to_numeric, errors='coerce')

    # 구 단위로 합계 계산
    grouped = df.groupby("구")[age_columns].sum()

    # 지수 계산
    age_0_14 = grouped.loc[:, '0':'14'].sum(axis=1)
    age_15_64 = grouped.loc[:, '15':'64'].sum(axis=1)
    age_65_up = grouped.loc[:, '65':].sum(axis=1)

    aging_index = (age_65_up / age_0_14 * 100).round(2)
    dependency_ratio = ((age_0_14 + age_65_up) / age_15_64 * 100).round(2)

    # 결과 데이터프레임 생성
    result_df = pd.DataFrame({
        "고령화 지수": aging_index,
        "부양비 지수": dependency_ratio
    })

    # 데이터 출력
    st.subheader("구별 고령화 지수 및 부양비 지수")
    st.dataframe(result_df)

    # 시각화: 고령화 지수
    st.subheader("구별 고령화 지수 (낮을수록 젊음)")
    st.bar_chart(result_df["고령화 지수"])

    # 시각화: 부양비 지수
    st.subheader("구별 부양비 지수 (높을수록 부담 큼)")
    st.bar_chart(result_df["부양비 지수"])
else:
    st.warning("CSV 파일을 먼저 업로드해 주세요.")
