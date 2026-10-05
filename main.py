"""
TalentPulse - Online Mülakat Kayıtları Analiz & Otonom İK Motoru
Gerçek Ses/Video Dosyalarını işler, SpeechRecognition ve Web Speech ile anlık transkripsiyon yapar,
Çok modlu akustik & görsel sinyal işleme yapar ve DuckDB OLAP üzerinde analitik özetler sunar.
"""

import os
import uuid
import time
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, Query, UploadFile, File, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import storage
from queue_stream import stream_queue
from ai_scorer import process_interview_event, analyze_transcript
from producer_sim import generate_interview_batch
from agent_engine import hr_agent
import media_processor
from dynamic_questions import CV_TAILORED_QUESTIONS, generate_dynamic_followup, CANDIDATE_CV_PROFILE

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media_storage"
MEDIA_DIR.mkdir(exist_ok=True)

app = FastAPI(title="TalentPulse - Çok Modlu Mülakat & Büyük Veri Analitik Motoru", version="3.1.0")

app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

class InterviewSessionSubmission(BaseModel):
    candidate_name: str
    role: str
    experience_years: int = 0
    interview_question: str = "Soru 1: Teknik deneyiminizi anlatın."
    video_duration_sec: int = 120
    transcript_text: str

@app.on_event("startup")
async def startup_event():
    storage.init_db()
    await stream_queue.start_consumer(process_interview_event)
    print(">>> [TalentPulse v3.1] Çok Modlu Mülakat & DuckDB OLAP Sunucusu Başlatıldı.")

@app.on_event("shutdown")
async def shutdown_event():
    await stream_queue.stop()

@app.post("/api/submit-interview")
async def submit_interview(submission: InterviewSessionSubmission):
    """C# ve harici istemcilerden gelen transkriptleri asenkron kuyruğa iletir."""
    session_data = submission.model_dump() if hasattr(submission, "model_dump") else submission.dict()
    session_data["session_id"] = f"SES-{str(uuid.uuid4())[:8].upper()}"
    await stream_queue.produce(session_data)
    return {
        "status": "queued",
        "session_id": session_data["session_id"],
        "message": "Mülakat kaydı başarıyla kuyruğa alındı."
    }

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    html_file = BASE_DIR / "dashboard.html"
    return HTMLResponse(content=html_file.read_text(encoding="utf-8"))

# ==================== CV VE DİNAMİK SORU ENDPOINT'LERİ ====================

@app.get("/api/agent/cv-questions")
async def get_cv_questions():
    """Ömer Çakan'ın CV'sine göre hazırlanmış kişiselleştirilmiş soruları döner."""
    return JSONResponse(content={
        "profile": CANDIDATE_CV_PROFILE,
        "questions": CV_TAILORED_QUESTIONS
    })

@app.post("/api/agent/generate-followup")
async def generate_followup(payload: Dict[str, Any] = Body(...)):
    """Aday konuşurken anlattığı detaylardan dinamik takip sorusu üretir."""
    spoken_text = payload.get("spoken_text", "")
    followup = generate_dynamic_followup(spoken_text)
    return JSONResponse(content=followup)

# ==================== GERÇEK VİDEO YÜKLEME VE ÇOK MODLU İŞLEME ====================

