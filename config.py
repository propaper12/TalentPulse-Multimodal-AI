from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "talent_pulse_analytics.duckdb")

ROLE_COMPETENCY_MAP = {
    "Junior Backend Developer (C# / .NET)": {
        "interview_question": "Kendinizi kısaca tanıtıp C# ile nesne yönelimli programlama (OOP), sınıf (class) ve veritabanı temellerini projelerinizde nasıl kullandığınızı anlatır mısınız?",
        # Junior seviyede aranan temel kavramlar (ağır terimler yok)
        "core_keywords": [
            "c#", "oop", "sınıf", "nesne", "class", "object", "metot", "fonksiyon",
            "sql", "veritabanı", "entity framework", "linq", "hata"
        ],
        "min_experience_expected": 0,
        "pass_threshold": 50  # Junior için dostane baraj
    },
    "Junior Data Engineer (Python / Big Data)": {
        "interview_question": "Üniversitede veya projelerinizde Python ve SQL kullanarak verileri nasıl topladınız, temizlediniz ve sorguladınız?",
        "core_keywords": [
            "python", "sql", "veri", "tablo", "sorgu", "temizleme",
            "veritabanı", "analiz", "pipeline", "pandas"
        ],
        "min_experience_expected": 0,
        "pass_threshold": 50
    },
    "Junior AI / ML Developer": {
        "interview_question": "Makine öğrenmesi ve yapay zeka alanında yaptığınız temel bir projeyi, modeli nasıl eğittiğinizi anlatır mısınız?",
        "core_keywords": [
            "python", "model", "veri", "öğrenme", "yapay zeka",
            "eğitim", "scikit-learn", "tahmin", "proje"
        ],
        "min_experience_expected": 0,
        "pass_threshold": 50
    },
    "IT Support & Systems Specialist": {
        "interview_question": "Kullanıcılardan gelen bilgisayar, ağ veya şifre sıfırlama sorunlarında ilk hangi adımları izlersiniz?",
        "core_keywords": [
            "donanım", "ağ", "network", "windows", "active directory",
            "format", "ip", "yazıcı", "destek", "sorun giderme"
        ],
        "min_experience_expected": 0,
        "pass_threshold": 45
    }
}
