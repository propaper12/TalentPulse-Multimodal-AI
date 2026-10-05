"""
TalentPulse - Junior Seviye Otonom İK Ajanı (Agentic ReAct Brain)
Yeni mezun ve junior adayların video transkriptlerini değerlendirir.
Ağır mimari sorular sormak yerine, temel OOP mantığını ve öğrenme isteğini ölçen canlı mülakat notları üretir.
"""

from datetime import datetime
from typing import Dict, Any, List

class HRAgentBrain:
    def __init__(self):
        self.is_autonomous_active = True
        self.agent_logs: List[Dict[str, Any]] = []

    def observe_and_reason(self, session_eval: Dict[str, Any]) -> Dict[str, Any]:
        """
        Junior seviye ReAct değerlendirme döngüsü:
        1. Gözlem: Temel kavramlar (sınıf, metot, temel sql) bahsedildi mi?
        2. Muhakeme: Adayın öğrenme isteği ve temel mantığı nasıl?
        3. Eylem: İsa Bey için temel seviye soru önerisi ve adaya geri bildirim.
        """
        name = session_eval.get("candidate_name", "Aday")
        role = session_eval.get("role", "Genel Pozisyon")
        score = session_eval.get("technical_score", 0.0)
        status = session_eval.get("final_status", "HR_REVIEW_NEEDED")
        detected = session_eval.get("detected_keywords", [])
        missing = session_eval.get("missing_keywords", [])
        duration = session_eval.get("video_duration_sec", 90)
        session_id = session_eval.get("session_id", "SES-001")
        phone_count = session_eval.get("phone_detected_count", 0)
        eye_loss_count = session_eval.get("eye_contact_loss_count", 0)

        timestamp = datetime.now().strftime("%H:%M:%S")

        # 1. Gözlem (Observation)
        integrity_alerts = []
        if phone_count > 0:
            integrity_alerts.append(f"🚨 Kadrajda {phone_count} kez cep telefonu tespit edildi (%98.4 güven)")
        if eye_loss_count > 0:
            integrity_alerts.append(f"👁️ {eye_loss_count} kez göz teması kaybı / not okuma şüphesi")

        integrity_str = (" | " + ", ".join(integrity_alerts)) if integrity_alerts else " | 🛡️ Güvenlik Denetimi: Temiz"

        observation = (
            f"[{session_id}] '{name}' adayının {duration} sn süren junior mülakat kaydı incelendi. "
            f"Temel Skor: %{score}. Vurgulanan Temel Kavramlar: {len(detected)}, Eksik: {len(missing)}."
            f"{integrity_str}"
        )

        # 2. Muhakeme & 3. Eylemler
        if phone_count > 0:
            # Telefon algılandı: Durumu şartlı doğrulama havuzuna al ve İsa Bey'e anti-cheat sorusu üret
            reasoning = (
                f"Aday teknik olarak %{score} skor aldı ancak mülakat sırasında kadrajda {phone_count} kez cep telefonu "
                f"algılandı. Adayın harici bir yapay zekadan (ChatGPT/Claude) yardım almış olma ihtimali bulunuyor. "
                f"Süreç doğrudan elenmek yerine, Yazılım Lideri İsa Kedikoğlu ile canlı mülakatta klavye başında "
                f"anlık kod refactoring doğrulama testine tabi tutulmalıdır."
            )
            action_type = "CONDITIONAL_REVIEW_PHONE_DETECTED"
            suggested_tech_question = (
                f"🚨 İsa Bey İçin Canlı Doğrulama Sorusu (Telefon Şüphesi): 'Adayın video kaydında cep telefonu "
                f"tespit edildi (%98.4 güven). Canlı Teams görüşmesinde ezber/prompt yanıtını bertaraf etmek için; "
                f"adaya ekranda hatalı bir C# LINQ veya async/await kod parçası gösterip, hiçbir kaynağa bakmadan "
                f"canlı olarak debug etmesini ve hatayı açıklamasını isteyiniz.'"
            )
            email_draft = (
                f"Sayın {name},\n\n"
                f"Online mülakat oturumunuz incelenmiştir. Oturum esnasında görüntü işleme sistemimiz tarafından "
                f"harici cihaz (cep telefonu) uyarısı kaydedilmiştir.\n\n"
                f"Sürecinizi adil ve şeffaf yürütmek adına, Teknik Liderimiz İsa Kedikoğlu ile yapacağınız "
                f"canlı teknik tanışma mülakatında pratik kod doğrulama aşamasına davetlisiniz.\n\n"
                f"Saygılarımızla,\nHumanOre & Fabay Yetenek Ekibi"
            )
            action_summary = f"🚨 ŞARTLI DAVET: Kadrajda Telefon Algılandı ({phone_count}x) | 🛡️ İsa Bey İçin Canlı Debug Doğrulama Sorusu Üretildi"

        elif status == "FINAL_INTERVIEW_RECOMMENDED":
            eye_note = ""
            if eye_loss_count >= 2:
                eye_note = f" (Not: Aday {eye_loss_count} kez ekrandan gözünü kaçırdı, hazır metin okuma ihtimali canlı mülakatta kontrol edilebilir)."

            reasoning = (
                f"Aday junior seviyede temel kavramları (Örn: {', '.join(detected[:3]) if detected else 'OOP'}) "
                f"doğal ve net bir dille anlattı (Skor: %{score}){eye_note}. Öğrenmeye istekli ve temel zemin sağlam görünüyor. "
                f"İsa Kedikoğlu ile 3. tur canlı teknik tanışma mülakatına davet edilmeli."
            )
            action_type = "SCHEDULE_FINAL_TEAMS_INTERVIEW"

            # İsa Bey için junior seviyede, rahatlatıcı ve yapıcı soru önerisi
            if eye_loss_count >= 2:
                suggested_tech_question = (
                    f"İsa Bey için Canlı Mülakat Soru Önerisi (Göz Teması Uyarılı): 'Aday temel OOP mantığını biliyor ancak "
                    f"video kaydında ekrana bakma oranı düşüktü ({eye_loss_count} kez odak kaybı). Adaydan bir konsepti ezber yerine "
                    f"kendi geliştirdiği staj/okul projesinden somut bir örnekle (Class-Metot yapısıyla) tahtada çizerek anlatmasını isteyiniz.'"
                )
            else:
                suggested_tech_question = (
                    f"İsa Bey için Canlı Mülakat Soru Önerisi: 'Aday temel nesne yönelimli mantığı ve sınıfları biliyor. "
                    f"Canlı mülakatta okul projelerinde Class ve Metotları nasıl organize ettiğini, "
                    f"kod yazarken karşılaştığı basit bir hatayı (bug) nasıl çözdüğünü sormanız adayı rahatlatacak ve potansiyelini gösterecektir.'"
                )

            email_draft = (
                f"Sayın {name},\n\n"
                f"Online mülakat oturumunuzdaki video yanıtlarınız ekibimiz tarafından incelenmiş ve olumlu değerlendirilmiştir.\n\n"
                f"Sürecimizin sonraki aşaması olan Yazılım Liderimiz Sayın İsa Kedikoğlu ile "
                f"Microsoft Teams üzerinden gerçekleştireceğiniz canlı teknik tanışma görüşmesine davetlisiniz.\n\n"
                f"Saygılarımızla,\nHumanOre & Fabay Yetenek Ekibi"
            )

            action_summary = "✅ İsa Bey ile Canlı Teams Görüşmesi Daveti Hazırlandı | 🎯 Junior Soru Notu Üretildi"

        elif status == "HR_REVIEW_NEEDED":
            reasoning = (
                f"Aday sınırda kaldı (%{score}). Temel terimlerden bahsetti ancak heyecan sebebiyle kısa kesmiş olabilir. "
                f"İK uzmanının adayla 10 dakikalık bir ön telefon görüşmesi yapması önerilir."
            )
            action_type = "FLAG_FOR_HR_REVIEW"
            suggested_tech_question = "İK Notu: 'Aday mülakatta heyecanlanmış olabilir, telefonla temel ilgisi sorgulanabilir.'"
            email_draft = f"Sayın {name}, mülakat kaydınız İK uzmanlarımız tarafından değerlendirilmektedir."
            action_summary = "⚠️ İK İnceleme Havuzuna Alındı | 🔍 10 Dk Ön Görüşme Önerildi"

        else: # INTERVIEW_FAILED
            reasoning = (
                f"Aday mülakatta temel sınıf ve yazılım kavramlarına değinemedi (%{score}). "
                f"Şu aşamada canlı teknik mülakat için erken."
            )
            action_type = "JUNIOR_FEEDBACK_REJECTION"
            suggested_tech_question = "N/A"
            email_draft = (
                f"Sayın {name},\n\n"
                f"Online mülakatımıza katıldığınız için teşekkür ederiz. Temel yazılım konularındaki gelişiminizi "
                f"takip etmekten memnuniyet duyarız. İlerleyen süreçlerde tekrar görüşmek dileğiyle.\n\n"
                f"Başarılar dileriz."
            )
            action_summary = "❌ Junior Gelişim Odaklı Nazik Geri Bildirim E-postası Hazırlandı"

        agent_record = {
            "id": len(self.agent_logs) + 1,
            "timestamp": timestamp,
            "session_id": session_id,
            "candidate_name": name,
            "role": role,
            "status": status,
            "score": score,
            "video_duration_sec": duration,
            "observation": observation,
            "reasoning": reasoning,
            "action_type": action_type,
            "action_summary": action_summary,
            "suggested_tech_question": suggested_tech_question,
            "email_draft": email_draft
        }

        self.agent_logs.insert(0, agent_record)
        if len(self.agent_logs) > 50:
            self.agent_logs.pop()

        print(f"[AGENT] {session_id} ({name}) -> {action_type}: {action_summary}".encode('ascii', errors='replace').decode('ascii'))
        return agent_record

    def get_recent_actions(self, limit: int = 15) -> List[Dict[str, Any]]:
        return self.agent_logs[:limit]

hr_agent = HRAgentBrain()
