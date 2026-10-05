"""
TalentPulse - Junior Seviye Mülakat Simülatörü
Yeni mezun ve junior adayların doğal konuşma tarzını, okul ve staj deneyimlerini yansıtan gerçekçi oturumlar.
Ağır terimler yok; temel OOP, sınıf, nesne, basit sorgular ve problem çözme odaklı.
"""

import random
import uuid
from typing import List, Dict, Any

SAMPLE_JUNIOR_SESSIONS = [
    {
        "candidate_name": "Ömer Çakan",
        "role": "Junior Backend Developer (C# / .NET)",
        "experience_years": 1,
        "interview_question": "Soru: Kendinizi tanıtıp C# ile nesne yönelimli programlama (OOP), sınıf ve veritabanı temellerini projelerinizde nasıl kullandığınızı anlatır mısınız?",
        "video_duration_sec": 95,
        "transcript_text": (
            "Merhaba, Yönetim Bilişim Sistemleri yeni mezunuyum. "
            "Üniversitede ve yaptığım projelerde nesne yönelimli programlama (OOP) mantığını C# ile öğrendim. "
            "Kod yazarken sınıflar (class) ve nesneler (object) oluşturarak projeyi parçalara ayırdım. "
            "Tekrarlayan işler için metot ve fonksiyonlar yazdım. "
            "Veritabanı tarafında SQL tablolarını bağlamak için temel Entity Framework ve LINQ sorguları kullandım. "
            "Bir hata çıktığında loglara bakıp adım adım çözmeyi seviyorum, öğrenmeye çok istekliyim."
        )
    },
    {
        "candidate_name": "Ali Demir (Junior C#)",
        "role": "Junior Backend Developer (C# / .NET)",
        "experience_years": 0,
        "interview_question": "Soru: C# ile nesne yönelimli programlama ve sınıf mantığını nasıl öğrendiniz?",
        "video_duration_sec": 75,
        "transcript_text": (
            "Okulda C# dersi aldık. Temel düzeyde class ve nesne oluşturmayı, if-else döngülerini ve fonksiyon yazmayı biliyorum. "
            "Veritabanında basit SQL tabloları açıp ekleme çıkarma yaptık. Henüz çok tecrübeli değilim ama junior olarak kendimi geliştirmek istiyorum."
        )
    },
    {
        "candidate_name": "Zeynep Kaya (Junior Data)",
        "role": "Junior Data Engineer (Python / Big Data)",
        "experience_years": 1,
        "interview_question": "Soru: Python ve SQL ile verileri nasıl topladınız ve analiz ettiniz?",
        "video_duration_sec": 85,
        "transcript_text": (
            "Üniversite bitirme projemde Python ve Pandas kullanarak e-ticaret sitelerinden veri çektik. "
            "Gelen verilerdeki eksik satırları temizleme işlemi yaptık. "
            "Sonrasında SQL veritabanına aktarıp temel SELECT ve GROUP BY sorguları ile raporlar hazırladım."
        )
    },
    {
        "candidate_name": "Burak Şen (Junior Destek)",
        "role": "IT Support & Systems Specialist",
        "experience_years": 1,
        "interview_question": "Soru: Bilgisayarı açılmayan veya ağa bağlanamayan bir kullanıcıya nasıl destek olursunuz?",
        "video_duration_sec": 90,
        "transcript_text": (
            "Kullanıcı aradığında önce sorunu dinlerim. Ağ bağlantısı yoksa IP adresi ve kablo kontrolü yaparım. "
            "Windows ortamında kullanıcı şifre sıfırlama işlerini Active Directory üzerinden hallederim. "
            "Yazıcı veya donanım arızalarında hızlıca yerinde destek veririm."
        )
    }
]

def generate_interview_batch(count: int = 5) -> List[Dict[str, Any]]:
    """Junior seviyede simüle edilmiş mülakat oturumları üretir."""
    batch = []
    for _ in range(count):
        template = random.choice(SAMPLE_JUNIOR_SESSIONS)
        session = template.copy()
        session["session_id"] = f"SES-2026-{str(uuid.uuid4())[:6].upper()}"
        batch.append(session)
    return batch
