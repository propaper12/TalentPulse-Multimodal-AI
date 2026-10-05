"""
TalentPulse - Online Mülakat Kayıtları Analiz, NLP & Çok Modlu Değerlendirme Motoru
Adayların kaydettiği video/ses mülakat transkriptlerini inceler, teknik doğruluğu ve
akustik/görsel sinyalleri puanlar, Otonom İK Ajanını tetikleyerek İsa Kedikoğlu için canlı mülakat soru notu üretir.
"""

import time
import re
import uuid
from typing import Dict, Any, List, Tuple
from config import ROLE_COMPETENCY_MAP
import storage
from agent_engine import hr_agent
import media_processor

POSITIVE_ACTION_KEYWORDS = [
    "geliştirdim", "tasarladım", "kurduk", "çözdüm", "öğrendim", "yönettim",
    "kullandım", "entegre", "optimize", "analiz", "başardık", "deneyimledim",
    "implemented", "designed", "developed", "built", "solved", "optimized"
]

def analyze_transcript(
    transcript: str, 
    role: str, 
    experience_years: int
) -> Tuple[List[str], List[str], float, float, str, str]:
    """Mülakat transkriptini NLP ile analiz eder."""
    role_config = ROLE_COMPETENCY_MAP.get(role)
    if not role_config:
        core_keywords = ["yazılım", "proje", "kod", "geliştirme", "ekip"]
        pass_threshold = 60
    else:
        core_keywords = role_config["core_keywords"]
        pass_threshold = role_config["pass_threshold"]

    clean_text = transcript.lower()
    
    # 1. Anahtar Kelime Taraması
    detected_keywords = []
    missing_keywords = []
    for kw in core_keywords:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, clean_text) or kw in clean_text:
            detected_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    # 2. Teknik Skor Hesaplama (0 - 100)
    kw_coverage = (len(detected_keywords) / max(len(core_keywords), 1)) * 100
    word_count = len(clean_text.split())
    depth_bonus = min(word_count / 10.0, 15.0)
    exp_bonus = min(experience_years * 5.0, 10.0)

    raw_score = (kw_coverage * 0.75) + depth_bonus + exp_bonus
    technical_score = round(min(max(raw_score, 15.0), 98.0), 1)

    # 3. Özgüven ve Aksiyon Skoru
    action_matches = sum(1 for word in POSITIVE_ACTION_KEYWORDS if word in clean_text)
    sentiment_score = round(min(50.0 + (action_matches * 10.0), 95.0), 1)

    # 4. Final Kararı
    if technical_score >= pass_threshold:
        final_status = "FINAL_INTERVIEW_RECOMMENDED"
    elif technical_score >= (pass_threshold - 15):
        final_status = "HR_REVIEW_NEEDED"
    else:
        final_status = "INTERVIEW_FAILED"

    summary = (
        f"Aday online mülakat kaydında {len(core_keywords)} temel kavramdan {len(detected_keywords)} tanesine yer verdi "
        f"({', '.join(detected_keywords[:4]) if detected_keywords else 'hiçbiri'}). "
        f"Teknik skor: {technical_score}%, Durum: {final_status}."
    )

    return detected_keywords, missing_keywords, technical_score, sentiment_score, final_status, summary

async def process_interview_event(event: Dict[str, Any]):
    """Kuyruktan gelen online mülakat oturumunu çok modlu sinyallerle işler."""
    start_time = time.time()
    
    session_id = event.get("session_id") or f"SES-{str(uuid.uuid4())[:8].upper()}"
    candidate_name = event.get("candidate_name", "Aday")
    role = event.get("role", "Junior Backend Developer (C# / .NET)")
    experience_years = event.get("experience_years", 0)
    interview_question = event.get("interview_question", "Soru 1: Teknik deneyiminizi ve mimari kararlarınızı anlatın.")
    video_duration_sec = event.get("video_duration_sec", 120)
    transcript_text = event.get("transcript_text", "")

    # 1. NLP ve Teknik Analiz
    detected, missing, tech_score, sent_score, status, summary = analyze_transcript(
        transcript_text, role, experience_years
    )

    # 2. Akustik ve Ses Sinyali İşleme
    wav_path = event.get("wav_path", "")
    audio_sig = media_processor.analyze_audio_signals(wav_path, transcript_text, video_duration_sec)
    
    # 3. Video ve Görsel Sinyal İşleme
    has_video = event.get("has_video", True)
    resolution = event.get("video_resolution", "1280x720")
    fps = event.get("fps", 30.0)
    video_sig = media_processor.analyze_video_signals(has_video, resolution, fps)

    # 4. Çok Modlu Kompozit Skor (Multimodal Composite Score)
    composite_score = media_processor.calculate_multimodal_composite_score(
        technical_score=tech_score,
        audio_clarity=audio_sig["audio_clarity_score"],
        visual_focus=video_sig["visual_focus_score"],
        fluency_score=audio_sig["fluency_score"],
        has_video=has_video
    )

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    record = {
        "session_id": session_id,
        "candidate_name": candidate_name,
        "role": role,
        "experience_years": experience_years,
        "interview_question": interview_question,
        "video_duration_sec": video_duration_sec,
        "transcript_text": transcript_text,
        "detected_keywords": detected,
        "missing_keywords": missing,
        "technical_score": tech_score,
        "sentiment_score": sent_score,
        "final_status": status,
        "evaluation_summary": summary,
        "processing_time_ms": processing_time_ms,
        "media_file_name": event.get("media_file_name", ""),
        "thumbnail_name": event.get("thumbnail_name", ""),
        "video_resolution": resolution,
        "audio_clarity_score": audio_sig["audio_clarity_score"],
        "fps": fps,
        "snr_db": audio_sig["snr_db"],
        "speech_wpm": audio_sig["speech_wpm"],
        "silence_ratio_pct": audio_sig["silence_ratio_pct"],
        "visual_focus_score": video_sig["visual_focus_score"],
        "eye_contact_pct": video_sig["eye_contact_pct"],
        "multimodal_composite_score": composite_score
    }

    # 5. DuckDB'ye kaydet
    storage.save_interview_session(record)
    print(f"[Worker] Mülakat Kaydı İşlendi: {candidate_name} ({role}) -> Multimodal Skor: {composite_score} ({processing_time_ms}ms)")

    # 6. Otonom Ajanı tetikle
    hr_agent.observe_and_reason(record)
