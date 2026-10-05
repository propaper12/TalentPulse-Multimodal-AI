"""
TalentPulse - CV Tabanlı Soru ve Dinamik Takip Sorusu Motoru (Dynamic Interview Engine)
Adayın CV'sine (YBS, C#, Microsoft, Samsung, verisepeti.net) göre kişiselleştirilmiş sorular hazırlar;
konuşma anında adayın bahsettiği detayları yakalayarak anlık takip soruları üretir.
"""

from typing import Dict, Any, List

# Ömer Çakan'ın CV Source of Truth bilgileri
CANDIDATE_CV_PROFILE = {
    "name": "Ömer Çakan",
    "degree": "Yönetim Bilişim Sistemleri (YBS / MIS) - İstanbul Gelişim Üniversitesi",
    "core_skills": ["C#", "OOP", "SQL", "Entity Framework", "LINQ", "Python", "Büyük Veri", "FastAPI"],
    "experiences": [
        {"company": "verisepeti.net", "role": "Kurucu Ortak & Veri Geliştirici", "details": "E-ticaret fiyat karşılaştırma ve veri toplama"},
        {"company": "Microsoft AI Innovators", "role": "Yaz Stajyeri", "details": "Kurumsal yapay zeka ve iş akışları"},
        {"company": "Samsung Innovation Campus", "role": "Yapay Zeka Stajyeri", "details": "Veri bilimi ve makine öğrenmesi projeleri"}
    ]
}

CV_TAILORED_QUESTIONS = [
    {
        "id": "Q1",
        "topic": "CV & Başlangıç",
        "question": "Ömer Bey, Yönetim Bilişim Sistemleri mezuniyetinizden ve yazılım tarafında C# nesne yönelimli programlama (OOP) mantığını projelerinizde nasıl kullandığınızdan bahseder misiniz?"
    },
    {
        "id": "Q2",
        "topic": "verisepeti.net & Veritabanı",
        "question": "CV'nizde yer alan verisepeti.net projenizde e-ticaret verilerini toplarken SQL ve veritabanı tablolarını C# veya Python tarafında nasıl organize ettiniz?"
    },
    {
        "id": "Q3",
        "topic": "Microsoft & Proje Kültürü",
        "question": "Microsoft AI Innovators stajınızda edindiğiniz tecrübeler ışığında; kod yazarken karşılaştığınız bir hatayı (bug) çözme yaklaşımınızı anlatır mısınız?"
    }
]

def generate_dynamic_followup(spoken_text: str) -> Dict[str, Any]:
    """
    Adayın konuşmasını analiz edip, standart sorularda olmayan ama adayın bizzat bahsettiği
    bir terimi / deneyimi anında yakalayıp dinamik takip sorusu üretir.
    """
    text_lower = spoken_text.lower()
    
    # Kural ve Anlamsal Tetikleyiciler
    if "verisepeti" in text_lower or "kazıma" in text_lower or "scraping" in text_lower or "fiyat" in text_lower:
        return {
            "triggered_by": "verisepeti.net / Veri Çekme",
            "question": "verisepeti projenizden bahsettiniz; farklı e-ticaret sitelerinden fiyat çekerken sitelerin yapısı değiştiğinde veya hata aldığınızda bunu kod tarafında nasıl yönettiniz?",
            "context": "Aday kendi girişiminden bahsetti; hata toleransı ve veri tutarlılığı sorgulandı."
        }
    elif "linq" in text_lower or "where" in text_lower or "select" in text_lower:
        return {
            "triggered_by": "C# LINQ",
            "question": "C#'ta LINQ kullandığınızı belirttiniz; verileri filtrelerken LINQ'in Where fonksiyonu ile klasik for/foreach döngüsü arasında size göre nasıl bir fark var?",
            "context": "Aday LINQ terimini kullandı; kod okunabilirliği ve pratik anlayışı sorgulandı."
        }
    elif "entity framework" in text_lower or "orm" in text_lower:
        return {
            "triggered_by": "Entity Framework / ORM",
            "question": "Entity Framework kullandığınızdan söz ettiniz; veritabanında yeni bir tablo eklerken veya güncelleme (CRUD) yaparken EF size nasıl bir kolaylık sağladı?",
            "context": "Aday ORM mimarisinden bahsetti; pratik veritabanı deneyimi sorgulandı."
        }
    elif "microsoft" in text_lower or "azure" in text_lower or "staj" in text_lower:
        return {
            "triggered_by": "Microsoft Stajı",
            "question": "Microsoft AI programındaki stajınızda ekip çalışması yaparken iş mantığı ile yazılım geliştirme arasındaki dengeyi nasıl kurdunuz?",
            "context": "Aday stajından bahsetti; YBS vizyonu ve ekip adaptasyonu sorgulandı."
        }
    elif "class" in text_lower or "sınıf" in text_lower or "nesne" in text_lower or "object" in text_lower:
        return {
            "triggered_by": "Sınıf & Nesne Mimarisi",
            "question": "Sınıf ve nesnelerden bahsettiniz; geliştirdiğiniz bir projede bir sınıfı (Class) ve onun içine koyduğunuz özellikleri basit bir örnekle anlatabilir misiniz?",
            "context": "Aday OOP'den bahsetti; somut bir junior örneği istendi."
        }
    elif "hata" in text_lower or "bug" in text_lower or "log" in text_lower or "try" in text_lower:
        return {
            "triggered_by": "Hata Yönetimi",
            "question": "Hata çözmekten bahsettiniz; C#'ta beklenmeyen bir hata oluştuğunda try-catch bloğunu nasıl kullandınız?",
            "context": "Aday hata ayıklamadan bahsetti; temel Exception yönetimi sorgulandı."
        }
    else:
        # Genel dinamik soru
        return {
            "triggered_by": "Genel Proje Deneyimi",
            "question": "Anlattığınız bu projede sizi teknik olarak en çok heyecanlandıran ve en çok şey öğrendiğiniz kısım ne oldu?",
            "context": "Adayın motivasyonu ve öğrenme eğrisi sorgulandı."
        }