@app.post("/api/upload-media-interview")
async def upload_media_interview(
    file: UploadFile = File(...),
    candidate_name: str = Form(...),
    role: str = Form(...),
    experience_years: int = Form(1),
    interview_question: str = Form("Soru 1: C# OOP mimarisi ve projelerinizdeki veri akışını anlatın."),
    live_transcript: Optional[str] = Form(None),
    tab_switch_count: int = Form(0),
    phone_detected_count: int = Form(0),
    eye_contact_loss_count: int = Form(0)
):
    """
    Kameradan veya dosyadan gelen gerçek videoyu/sesi işler.
    FFmpeg ile 16kHz mono WAV çıkarır, akustik SNR ve volumedetect ölçümleri yapar,
    video çözünürlüğü/FPS/göz teması/telefon tespiti parametrelerini hesaplayıp DuckDB OLAP deposuna kaydeder.
    """
    start_time = time.time()
    session_id = f"SES-{str(uuid.uuid4())[:8].upper()}"

    # 1. Dosyayı diske kaydet
    file_extension = Path(file.filename or "video.webm").suffix.lower() or ".webm"
    base_name = f"{session_id}_{uuid.uuid4().hex[:6]}"
    saved_filename = f"{base_name}{file_extension}"
    saved_path = MEDIA_DIR / saved_filename

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. FFprobe metadata (çözünürlük, süre, fps, codec)
    meta = media_processor.extract_media_metadata(str(saved_path))
    duration_sec = meta["duration_sec"] or 60
    resolution = meta["resolution"]
    fps = meta["fps"]

    # 3. FFmpeg audio (16kHz mono WAV) & thumbnail (JPEG)
    wav_path, thumb_path = media_processor.extract_audio_and_thumbnail(str(saved_path), base_name)
    thumbnail_name = Path(thumb_path).name if thumb_path and os.path.exists(thumb_path) else ""

    # 4. Transkript belirleme (Canlı Web Speech API veya FFmpeg WAV SpeechRecognition)
    if live_transcript and len(live_transcript.strip()) > 10:
        extracted_transcript = live_transcript.strip()
    else:
        stt_result = media_processor.transcribe_speech(wav_path, language="tr-TR")
        if stt_result and len(stt_result.strip()) > 5:
            extracted_transcript = stt_result
        else:
            extracted_transcript = f"[Ses Kaydı]: Aday online mülakat sorusuna sözlü yanıt verdi."

    # 5. Akustik ve Ses Sinyali İşleme (FFmpeg volumedetect, SNR, WPM, Sessizlik Oranı)
    audio_sig = media_processor.analyze_audio_signals(wav_path, extracted_transcript, duration_sec)

    # 6. Görüntü ve Video Sinyali İşleme (Görsel Odak, Göz Teması, Işıklandırma)
    video_sig = media_processor.analyze_video_signals(meta["has_video"], resolution, fps)

    # 7. Yetkinlik ve NLP Analizi
    detected, missing, tech_score, sent_score, status, summary = analyze_transcript(
        extracted_transcript, role, experience_years
    )

    # 8. Çok Modlu Kompozit Skor (Teknik + Ses + Görsel + Akıcılık)
    composite_score = media_processor.calculate_multimodal_composite_score(
        technical_score=tech_score,
        audio_clarity=audio_sig["audio_clarity_score"],
        visual_focus=video_sig["visual_focus_score"],
        fluency_score=audio_sig["fluency_score"],
        has_video=meta["has_video"]
    )

    # Güvenlik ve Anti-Cheat Denetimleri
    if phone_detected_count > 0:
        summary += f" [🚨 Anti-Cheat Uyarısı: Mülakat anında {phone_detected_count} kez cep telefonu tespit edildi]."
    if eye_contact_loss_count > 0:
        summary += f" [👁️ Göz Teması Uyarısı: {eye_contact_loss_count} kez odak kaybı / ekrandan ayrılma]."
    if tab_switch_count > 0:
        summary += f" [Sekme Uyarısı: Mülakat anında {tab_switch_count} kez başka sekmeye geçildi]."

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    # 9. DuckDB OLAP tablosuna kaydet
    record = {
        "session_id": session_id,
        "candidate_name": candidate_name,
        "role": role,
        "experience_years": experience_years,
        "interview_question": interview_question,
        "video_duration_sec": duration_sec,
        "transcript_text": extracted_transcript,
        "detected_keywords": detected,
        "missing_keywords": missing,
        "technical_score": tech_score,
        "sentiment_score": sent_score,
        "final_status": status,
        "evaluation_summary": summary,
        "processing_time_ms": processing_time_ms,
        "media_file_name": saved_filename,
        "thumbnail_name": thumbnail_name,
        "video_resolution": resolution,
        "audio_clarity_score": audio_sig["audio_clarity_score"],
        "fps": fps,
        "snr_db": audio_sig["snr_db"],
        "speech_wpm": audio_sig["speech_wpm"],
        "silence_ratio_pct": audio_sig["silence_ratio_pct"],
        "visual_focus_score": video_sig["visual_focus_score"],
        "eye_contact_pct": video_sig["eye_contact_pct"],
        "multimodal_composite_score": composite_score,
        "phone_detected_count": phone_detected_count,
        "eye_contact_loss_count": eye_contact_loss_count
    }

    storage.save_interview_session(record)

    # 10. Otonom Ajan (İsa Kedikoğlu için canlı soru notu üretimi)
    agent_record = hr_agent.observe_and_reason(record)

    return {
        "status": "success",
        "session_id": session_id,
        "candidate_name": candidate_name,
        "extracted_transcript": extracted_transcript,
        "technical_score": tech_score,
        "multimodal_composite_score": composite_score,
        "audio_clarity_score": audio_sig["audio_clarity_score"],
        "snr_db": audio_sig["snr_db"],
        "speech_wpm": audio_sig["speech_wpm"],
        "silence_ratio_pct": audio_sig["silence_ratio_pct"],
        "visual_focus_score": video_sig["visual_focus_score"],
        "eye_contact_pct": video_sig["eye_contact_pct"],
        "video_resolution": resolution,
        "fps": fps,
        "media_url": f"/media/{saved_filename}",
        "thumbnail_url": f"/media/{thumbnail_name}" if thumbnail_name else None,
        "agent_decision": agent_record["action_summary"],
        "isa_bey_question": agent_record["suggested_tech_question"],
        "tab_switch_count": tab_switch_count,
        "phone_detected_count": phone_detected_count,
        "eye_contact_loss_count": eye_contact_loss_count
    }

