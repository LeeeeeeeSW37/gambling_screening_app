import streamlit as st
from questions import questions
from report import generate_pdf_report
import matplotlib.pyplot as plt

st.set_page_config(page_title="도박 중독 자가진단", layout="centered")
st.title("도박 중독 자가진단 테스트 (DSM-5 기준)")

user_name = st.text_input("이름 또는 닉네임:")
answers = []

with st.form("gambling_test"):
    for i, q in enumerate(questions):
        score = st.radio(q, [0, 1, 2], key=f"q{i}", horizontal=True,
                         help="0: 전혀 아니다 / 1: 가끔 그렇다 / 2: 자주 그렇다")
        answers.append(score)
    submitted = st.form_submit_button("제출")

if submitted:
    total_score = sum(answers)

    if total_score < 4:
        result = "도박 장애 없음"
        interpretation = "현재로서는 도박 관련 문제가 없습니다. 하지만 주기적인 자기 점검은 도움이 됩니다."
    elif total_score <= 5:
        result = "경증 도박 장애"
        interpretation = "초기적인 도박 문제 징후가 보입니다. 습관을 조절하고 예방 교육을 고려해보세요."
    elif total_score <= 7:
        result = "중등도 도박 장애"
        interpretation = "도박으로 인해 일상 기능에 영향을 받는 상태입니다. 전문가 상담을 진지하게 고려하세요."
    else:
        result = "중증 도박 장애"
        interpretation = "심각한 도박 중독 위험이 있습니다. 즉시 정신건강 전문가의 도움이 필요합니다."

    st.subheader(f"총 점수: {total_score}점")
    st.success(f"진단 결과: {result}")
    st.info(interpretation)

    st.markdown("### 문항별 응답 점수 시각화")
    fig, ax = plt.subplots()
    ax.bar(range(1, len(answers)+1), answers)
    ax.set_xlabel("문항 번호")
    ax.set_ylabel("응답 점수")
    ax.set_title("도박 위험 응답 점수")
    st.pyplot(fig)

    pdf_file = generate_pdf_report(user_name, total_score, result, interpretation, answers)
    st.download_button("PDF 리포트 다운로드", pdf_file, file_name="gambling_report.pdf", mime="application/pdf")

    st.caption("※ 본 검사는 자가진단 도구이며, 전문가의 진단을 대체하지 않습니다.")
