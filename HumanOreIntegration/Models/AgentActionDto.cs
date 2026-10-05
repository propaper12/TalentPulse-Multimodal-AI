using System.Text.Json.Serialization;

namespace HumanOreIntegration.Models;

/// <summary>
/// Otonom İK Ajanı tarafından üretilen karar, eylem ve mülakat soru önerisi DTO modeli.
/// </summary>
public class AgentActionDto
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("timestamp")]
    public string Timestamp { get; set; } = string.Empty;

    [JsonPropertyName("candidate_name")]
    public string CandidateName { get; set; } = string.Empty;

    [JsonPropertyName("role")]
    public string Role { get; set; } = string.Empty;

    [JsonPropertyName("status")]
    public string Status { get; set; } = string.Empty;

    [JsonPropertyName("score")]
    public double Score { get; set; }

    [JsonPropertyName("observation")]
    public string Observation { get; set; } = string.Empty;

    [JsonPropertyName("reasoning")]
    public string Reasoning { get; set; } = string.Empty;

    [JsonPropertyName("action_type")]
    public string ActionType { get; set; } = string.Empty;

    [JsonPropertyName("action_summary")]
    public string ActionSummary { get; set; } = string.Empty;

    [JsonPropertyName("suggested_tech_question")]
    public string SuggestedTechQuestion { get; set; } = string.Empty;

    [JsonPropertyName("email_draft")]
    public string EmailDraft { get; set; } = string.Empty;
}
