"""
TalentPulse - Online Mülakat Kayıtları Analitik Deposu (DuckDB OLAP)
Gerçek video ve ses dosyası metaverileri, çok modlu akustik ve görsel sinyal analizlerini saklar.
"""

import duckdb
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import DB_PATH

def get_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    """Gerçek video ve ses mülakat oturumları için DuckDB şemasını oluşturur ve günceller."""
    con = get_connection()
    con.execute("""
        CREATE TABLE IF NOT EXISTS online_interview_sessions (
            session_id VARCHAR PRIMARY KEY,
            candidate_name VARCHAR,
            role VARCHAR,
            experience_years INTEGER,
            interview_question VARCHAR,
            video_duration_sec INTEGER,
            transcript_text VARCHAR,
            detected_keywords VARCHAR[],
            missing_keywords VARCHAR[],
            technical_score DOUBLE,
            sentiment_score DOUBLE,
            final_status VARCHAR,
            evaluation_summary VARCHAR,
            processing_time_ms DOUBLE,
            media_file_name VARCHAR,
            thumbnail_name VARCHAR,
            video_resolution VARCHAR,
            audio_clarity_score DOUBLE,
            created_at TIMESTAMP
        )
    """)
    # Migration: Çok modlu (Multimodal) ses ve görüntü sütunlarını ekle
    con.execute("""
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS media_file_name VARCHAR;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS thumbnail_name VARCHAR;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS video_resolution VARCHAR;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS audio_clarity_score DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS fps DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS snr_db DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS speech_wpm INTEGER;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS silence_ratio_pct DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS visual_focus_score DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS eye_contact_pct DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS multimodal_composite_score DOUBLE;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS phone_detected_count INTEGER;
        ALTER TABLE online_interview_sessions ADD COLUMN IF NOT EXISTS eye_contact_loss_count INTEGER;
    """)

    # Telemetri tablosu
    con.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_events (
            event_id VARCHAR PRIMARY KEY,
            session_id VARCHAR,
            event_type VARCHAR,
            details VARCHAR,
            created_at TIMESTAMP
        )
    """)
    con.close()

def save_interview_session(record: Dict[str, Any]):
    """Gerçek ses/video oturum kaydını çok modlu metrikleriyle DuckDB'ye yazar."""
    con = get_connection()
    con.execute("""
        INSERT OR REPLACE INTO online_interview_sessions (
            session_id, candidate_name, role, experience_years, interview_question,
            video_duration_sec, transcript_text, detected_keywords, missing_keywords,
            technical_score, sentiment_score, final_status, evaluation_summary,
            processing_time_ms, media_file_name, thumbnail_name, video_resolution,
            audio_clarity_score, fps, snr_db, speech_wpm, silence_ratio_pct,
            visual_focus_score, eye_contact_pct, multimodal_composite_score,
            phone_detected_count, eye_contact_loss_count, created_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, [
        record["session_id"],
        record["candidate_name"],
        record["role"],
        record["experience_years"],
        record["interview_question"],
        record["video_duration_sec"],
        record["transcript_text"],
        record["detected_keywords"],
        record["missing_keywords"],
        record["technical_score"],
        record["sentiment_score"],
        record["final_status"],
        record["evaluation_summary"],
        record["processing_time_ms"],
        record.get("media_file_name", ""),
        record.get("thumbnail_name", ""),
        record.get("video_resolution", "1280x720"),
        record.get("audio_clarity_score", 88.0),
        record.get("fps", 30.0),
        record.get("snr_db", 26.5),
        record.get("speech_wpm", 125),
        record.get("silence_ratio_pct", 8.5),
        record.get("visual_focus_score", 94.0),
        record.get("eye_contact_pct", 91.0),
        record.get("multimodal_composite_score", record.get("technical_score", 85.0)),
        record.get("phone_detected_count", 0),
        record.get("eye_contact_loss_count", 0),
        record.get("created_at", datetime.now())
    ])
    con.close()

def get_interview_sessions(limit: int = 50, role: Optional[str] = None) -> List[Dict[str, Any]]:
    """Tamamlanan online mülakat kayıtlarını listeler."""
    con = get_connection()
    query = "SELECT * FROM online_interview_sessions"
    params = []
    if role:
        query += " WHERE role = ?"
        params.append(role)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor = con.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    con.close()

    result = []
    for row in rows:
        d = dict(zip(columns, row))
        d["detected_keywords"] = list(d.get("detected_keywords") or [])
        d["missing_keywords"] = list(d.get("missing_keywords") or [])
        d["audio_clarity_score"] = float(d.get("audio_clarity_score") or 88.0)
        d["snr_db"] = float(d.get("snr_db") or 26.5)
        d["speech_wpm"] = int(d.get("speech_wpm") or 125)
        d["silence_ratio_pct"] = float(d.get("silence_ratio_pct") or 8.5)
        d["visual_focus_score"] = float(d.get("visual_focus_score") or 94.0)
        d["eye_contact_pct"] = float(d.get("eye_contact_pct") or 91.0)
        d["fps"] = float(d.get("fps") or 30.0)
        d["multimodal_composite_score"] = float(d.get("multimodal_composite_score") or d.get("technical_score") or 80.0)
        d["phone_detected_count"] = int(d.get("phone_detected_count") or 0)
        d["eye_contact_loss_count"] = int(d.get("eye_contact_loss_count") or 0)
        if isinstance(d.get("created_at"), datetime):
            d["created_at"] = d["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        result.append(d)

    return result

def get_interview_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Tekil mülakat oturum detayını döner."""
    con = get_connection()
    cursor = con.execute("SELECT * FROM online_interview_sessions WHERE session_id = ?", [session_id])
    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()
    con.close()
    if not row:
        return None
    d = dict(zip(columns, row))
    d["detected_keywords"] = list(d.get("detected_keywords") or [])
    d["missing_keywords"] = list(d.get("missing_keywords") or [])
    d["audio_clarity_score"] = float(d.get("audio_clarity_score") or 88.0)
    d["snr_db"] = float(d.get("snr_db") or 26.5)
    d["speech_wpm"] = int(d.get("speech_wpm") or 125)
    d["silence_ratio_pct"] = float(d.get("silence_ratio_pct") or 8.5)
    d["visual_focus_score"] = float(d.get("visual_focus_score") or 94.0)
    d["eye_contact_pct"] = float(d.get("eye_contact_pct") or 91.0)
    d["fps"] = float(d.get("fps") or 30.0)
    d["multimodal_composite_score"] = float(d.get("multimodal_composite_score") or d.get("technical_score") or 80.0)
    d["phone_detected_count"] = int(d.get("phone_detected_count") or 0)
    d["eye_contact_loss_count"] = int(d.get("eye_contact_loss_count") or 0)
    if isinstance(d.get("created_at"), datetime):
        d["created_at"] = d["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    return d

def get_analytics_summary() -> Dict[str, Any]:
    """Mülakat oturumları üzerinden anlık OLAP analitik özetini çıkarır."""
    start_t = time.time()
    con = get_connection()
    
    kpi_query = """
        SELECT 
            COUNT(*) AS total_interviews,
            COALESCE(AVG(technical_score), 0.0) AS avg_score,
            COALESCE(SUM(CASE WHEN final_status = 'FINAL_INTERVIEW_RECOMMENDED' THEN 1 ELSE 0 END), 0) AS recommended_count,
            COALESCE(SUM(CASE WHEN final_status = 'HR_REVIEW_NEEDED' THEN 1 ELSE 0 END), 0) AS review_count,
            COALESCE(SUM(CASE WHEN final_status = 'INTERVIEW_FAILED' THEN 1 ELSE 0 END), 0) AS rejected_count,
            COALESCE(AVG(video_duration_sec), 0.0) AS avg_duration_sec,
            COALESCE(AVG(audio_clarity_score), 0.0) AS avg_audio_clarity,
            COALESCE(AVG(processing_time_ms), 0.0) AS avg_latency_ms,
            COALESCE(AVG(multimodal_composite_score), 0.0) AS avg_composite_score,
            COALESCE(AVG(snr_db), 0.0) AS avg_snr,
            COALESCE(AVG(visual_focus_score), 0.0) AS avg_visual_focus,
            COALESCE(AVG(eye_contact_pct), 0.0) AS avg_eye_contact
        FROM online_interview_sessions
    """
    kpis = con.execute(kpi_query).fetchone()
    
    role_query = """
        SELECT 
            role, 
            COUNT(*) as interview_count, 
            ROUND(AVG(technical_score), 1) as avg_score,
            SUM(CASE WHEN final_status = 'FINAL_INTERVIEW_RECOMMENDED' THEN 1 ELSE 0 END) as passed
        FROM online_interview_sessions
        GROUP BY role
        ORDER BY interview_count DESC
    """
    role_breakdown = con.execute(role_query).fetchall()
    
    status_query = """
        SELECT final_status, COUNT(*) as count 
        FROM online_interview_sessions 
        GROUP BY final_status
    """
    status_counts = dict(con.execute(status_query).fetchall())

    olap_query_ms = round((time.time() - start_t) * 1000, 2)
    con.close()

    return {
        "kpis": {
            "total_interviews": int(kpis[0]),
            "avg_score": round(float(kpis[1]), 1),
            "recommended": int(kpis[2]),
            "review": int(kpis[3]),
            "rejected": int(kpis[4]),
            "avg_duration_sec": round(float(kpis[5]), 0),
            "avg_audio_clarity": round(float(kpis[6]), 1),
            "avg_latency_ms": round(float(kpis[7]), 1),
            "avg_composite_score": round(float(kpis[8]), 1),
            "avg_snr": round(float(kpis[9]), 1),
            "avg_visual_focus": round(float(kpis[10]), 1),
            "avg_eye_contact": round(float(kpis[11]), 1),
            "olap_query_ms": olap_query_ms
        },
        "role_breakdown": [
            {"role": r[0], "count": int(r[1]), "avg_score": float(r[2]), "passed": int(r[3])}
            for r in role_breakdown
        ],
        "status_distribution": status_counts
    }

def get_multimodal_analytics() -> Dict[str, Any]:
    """Çok Modlu Ses ve Görüntü Analitiği + DuckDB Big Data OLAP metrikleri."""
    start_t = time.time()
    con = get_connection()
    query = """
        SELECT 
            COUNT(*) as total_evaluated,
            ROUND(AVG(COALESCE(multimodal_composite_score, technical_score)), 1) as avg_composite,
            ROUND(AVG(COALESCE(audio_clarity_score, 85.0)), 1) as avg_clarity,
            ROUND(AVG(COALESCE(snr_db, 26.0)), 1) as avg_snr,
            ROUND(AVG(COALESCE(speech_wpm, 125)), 0) as avg_wpm,
            ROUND(AVG(COALESCE(silence_ratio_pct, 9.0)), 1) as avg_silence_pct,
            ROUND(AVG(COALESCE(visual_focus_score, 92.0)), 1) as avg_visual_focus,
            ROUND(AVG(COALESCE(eye_contact_pct, 90.0)), 1) as avg_eye_contact,
            ROUND(AVG(COALESCE(fps, 30.0)), 1) as avg_fps,
            COALESCE(SUM(phone_detected_count), 0) as total_phone_breaches,
            COALESCE(SUM(eye_contact_loss_count), 0) as total_eye_breaches
        FROM online_interview_sessions
    """
    row = con.execute(query).fetchone()
    olap_query_ms = round((time.time() - start_t) * 1000, 3)
    con.close()

    return {
        "total_evaluated": int(row[0]),
        "avg_composite": float(row[1] or 0),
        "avg_clarity": float(row[2] or 0),
        "avg_snr": float(row[3] or 0),
        "avg_wpm": int(row[4] or 0),
        "avg_silence_pct": float(row[5] or 0),
        "avg_visual_focus": float(row[6] or 0),
        "avg_eye_contact": float(row[7] or 0),
        "avg_fps": float(row[8] or 0),
        "total_phone_breaches": int(row[9] or 0),
        "total_eye_breaches": int(row[10] or 0),
        "olap_query_latency_ms": olap_query_ms,
        "engine": "DuckDB Columnar In-Memory OLAP",
        "streaming_buffer": "Async Multi-Topic Queue"
    }

def get_question_difficulty_analytics() -> List[Dict[str, Any]]:
    """DuckDB ile mülakat sorularının zorluk ve başarı oranlarını hesaplar."""
    con = get_connection()
    query = """
        SELECT 
            interview_question,
            COUNT(*) as total_asked,
            ROUND(AVG(technical_score), 1) as avg_score,
            ROUND(SUM(CASE WHEN final_status = 'FINAL_INTERVIEW_RECOMMENDED' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 1) as pass_rate_pct
        FROM online_interview_sessions
        GROUP BY interview_question
        ORDER BY total_asked DESC
    """
    rows = con.execute(query).fetchall()
    con.close()
    return [
        {
            "question": r[0],
            "total_asked": int(r[1]),
            "avg_score": float(r[2] or 0),
            "pass_rate_pct": float(r[3] or 0)
        }
        for r in rows
    ]

def save_telemetry_event(event: Dict[str, Any]):
    """Sekme değişimi veya odak kaybı gibi güvenlik olaylarını kaydeder."""
    con = get_connection()
    con.execute("""
        INSERT INTO telemetry_events (event_id, session_id, event_type, details, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, [
        event.get("event_id") or f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
        event.get("session_id", "UNKNOWN"),
        event.get("event_type", "GENERIC_EVENT"),
        event.get("details", ""),
        datetime.now()
    ])
    con.close()

def clear_all_data():
    """Tüm oturum verilerini sıfırlar."""
    con = get_connection()
    con.execute("DELETE FROM online_interview_sessions")
    con.execute("DELETE FROM telemetry_events")
    con.close()
