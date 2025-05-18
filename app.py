import streamlit as st
from questions import questions
from report import generate_pdf_report

# 페이지 기본 설정
st.set_page_config(page_title="도박 중독 자가진단", layout="centered")

# 앱 제목
st.title("도박 중독 자가진단 테스트 (DSM-5 기준)")

# 사용자 정보 입력
user_name = st.text_input("이름 또는 닉네임을 입력하세요:")
answers = []

# 설문 폼
with st.form("gambling_test"):
    for i, q in enumerate(questions):
        score = st.radio(q, [0, 1, 2], key=f"q{i}", horizontal=True,
                         help="0: 전혀 아니다 / 1: 가끔 그렇다 / 2: 자주 그렇다")
        answers.append(score)
    submitted = st.form_submit_button("제출")

# 결과 처리
if submitted:
    total_score = sum(answers)

    # DSM-5 기반 해석
    if total_score < 4:
        result = "도박 장애 없음"
    elif total_score <= 5:
        result = "경증 도박 장애"
    elif total_score <= 7:
        result = "중등도 도박 장애"
    else:
        result = "중증 도박 장애"

    # 결과 출력
    st.subheader(f"총 점수: {total_score}점")
    st.success(f"진단 결과: {result}")

    # PDF 리포트 생성 및 다운로드
    pdf_file = generate_pdf_report(user_name, total_score, result)
    st.download_button(
        label="PDF 리포트 다운로드",
        data=pdf_file,
        file_name="gambling_report.pdf",
        mime="application/pdf"
    )

    st.markdown("---")
    st.caption("※ 본 검사는 자가진단 도구이며, 정확한 진단은 전문가 상담을 통해 확인해야 합니다.")
