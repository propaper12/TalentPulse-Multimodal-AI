using System.Net.Http.Json;
using System.Text.Json;
using HumanOreIntegration.Models;

namespace HumanOreIntegration.Services;

/// <summary>
/// HumanOre C# ana altyapısı için TalentPulse Entegrasyon Servis Gerçekleştirmesi.
/// HttpClient, async/await, LINQ, Çok Modlu Sinyal Analizi ve Otonom Ajan yeteneklerini kullanır.
/// </summary>
public class HumanOrePulseService : IHumanOrePulseService
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;

    public HumanOrePulseService(HttpClient? httpClient = null, string baseUrl = "http://127.0.0.1:8000")
    {
        _httpClient = httpClient ?? new HttpClient();
        _baseUrl = baseUrl.TrimEnd('/');
    }

    /// <summary>
    /// Aday mülakat transkriptini asenkron olarak kuyruğa yollar (Non-blocking).
    /// </summary>
    public async Task<bool> EnqueueInterviewAsync(CandidateInterviewDto candidate)
    {
        try
        {
            var payload = new
            {
                candidate_name = candidate.CandidateName,
                role = candidate.Role,
                experience_years = candidate.ExperienceYears,
                transcript_text = candidate.TranscriptText
            };

            var response = await _httpClient.PostAsJsonAsync($"{_baseUrl}/api/submit-interview", payload);
            return response.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[C# Entegrasyon Hatası] Aday kuyruğa iletilemedi: {ex.Message}");
            return false;
        }
    }

    /// <summary>
    /// DuckDB'de saklanan değerlendirme sonuçlarını C# DTO listesi olarak çeker.
    /// </summary>
    public async Task<List<EvaluationResultDto>> GetEvaluationsAsync(string? roleFilter = null)
    {
        try
        {
            string url = string.IsNullOrEmpty(roleFilter) 
                ? $"{_baseUrl}/api/candidates" 
                : $"{_baseUrl}/api/candidates?role={Uri.EscapeDataString(roleFilter)}";

            var results = await _httpClient.GetFromJsonAsync<List<EvaluationResultDto>>(url);
            return results ?? new List<EvaluationResultDto>();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[C# Entegrasyon Hatası] Veri çekilemedi: {ex.Message}");
            return new List<EvaluationResultDto>();
        }
    }

    /// <summary>
    /// C# LINQ: Sadece önerilen (RECOMMENDED) adayları teknik skora göre sıralar.
    /// </summary>
    public async Task<List<EvaluationResultDto>> GetTopRecommendedCandidatesAsync(int topCount = 5)
    {
        var allCandidates = await GetEvaluationsAsync();

        return allCandidates
            .Where(c => !string.IsNullOrEmpty(c.FinalStatus) && c.FinalStatus.Contains("RECOMMENDED"))
            .OrderByDescending(c => c.TechnicalScore)
            .Take(topCount)
            .ToList();
    }

    /// <summary>
    /// C# LINQ: Çok Modlu (Multimodal) Kompozit Skora göre (Ses Netliği + Görüntü Odak + Teknik) adayları sıralar.
    /// </summary>
    public async Task<List<EvaluationResultDto>> GetTopMultimodalCandidatesAsync(int topCount = 5)
    {
        var allCandidates = await GetEvaluationsAsync();

        return allCandidates
            .OrderByDescending(c => (c.MultimodalCompositeScore.HasValue && c.MultimodalCompositeScore.Value > 0) ? c.MultimodalCompositeScore.Value : c.TechnicalScore)
            .Take(topCount)
            .ToList();
    }

    /// <summary>
    /// Otonom İK Ajanı tarafından üretilen son kararları ve eylemleri çeker.
    /// </summary>
    public async Task<List<AgentActionDto>> GetRecentAgentActionsAsync(int limit = 10)
    {
        try
        {
            var results = await _httpClient.GetFromJsonAsync<List<AgentActionDto>>($"{_baseUrl}/api/agent/actions?limit={limit}");
            return results ?? new List<AgentActionDto>();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[C# Entegrasyon Hatası] Ajan eylemleri çekilemedi: {ex.Message}");
            return new List<AgentActionDto>();
        }
    }

    /// <summary>
    /// Gerçek zamanlı Event Stream akış metriklerini ve throughput değerini çeker.
    /// </summary>
    public async Task<string> GetStreamStatusAsync()
    {
        try
        {
            return await _httpClient.GetStringAsync($"{_baseUrl}/api/stream-status");
        }
        catch (Exception ex)
        {
            return $"{{\"error\": \"{ex.Message}\"}}";
        }
    }

    /// <summary>
    /// DuckDB ile hesaplanan mülakat soru zorluk analitiklerini çeker.
    /// </summary>
    public async Task<string> GetQuestionDifficultyAsync()
    {
        try
        {
            return await _httpClient.GetStringAsync($"{_baseUrl}/api/analytics/question-difficulty");
        }
        catch (Exception ex)
        {
            return $"{{\"error\": \"{ex.Message}\"}}";
        }
    }

    /// <summary>
    /// Çok modlu akustik ve video sinyal analitiği özetini çeker.
    /// </summary>
    public async Task<string> GetMultimodalAnalyticsSummaryAsync()
    {
        try
        {
            return await _httpClient.GetStringAsync($"{_baseUrl}/api/analytics/multimodal");
        }
        catch (Exception ex)
        {
            return $"{{\"error\": \"{ex.Message}\"}}";
        }
    }
}
