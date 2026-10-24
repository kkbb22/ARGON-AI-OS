import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "sandbox" / "content-pack"


def build_content():
    topic = "نظام إدارة العيادات"
    headline = "خلي إدارة عيادتك أسهل وركز على مرضاك"

    instagram = (
        f"{headline} 🩺\n\n"
        "تنظيم المواعيد وملفات المرضى ومتابعة العمل اليومي "
        "يساعدك على إدارة عيادتك بصورة أوضح.\n\n"
        "مع الحلول الرقمية المناسبة تقدر تقلل الاعتماد على الورق "
        "وتنظم سير العمل داخل العيادة.\n\n"
        "حاب تعرف كيف ممكن التقنية تخدم عيادتك تواصل مع ARGON.\n\n"
        "#ARGON #إدارة_العيادات #التحول_الرقمي #الأردن"
    )

    facebook = (
        f"{headline}\n\n"
        "هل تضيع وقتا في متابعة المواعيد والملفات الورقية\n"
        "يساعد نظام إدارة العيادات على تنظيم المواعيد وملفات المرضى "
        "وتسهيل متابعة العمل اليومي من مكان واحد.\n\n"
        "تقدم ARGON حلولا رقمية تساعد عيادتك على تنظيم إجراءاتها.\n"
        "راسلنا لمعرفة المزيد عن الحل المناسب لعيادتك."
    )

    x_post = (
        "إدارة العيادة تبدأ بتنظيم العمل: المواعيد ملفات المرضى "
        "والمتابعة اليومية. اكتشف كيف تساعدك الحلول الرقمية من ARGON "
        "على تنظيم سير العمل. #ARGON"
    )

    return {
        "brand": "ARGON",
        "topic": topic,
        "headline": headline,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
        "platforms": {
            "instagram": instagram,
            "facebook": facebook,
            "x": x_post
        },
        "visual_brief": (
            "تصميم عربي احترافي لعيادة حديثة مقارنة بصرية بين "
            "أوراق ومواعيد مبعثرة وواجهة رقمية منظمة. "
            "لا تعرض بيانات مرضى حقيقية أو نتائج غير مثبتة."
        ),
        "review_checklist": [
            "مراجعة اللغة واللهجة وملاءمة الرسالة للجمهور الأردني",
            "التحقق من دقة كل ادعاء تسويقي قبل النشر",
            "إضافة شعار ARGON والهوية البصرية المعتمدة",
            "مراجعة التصميم على الهاتف",
            "موافقة بشرية صريحة قبل النشر"
        ],
        "publishing": {
            "published": False,
            "automatic_publishing_enabled": False
        }
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    package = build_content()
    target = OUTPUT / "content-pack.json"
    target.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    review = OUTPUT / "REVIEW-BEFORE-PUBLISH.md"
    review.write_text(
        "# مراجعة منشور ARGON\n\n"
        f"**الموضوع:** {package['topic']}\n\n"
        f"**العنوان:** {package['headline']}\n\n"
        "**الحالة:** مسودة تحتاج موافقة بشرية.\n\n"
        + "\n".join(f"- [ ] {item}" for item in package["review_checklist"])
        + "\n\n**لم يتم النشر تلقائيا.**\n",
        encoding="utf-8"
    )
    print("CONTENT PACKAGE CREATED")
    print(target)
    print(review)
    print("Status:", package["status"])


if __name__ == "__main__":
    main()
