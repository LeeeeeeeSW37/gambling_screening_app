from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import qrcode
import matplotlib.pyplot as plt

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

font_path_regular = os.path.join(os.path.dirname(__file__), "NanumGothic-Regular.ttf")
font_path_bold = os.path.join(os.path.dirname(__file__), "NanumGothic-Bold.ttf")
pdfmetrics.registerFont(TTFont("Nanum", font_path_regular))
pdfmetrics.registerFont(TTFont("Nanum-Bold", font_path_bold))

def generate_pdf_report(name, score, result, interpretation, answers):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 25 * mm

    c.setFont("Nanum-Bold", 18)
    c.drawString(margin, height - 40 * mm, "도박 중독 자가진단 결과 리포트")

    c.setFont("Nanum", 12)
    c.drawString(margin, height - 60 * mm, f"이름: {name}")
    c.drawString(margin, height - 75 * mm, f"총 점수: {score}점")
    c.drawString(margin, height - 90 * mm, f"진단 결과: {result}")
    c.drawString(margin, height - 110 * mm, "상세 해석:")
    c.setFont("Nanum", 11)
    c.drawString(margin + 10, height - 125 * mm, interpretation)

    c.setFont("Nanum", 12)
    c.drawString(margin, height - 155 * mm, "문항별 점수 시각화:")

    # 응답 그래프 그리기
    fig, ax = plt.subplots()
    ax.bar(range(1, len(answers) + 1), answers)
    ax.set_xlabel("문항 번호")
    ax.set_ylabel("점수")
    ax.set_title("문항별 점수")
    fig.tight_layout()

    img_buf = BytesIO()
    fig.savefig(img_buf, format='PNG')
    plt.close(fig)
    img_buf.seek(0)
    c.drawImage(ImageReader(img_buf), margin, height - 280 * mm, width=150 * mm, height=60 * mm)

    # QR 코드
    qr = qrcode.make("https://www.kcgp.or.kr")
    qr_buf = BytesIO()
    qr.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    c.drawString(margin, 50 * mm, "도움이 필요하신가요? 아래 QR 코드를 스캔하세요:")
    c.drawImage(ImageReader(qr_buf), margin, 20 * mm, width=40 * mm, height=40 * mm)

    today = datetime.today().strftime("%Y-%m-%d")
    c.setFont("Nanum", 10)
    c.drawString(margin, 10 * mm, f"리포트 생성일: {today}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
