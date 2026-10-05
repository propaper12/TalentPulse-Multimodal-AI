namespace HumanOreIntegration.Models;

/// <summary>
/// HumanOre C# ana sisteminden TalentPulse akış hattına gönderilecek aday mülakat DTO modeli.
/// </summary>
public class CandidateInterviewDto
{
    public string CandidateName { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public int ExperienceYears { get; set; }
    public string TranscriptText { get; set; } = string.Empty;

    public CandidateInterviewDto() { }

    public CandidateInterviewDto(string name, string role, int experience, string transcript)
    {
        CandidateName = name;
        Role = role;
        ExperienceYears = experience;
        TranscriptText = transcript;
    }
}