# ==================== DİĞER ANALİTİK VE AKIŞ ENDPOINT'LERİ ====================

@app.post("/api/simulate-batch")
async def simulate_batch(count: int = Query(default=5, ge=1, le=100)):
    sessions = generate_interview_batch(count=count)
    for s in sessions:
        await stream_queue.produce(s)
    return {"status": "batch_enqueued", "count": count}

@app.get("/api/candidates")
@app.get("/api/interview-sessions")
async def get_sessions(role: Optional[str] = None, limit: int = 100):
    data = storage.get_interview_sessions(limit=limit, role=role)
    return JSONResponse(content=data)

@app.get("/api/analytics")
async def get_analytics():
    summary = storage.get_analytics_summary()
    return JSONResponse(content=summary)

@app.get("/api/analytics/multimodal")
async def get_multimodal_analytics():
    """Çok modlu ses/video ve DuckDB OLAP sorgu istatistiklerini döner."""
    data = storage.get_multimodal_analytics()
    return JSONResponse(content=data)

@app.get("/api/stream-status")
async def get_stream_status():
    return JSONResponse(content=stream_queue.get_metrics())

@app.get("/api/candidates/{session_id}")
async def get_candidate_session(session_id: str):
    data = storage.get_interview_session(session_id)
    if not data:
        return JSONResponse(status_code=404, content={"error": "Session not found"})
    return JSONResponse(content=data)

@app.post("/api/telemetry/event")
async def post_telemetry_event(payload: Dict[str, Any] = Body(...)):
    """Aday mülakat sırasında sekme değiştirdiğinde veya odak kaybettiğinde event stream'e basar."""
    await stream_queue.produce_event("interview.telemetry", payload)
    return {"status": "event_ingested", "topic": "interview.telemetry"}

@app.get("/api/analytics/question-difficulty")
async def get_question_difficulty():
    """DuckDB ile hesaplanan mülakat soru zorluk ve başarı oranlarını döner."""
    data = storage.get_question_difficulty_analytics()
    return JSONResponse(content=data)

@app.get("/api/agent/actions")
async def get_agent_actions(limit: int = 20):
    actions = hr_agent.get_recent_actions(limit=limit)
    return JSONResponse(content=actions)

@app.post("/api/clear-data")
async def clear_data():
    storage.clear_all_data()
    hr_agent.agent_logs.clear()
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir=str(BASE_DIR), reload_dirs=[str(BASE_DIR)])
