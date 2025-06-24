import streamlit as st

# 제목
st.title("MBTI 기반 직업 추천기")

# 설명
st.write("당신의 MBTI를 선택하면, 그에 맞는 직업을 추천해드립니다!")

# MBTI 리스트
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 사용자 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_list)

# MBTI별 직업 추천 데이터 (예시)
mbti_jobs = {
    "ISTJ": ["회계사", "공무원", "데이터 분석가"],
    "ISFJ": ["간호사", "사회복지사", "도서관 사서"],
    "INFJ": ["상담가", "작가", "인권운동가"],
    "INTJ": ["전략기획가", "과학자", "소프트웨어 엔지니어"],
    "ISTP": ["기계공", "파일럿", "응급구조사"],
    "ISFP": ["디자이너", "요리사", "플로리스트"],
    "INFP": ["시인", "심리학자", "콘텐츠 크리에이터"],
    "INTP": ["연구원", "게임 개발자", "철학자"],
    "ESTP": ["영업사원", "스턴트맨", "기업가"],
    "ESFP": ["MC", "이벤트 플래너", "배우"],
    "ENFP": ["마케터", "기획자", "방송 작가"],
    "ENTP": ["창업가", "변호사", "광고기획자"],
    "ESTJ": ["경영자", "군인", "프로젝트 매니저"],
    "ESFJ": ["교사", "호텔 매니저", "상담교사"],
    "ENFJ": ["홍보담당자", "정치가", "교육자"],
    "ENTJ": ["CEO", "경영컨설턴트", "변호사"]
}

# 추천 결과 출력
if selected_mbti:
    st.subheader(f"{selected_mbti} 유형에게 어울리는 직업 추천")
    jobs = mbti_jobs.get(selected_mbti, [])
    for job in jobs:
        st.write(f"- {job}")
