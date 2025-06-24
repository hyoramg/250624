import streamlit as st
import pandas as pd

# 페이지 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")
st.write("총인구수 기준 상위 5개 행정구역의 연령별 인구를 시각화합니다.")

# 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="EUC-KR")

# '2025년05월_계_'로 시작하는 열만 필터링하고 연령 숫자만 추출
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

# 필요한 컬럼만 선택해서 새 데이터프레임 구성
df_cleaned = df[["행정기관", "총인구수"] + age_columns].copy()
df_cleaned.columns = ["행정기관", "총인구수"] + age_labels

# 총인구수 기준 상위 5개 행정구역 선택
top5_df = df_cleaned.sort_values(by="총인구수", ascending=False).head(5)

# 연령 컬럼만 선택해서 숫자로 변환
age_numbers = [int(age) for age in age_labels]

# 시각화 데이터 구성 및 표시
st.subheader("상위 5개 행정구역 연령별 인구 변화")

for idx, row in top5_df.iterrows():
    region = row["행정기관"]
    age_population = row[2:]  # 연령별 인구만 추출
    data = pd.DataFrame({
        "연령": age_numbers,
        "인구수": age_population.values
    }).sort_values(by="연령")
    
    st.write(f"### {region}")
    st.line_chart(data=data, x="연령", y="인구수")

# 원본 데이터 표시
st.subheader("원본 데이터 (일부)")
st.dataframe(df.head(20))
