using System.Text.Json.Serialization;

namespace HumanOreIntegration.Models;

/// <summary>
/// DuckDB OLAP analitik katmanından C# tarafına dönen çok modlu (multimodal) değerlendirme sonuç modeli.
/// Görüntü (FPS, Çözünürlük, Göz Teması) ve Ses (SNR, Netlik, WPM) verilerini içerir.
/// Nullable türler sayesinde eski/eksik veri kayıtları sorunsuz karşılanır.
/// </summary>
public class EvaluationResultDto
{
    [JsonPropertyName("session_id")]
    public string SessionId { get; set; } = string.Empty;

    [JsonPropertyName("candidate_name")]
    public string CandidateName { get; set; } = string.Empty;

    [JsonPropertyName("role")]
    public string Role { get; set; } = string.Empty;

    [JsonPropertyName("experience_years")]
    public int ExperienceYears { get; set; }

    [JsonPropertyName("technical_score")]
    public double TechnicalScore { get; set; }

    [JsonPropertyName("multimodal_composite_score")]
    public double? MultimodalCompositeScore { get; set; }

    [JsonPropertyName("sentiment_score")]
    public double SentimentScore { get; set; }

    [JsonPropertyName("final_status")]
    public string FinalStatus { get; set; } = string.Empty;

    [JsonPropertyName("evaluation_summary")]
    public string EvaluationSummary { get; set; } = string.Empty;

    // --- Ses & Akustik Sinyal Metrikleri ---
    [JsonPropertyName("audio_clarity_score")]
    public double? AudioClarityScore { get; set; }

    [JsonPropertyName("snr_db")]
    public double? SnrDb { get; set; }

    [JsonPropertyName("speech_wpm")]
    public int? SpeechWpm { get; set; }

    [JsonPropertyName("silence_ratio_pct")]
    public double? SilenceRatioPct { get; set; }

    // --- Görüntü & Video Sinyal Metrikleri ---
    [JsonPropertyName("video_resolution")]
    public string VideoResolution { get; set; } = "1280x720";

    [JsonPropertyName("fps")]
    public double? Fps { get; set; }

    [JsonPropertyName("visual_focus_score")]
    public double? VisualFocusScore { get; set; }

    [JsonPropertyName("eye_contact_pct")]
    public double? EyeContactPct { get; set; }

    // --- Anti-Cheat & Bütünlük Denetim Metrikleri ---
    [JsonPropertyName("phone_detected_count")]
    public int? PhoneDetectedCount { get; set; }

    [JsonPropertyName("eye_contact_loss_count")]
    public int? EyeContactLossCount { get; set; }

    [JsonPropertyName("detected_keywords")]
    public List<string> DetectedKeywords { get; set; } = new();

    [JsonPropertyName("missing_keywords")]
    public List<string> MissingKeywords { get; set; } = new();

    [JsonPropertyName("processing_time_ms")]
    public double ProcessingTimeMs { get; set; }
}
