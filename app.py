import streamlit as st
from questions import questions
from report import generate_pdf_report

st.set_page_config(page_title="도박 중독 검사", layout="centered")
st.title("도박 중독 자가진단 테스트 (DSM-5 기반)")

user_name = st.text_input("이름 (또는 닉네임):")
answers = []

with st.form("gambling_test"):
    for i, q in enumerate(questions):
        score = st.radio(q, [0, 1, 2], key=f"q{i}", horizontal=True)
        answers.append(score)
    submitted = st.form_submit_button("제출")

if submitted:
    total_score = sum(answers)

    if total_score < 4:
        result = "도박 장애 없음"
    elif total_score <= 5:
        result = "경증 도박 장애"
    elif total_score <= 7:
        result = "중등도 도박 장애"
    else:
        result = "중증 도박 장애"

    st.subheader(f"총 점수: {total_score}점")
    st.success(f"결과: {result}")

    pdf_file = generate_pdf_report(user_name, total_score, result)
    st.download_button("PDF 리포트 다운로드", pdf_file, file_name="gambling_report.pdf", mime="application/pdf")
