using HumanOreIntegration.Models;

namespace HumanOreIntegration.Services;

/// <summary>
/// HumanOre C# mimarisinin TalentPulse yapay zeka, analitik ve Çok Modlu (Multimodal) ses/görüntü motoruyla haberleşmesini sağlayan arayüz.
/// Loose coupling (Gevşek bağlılık) ve Dependency Injection için tasarlanmıştır.
/// </summary>
public interface IHumanOrePulseService
{
    /// <summary>
    /// Aday mülakat transkriptini asenkron olarak kuyruğa (Queue) iletir.
    /// </summary>
    Task<bool> EnqueueInterviewAsync(CandidateInterviewDto candidate);

    /// <summary>
    /// DuckDB analitik katmanından aday değerlendirme sonuçlarını asenkron olarak çeker.
    /// </summary>
    Task<List<EvaluationResultDto>> GetEvaluationsAsync(string? roleFilter = null);

    /// <summary>
    /// LINQ kullanarak en yüksek skorlu ve önerilen (RECOMMENDED) adayları filtreler.
    /// </summary>
    Task<List<EvaluationResultDto>> GetTopRecommendedCandidatesAsync(int topCount = 5);

    /// <summary>
    /// LINQ kullanarak çok modlu (ses netliği + görüntü odağı + teknik) kompozit puana göre en iyi adayları filtreler.
    /// </summary>
    Task<List<EvaluationResultDto>> GetTopMultimodalCandidatesAsync(int topCount = 5);

    /// <summary>
    /// Otonom İK Ajanının ürettiği son kararları, eylemleri ve İsa Bey için soru önerilerini çeker.
    /// </summary>
    Task<List<AgentActionDto>> GetRecentAgentActionsAsync(int limit = 10);

    /// <summary>
    /// Gerçek zamanlı Event Stream kuyruk durumunu ve throughput değerini çeker.
    /// </summary>
    Task<string> GetStreamStatusAsync();

    /// <summary>
    /// DuckDB ile hesaplanan mülakat soru zorluk analitiklerini çeker.
    /// </summary>
    Task<string> GetQuestionDifficultyAsync();

    /// <summary>
    /// Çok modlu akustik ve video sinyal analitiği özetini çeker.
    /// </summary>
    Task<string> GetMultimodalAnalyticsSummaryAsync();
}
