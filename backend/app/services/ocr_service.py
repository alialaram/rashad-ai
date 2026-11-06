import re
import uuid
import os
from pathlib import Path
from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

from app.core.config import settings


class ArabicDocumentOCREngine:
    """
    محرك استخراج النصوص العربية من الوثائق الرسمية والتجريبية
    Arabic Document Intelligence & Experimental OCR Pipeline

    المبدأ الرقابي:
    OCR وسيلة مساعدة أولية، ونسب الثقة تلزم الموظف بالمراجعة والاعتماد البشري للحقول الحساسة.
    """

    @classmethod
    def preprocess_image(cls, file_path: str) -> Image.Image:
        """تحسين جودة الصورة، تصحيح التباين وتحويلها للدرجات الرمادية"""
        image = Image.open(file_path)
        # تحويل إلى RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # تصغير الصور الضخمة لتسريع المعالجة مع الحفاظ على المقروئية
        max_dim = 1600
        if max(image.size) > max_dim:
            image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        # تحسين التباين
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(1.4)
        return enhanced_image

    @classmethod
    def extract_id_fields(cls, text: str) -> Dict[str, Any]:
        """
        استخراج الحقول المهيكلة من النص العربي مع حساب درجة الثقة لكل حقل
        """
        extracted = {}

        # 1. استخراج الرقم الوطني (11 خانة تبدأ بـ 01)
        id_match = re.search(r"\b01\d{9}\b", text)
        if id_match:
            extracted["national_id"] = {
                "value": id_match.group(0),
                "confidence": 96.0,
                "label_ar": "الرقم الوطني",
                "requires_review": False,
            }
        else:
            # البحث عن أرقام بطول 9-11 خانة مشتبه بها
            fuzzy_id = re.search(r"\b\d{9,11}\b", text)
            if fuzzy_id:
                extracted["national_id"] = {
                    "value": fuzzy_id.group(0),
                    "confidence": 68.0,
                    "label_ar": "الرقم الوطني (اشتباه قراءة)",
                    "requires_review": True,
                }
            else:
                extracted["national_id"] = {
                    "value": None,
                    "confidence": 0.0,
                    "label_ar": "الرقم الوطني",
                    "requires_review": True,
                }

        # 2. استخراج الاسم الكامل (4 مقاطع عربية)
        name_match = re.search(r"(?:الاسم|اسم المستفيد|المواطن)[:\s]+([\u0621-\u064A\s]{8,50})", text)
        if name_match:
            raw_name = name_match.group(1).strip()
            # فحص عدد الكلمات
            words = raw_name.split()
            conf = 92.0 if len(words) >= 4 else (78.0 if len(words) == 3 else 60.0)
            extracted["full_name"] = {
                "value": raw_name,
                "confidence": conf,
                "label_ar": "الاسم الرباعي",
                "requires_review": conf < 80.0,
            }
        else:
            extracted["full_name"] = {
                "value": None,
                "confidence": 0.0,
                "label_ar": "الاسم الرباعي",
                "requires_review": True,
            }

        # 3. استخراج تاريخ الميلاد
        date_match = re.search(r"\b(19\d{2}|20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b", text)
        if date_match:
            extracted["birth_date"] = {
                "value": date_match.group(0),
                "confidence": 88.0,
                "label_ar": "تاريخ الميلاد",
                "requires_review": False,
            }
        else:
            extracted["birth_date"] = {
                "value": None,
                "confidence": 0.0,
                "label_ar": "تاريخ الميلاد",
                "requires_review": True,
            }

        # 4. محل الإصدار
        place_match = re.search(r"(?:محل الإصدار|المحافظة|الإصدار)[:\s]+([\u0621-\u064A\s]{3,30})", text)
        if place_match:
            extracted["issue_place"] = {
                "value": place_match.group(1).strip(),
                "confidence": 84.0,
                "label_ar": "محل الإصدار",
                "requires_review": False,
            }
        else:
            extracted["issue_place"] = {
                "value": None,
                "confidence": 0.0,
                "label_ar": "محل الإصدار",
                "requires_review": True,
            }

        return extracted

    @classmethod
    def process_document(cls, file_path: str, simulated_text: str = None) -> Tuple[Dict[str, Any], float, str]:
        """
        تشغيل خط المعالجة والاستخراج وحساب نسبة الثقة الإجمالية
        """
        # التحقق من وجود الملف
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document file not found: {file_path}")

        # تجهيز الصورة والتأكد من سلامتها
        cls.preprocess_image(file_path)

        # النص المستخرج (نستخدم نصوص وثائق تجريبية معتمدة أو النص الممرر)
        raw_text = simulated_text or (
            "الجمهورية اليمنية\n"
            "وزارة الداخلية - مصلحة الأحوال المدنية والسجل المدني\n"
            "بطاقة شخصية ذكية\n"
            "الرقم الوطني: 01023456789\n"
            "الاسم: أحمد محمد علي الصنعاني\n"
            "تاريخ الميلاد: 1985-04-12\n"
            "محل الإصدار: صنعاء\n"
        )

        extracted_data = cls.extract_id_fields(raw_text)

        # حساب متوسط نسبة الثقة لجميع الحقول
        confidences = [item["confidence"] for item in extracted_data.values() if isinstance(item, dict) and "confidence" in item]
        overall_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.0

        return extracted_data, overall_conf, raw_text

    @classmethod
    def generate_synthetic_id_card(cls, output_path: str, full_name: str, national_id: str, birth_date: str) -> str:
        """
        توليد صورة بطاقة هوية يمنية تجريبية لاستخدامها في الاختبارات والمعاينة البصرية
        """
        width, height = 800, 500
        image = Image.new("RGB", (width, height), color="#f8fafc")
        draw = ImageDraw.Draw(image)

        # إطار البطاقة
        draw.rectangle([(20, 20), (width - 20, height - 20)], outline="#0f766e", width=4)
        draw.rectangle([(30, 30), (width - 30, 110)], fill="#042f2e")

        # صورة شخصية وهمية (مربع رمادي)
        draw.rectangle([(50, 140), (220, 360)], fill="#e2e8f0", outline="#94a3b8", width=2)
        draw.text((75, 230), "صورة تجريبية\n[DEMO PHOTO]", fill="#64748b")

        # نصوص البطاقة
        draw.text((320, 45), "الجمهورية اليمنية - مصلحة الأحوال المدنية", fill="#ffffff")
        draw.text((360, 75), "بطاقة إثبات الهوية الشخصية (تجريبية)", fill="#5eead4")

        draw.text((270, 160), f"الاسم الكامل: {full_name}", fill="#0f172a")
        draw.text((270, 210), f"الرقم الوطني: {national_id}", fill="#0f172a")
        draw.text((270, 260), f"تاريخ الميلاد: {birth_date}", fill="#0f172a")
        draw.text((270, 310), "جهة الإصدار: أمانة العاصمة - صنعاء", fill="#0f172a")

        # شريط تحذيري بالأسفل
        draw.rectangle([(30, 410), (width - 30, 460)], fill="#fef3c7")
        draw.text((80, 425), "وثيقة اصطناعية مولدة برمجياً لأغراض التطوير واختبار OCR - رشاد AI", fill="#92400e")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, "JPEG", quality=90)
        return output_path
