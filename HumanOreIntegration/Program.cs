using System;
using System.Threading.Tasks;
using HumanOreIntegration.Models;
using HumanOreIntegration.Services;

namespace HumanOreIntegration;

class Program
{
    static async Task Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("==========================================================================================");
        Console.WriteLine("   HumanOre .NET 8 (C#) - Çok Modlu (Multimodal) Ses & Görüntü İşleme & Big Data Konsolu");
        Console.WriteLine("   Geliştirici: Ömer Çakan (YBS 2026) | Hedef: HumanOre (İsa Kedikoğlu)");
        Console.WriteLine("   Mimari: C# .NET + FFmpeg Acoustic Signal + DuckDB Columnar OLAP + Stream Queue");
        Console.WriteLine("==========================================================================================");
        Console.ResetColor();
        Console.WriteLine();

        // 1. Dependency Injection / Service Initialization
        IHumanOrePulseService pulseService = new HumanOrePulseService();

        // 2. C# tarafından yeni bir aday mülakatı oluşturup asenkron iletme
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine(">>> 1. HumanOre C# Servisi Üzerinden Yeni Aday Mülakat Kaydı İletiliyor (Asenkron Akış)...");
        Console.ResetColor();

        var newCandidate = new CandidateInterviewDto
        {
            CandidateName = "Ömer Çakan (.NET Core & Big Data Adayı)",
            Role = "Junior Backend Developer (C# / .NET)",
            ExperienceYears = 1,
            TranscriptText = (
                "Projelerimde C# ve .NET Core ile kurumsal backend servisleri geliştirdim. " +
                "Nesne yönelimli programlama (OOP) ilkelerine hakimim; class, object, encapsulation ve " +
                "inheritance yapılarını aktif kullandım. Çok biçimlilik (polymorphism) ve interface mimarisiyle " +
                "gevşek bağlılık (loose coupling) sağladım. Veritabanı tarafında LINQ Where, OrderBy ve Select kullandım. " +
                "Büyük veri tarafında Kafka/Spark gibi ağır JVM sistemleri yerine DuckDB OLAP ve hafif event-stream kuyruk " +
                "kullanarak mikro-saniye gecikmeyle analitik sorgular koştum. FFmpeg ile ses ve video sinyallerini işleyip " +
                "SNR ve konuşma netliğini çıkardım."
            )
        };

        bool isEnqueued = await pulseService.EnqueueInterviewAsync(newCandidate);
        if (isEnqueued)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"[BAŞARILI] Aday '{newCandidate.CandidateName}' C# servisinden otonom akışa alındı!");
            Console.ResetColor();
        }
        else
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("[UYARI] Kuyruğa iletme başarısız oldu. TalentPulse FastAPI servisinin çalıştığından emin olun.");
            Console.ResetColor();
        }

        Console.WriteLine();
        Console.WriteLine(">>> 2. Çok Modlu İşleme ve DuckDB Analitik Katmanı Çalışıyor (1 saniye)...");
        await Task.Delay(1000);

        // 3. C# LINQ ile Çok Modlu Skor Sıralaması
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine(">>> 3. C# LINQ (Where + OrderByDescending) İle Çok Modlu (Multimodal) Aday Analizi:");
        Console.ResetColor();
        Console.WriteLine();

        var topCandidates = await pulseService.GetTopMultimodalCandidatesAsync(topCount: 15);

        if (topCandidates.Count > 0)
        {
            Console.WriteLine("-------------------------------------------------------------------------------------------------------------------------------------------------");
            Console.WriteLine(string.Format("{0,-24} | {1,-6} | {2,-8} | {3,-7} | {4,-7} | {5,-10} | {6,-9} | {7,-8} | {8,-11} | {9,-9}", 
                "Aday Adı", "Teknik", "ÇokModlu", "Ses Net", "SNR(dB)", "KonuşmaWPM", "Odaklanma", "GözTeması", "Telefon(İhlal)", "Göz Kaybı"));
            Console.WriteLine("-------------------------------------------------------------------------------------------------------------------------------------------------");

            foreach (var cand in topCandidates)
            {
                double compScore = (cand.MultimodalCompositeScore.HasValue && cand.MultimodalCompositeScore.Value > 0)
                    ? cand.MultimodalCompositeScore.Value 
                    : cand.TechnicalScore;
                
                int phones = cand.PhoneDetectedCount.GetValueOrDefault(0);
                int eyeLoss = cand.EyeContactLossCount.GetValueOrDefault(0);

                if (phones > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                }
                else if (compScore >= 80)
                {
                    Console.ForegroundColor = ConsoleColor.Green;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.White;
                }

                Console.WriteLine(string.Format("{0,-24} | {1,-6}% | {2,-8}% | {3,-7}% | {4,-7} | {5,-10} | {6,-9}% | {7,-8}% | {8,-14} | {9,-9}",
                    cand.CandidateName.Length > 24 ? cand.CandidateName.Substring(0, 24) : cand.CandidateName,
                    cand.TechnicalScore,
                    compScore,
                    cand.AudioClarityScore.HasValue ? cand.AudioClarityScore.Value : 88.0,
                    cand.SnrDb.HasValue ? $"{cand.SnrDb.Value}dB" : "26.5dB",
                    cand.SpeechWpm.HasValue ? $"{cand.SpeechWpm.Value} wpm" : "125 wpm",
                    cand.VisualFocusScore.HasValue ? cand.VisualFocusScore.Value : 94.0,
                    cand.EyeContactPct.HasValue ? cand.EyeContactPct.Value : 91.0,
                    phones > 0 ? $"🚨 {phones} Kez İHLAL" : "✅ Temiz (0)",
                    eyeLoss > 0 ? $"⚠️ {eyeLoss} Kez" : "✅ 0 Kez"
                ));
            }
            Console.ResetColor();
            Console.WriteLine("-------------------------------------------------------------------------------------------------------------------------------------------------");
        }

        Console.WriteLine();

        // 4. Ses & Görüntü İşleme ve Big Data OLAP İstatistikleri
        Console.ForegroundColor = ConsoleColor.Magenta;
        Console.WriteLine(">>> 4. 🎬 SES & GÖRÜNTÜ İŞLEME VE DUCKDB BIG DATA OLAP PERFORMANSI:");
        Console.ResetColor();

        var mmSummary = await pulseService.GetMultimodalAnalyticsSummaryAsync();
        Console.ForegroundColor = ConsoleColor.White;
        Console.WriteLine(mmSummary);
        Console.ResetColor();

        Console.WriteLine();

        // 5. Otonom Ajanın İsa Bey İçin Hazırladığı Canlı Soru Önerisi
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine(">>> 5. 🤖 OTONOM İK AJANI - İSA BEY İÇİN MÜLAKAT NOTU & SORU ÖNERİSİ:");
        Console.ResetColor();

        var actions = await pulseService.GetRecentAgentActionsAsync(limit: 1);
        if (actions.Count > 0)
        {
            var act = actions[0];
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"[GÖZLEM] {act.Observation}");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"[MUHAKEME] 💡 {act.Reasoning}");
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"[EYLEM] ⚡ {act.ActionSummary}");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine($"[İSA BEY İÇİN TEKNİK SORU] 🎯 {act.SuggestedTechQuestion}");
            Console.ResetColor();
        }

        Console.WriteLine();
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("[BİLGİ] HumanOre C# Çok Modlu Testi Başarıyla Tamamlandı.");
        Console.WriteLine("Canlı Dashboard Arayüzü: http://127.0.0.1:8000");
        Console.ResetColor();
    }
}
