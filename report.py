# report.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import qrcode

def generate_pdf_report(name, score, result):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    margin_x = 25 * mm
    start_y = height - 40 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, start_y, "도박 중독 자가진단 결과 리포트")

    c.setFont("Helvetica", 12)
    c.drawString(margin_x, start_y - 30, f"이름: {name}")
    c.drawString(margin_x, start_y - 50, f"점수: {score}점")
    c.drawString(margin_x, start_y - 70, f"판단: {result}")
    c.drawString(margin_x, start_y - 100, "진단 기준:")
    c.setFont("Helvetica", 11)
    c.drawString(margin_x + 10, start_y - 120, "- 본 평가는 DSM-5의 도박 장애 기준에 기반함.")
    c.drawString(margin_x + 10, start_y - 140, "- 최근 12개월 동안 9가지 항목 중 4개 이상에 해당될 경우 도박 장애로 진단됩니다.")
    c.drawString(margin_x + 10, start_y - 160, "- 점수 4~5: 경증 / 6~7: 중등도 / 8~9: 중증")

    c.setFont("Helvetica", 12)
    c.drawString(margin_x, start_y - 200, "권장사항:")
    if score >= 8:
        c.drawString(margin_x + 10, start_y - 220, "- 심각한 수준의 도박 문제가 의심되므로 전문가 상담이 필요합니다.")
    elif score >= 6:
        c.drawString(margin_x + 10, start_y - 220, "- 중등도 위험으로 조기 상담이 권장됩니다.")
    elif score >= 4:
        c.drawString(margin_x + 10, start_y - 220, "- 도박 습관에 대한 점검이 필요하며, 주의가 요구됩니다.")
    else:
        c.drawString(margin_x + 10, start_y - 220, "- 현재로서는 큰 문제가 없습니다. 건전한 생활을 유지하세요.")

    # QR 코드 삽입
    c.setFont("Helvetica", 10)
    c.drawString(margin_x, 160, "상담 및 도움 링크 (한국도박문제관리센터):")
    url = "https://www.kcgp.or.kr"
    qr_img = qrcode.make(url)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_reader = ImageReader(qr_buffer)
    c.drawImage(qr_reader, margin_x, 80, width=80, height=80)

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin_x, 60, "※ 본 검사는 자가진단 도구로서, 전문가의 임상적 평가를 대신할 수 없습니다.")
    c.drawString(margin_x, 45, "출처: American Psychiatric Association. (2013). DSM-5")
    c.drawString(margin_x, 30, "추가 정보: National Center for Responsible Gaming, 한국도박문제관리센터")

    today = datetime.today().strftime("%Y-%m-%d")
    c.setFont("Helvetica", 10)
    c.drawString(margin_x, 15, f"리포트 생성일: {today}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
