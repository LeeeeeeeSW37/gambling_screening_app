from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import qrcode
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path_regular = os.path.join(os.path.dirname(__file__), "NanumGothic-Regular.ttf")
font_path_bold = os.path.join(os.path.dirname(__file__), "NanumGothic-Bold.ttf")
pdfmetrics.registerFont(TTFont("Nanum", font_path_regular))
pdfmetrics.registerFont(TTFont("Nanum-Bold", font_path_bold))

def get_detailed_interpretation(score):
    if score < 4:
        return (
            "현재 도박 행동에서 중독 징후는 관찰되지 않습니다. 하지만 도박은 자극적인 보상 시스템을 유발하므로, "
            "앞으로도 일정 간격으로 자가 점검을 해보는 것이 좋습니다. 특히 스트레스 상황에서 도박에 의존하는 습관이 "
            "생기지 않도록 주의해야 합니다."
        )
    elif score <= 5:
        return (
            "도박에 대한 통제력이 약해지고 있거나 초기 징후가 포착됩니다. 이러한 수준은 보통 '위험 사용(risky use)' 단계로, "
            "습관을 스스로 조절하는 것이 아직 가능한 시점입니다. 권장 조치: 도박 일지 작성, 지출 한도 설정, 도박 관련 앱 제거 등 "
            "구체적인 예방 전략을 실천해보세요."
        )
    elif score <= 7:
        return (
            "도박으로 인한 부정적 결과가 현실에서 나타나고 있으며, 외부의 개입이 필요한 상태입니다. "
            "후회·스트레스·경제적 손실이 반복된다면 이미 중독의 중간 단계로 진입한 상태입니다. "
            "권장 조치: 심리 상담사 또는 정신건강의학과와의 첫 면담을 권장합니다. 익명 상담 기관도 좋은 시작점이 될 수 있습니다."
        )
    else:
        return (
            "도박 중독이 일상생활, 인간관계, 경제상태에 심각한 해를 끼치고 있는 상황입니다. "
            "본인의 의지만으로 통제가 어렵고 반복적인 실패 경험이 있을 수 있습니다. "
            "권장 조치: 반드시 전문기관의 개입이 필요합니다. 도박문제관리센터, 중독클리닉, 병원 기반의 행동 치료 등을 적극적으로 "
            "검토해야 합니다. 회복은 충분히 가능합니다."
        )

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

    detailed = get_detailed_interpretation(score)
    text_object = c.beginText(margin + 10, height - 130 * mm)
    text_object.setFont("Nanum", 11)
    for line in detailed.split(". "):
        text_object.textLine(line.strip() + ("" if line.strip().endswith(".") else "."))
    c.drawText(text_object)

    c.setFont("Nanum", 12)
    c.drawString(margin, height - 195 * mm, "문항별 점수 시각화:")

    font_prop = fm.FontProperties(fname=font_path_regular)
    plt.rcParams["font.family"] = font_prop.get_name()

    fig, ax = plt.subplots()
    ax.bar(range(1, len(answers) + 1), answers, color="black", edgecolor="gray")
    ax.set_xlabel("문항 번호", fontproperties=font_prop)
    ax.set_ylabel("점수", fontproperties=font_prop)
    ax.set_title("문항별 점수", fontproperties=font_prop)
    fig.tight_layout()

    img_buf = BytesIO()
    fig.savefig(img_buf, format='PNG')
    plt.close(fig)
    img_buf.seek(0)
    c.drawImage(ImageReader(img_buf), margin, height - 320 * mm, width=150 * mm, height=60 * mm)

    c.showPage()
    c.setFont("Nanum", 12)
    c.drawString(margin, height - 50 * mm, "도움이 필요하신가요? 아래 QR 코드를 스캔하세요:")

    qr = qrcode.make("https://www.kcgp.or.kr")
    qr_buf = BytesIO()
    qr.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    c.drawImage(ImageReader(qr_buf), margin, height - 120 * mm, width=50 * mm, height=50 * mm)

    today = datetime.today().strftime("%Y-%m-%d")
    c.setFont("Nanum", 10)
    c.drawString(margin, 25 * mm, f"리포트 생성일: {today}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
