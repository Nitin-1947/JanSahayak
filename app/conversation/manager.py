import uuid
from typing import Optional

from app.agent.brain import OllamaBrain
from app.agent.response import clean_response
from app.memory.conversation_history import save_message, get_recent_messages
from app.memory.database import get_connection
from app.profile.profile_manager import ProfileManager
from app.profile.profile_extractor import ProfileExtractor
from app.schemes.scheme_service import SchemeService


class ConversationManager:
    def __init__(self, brain: OllamaBrain, scheme_service: SchemeService):
        self.brain = brain
        self.scheme_service = scheme_service
        self.profile_manager = ProfileManager()
        self.profile_extractor = ProfileExtractor()

    def create_user(self, phone_number: Optional[str] = None):
        # Reuse the same local profile when the caller's phone number is known.
        if phone_number:
            connection = get_connection()
            row = connection.execute(
                "SELECT user_id FROM citizen_profiles WHERE phone_number = ? LIMIT 1",
                (phone_number,),
            ).fetchone()
            connection.close()
            if row:
                return row["user_id"]

        user_id = str(uuid.uuid4())
        self.profile_manager.create_profile(user_id, phone_number)
        return user_id

    def process(self, user_id: str, text: str):
        save_message(user_id, "user", text)

        extracted = self.profile_extractor.extract_basic(text)
        if extracted:
            self.profile_manager.update_profile(user_id, **extracted)

        profile = self.profile_manager.get_profile(user_id)

        if self._is_scheme_query(text) and profile:
            results = self.scheme_service.get_user_schemes(profile)
            response = self._explain_scheme_results(results, text)
        else:
            history = get_recent_messages(user_id, limit=8)
            profile_context = self._profile_context(profile)
            messages = [
                {"role": "system", "content": profile_context},
                *history,
            ]
            response = self.brain.generate(messages)

        response = clean_response(response)
        save_message(user_id, "assistant", response)
        return response

    def _is_scheme_query(self, text: str):
        keywords = [
            "योजना", "स्कीम", "scheme", "सरकार", "सरकारी", "लाभ",
            "पात्र", "eligibility", "आवेदन", "apply",
        ]
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    def _profile_context(self, profile):
        if not profile:
            return "Citizen profile उपलब्ध नहीं है।"
        return f"""Citizen profile:
Name: {profile.name}
Age: {profile.age}
Gender: {profile.gender}
State: {profile.state}
District: {profile.district}
Residence: {profile.residence_type}
Occupation: {profile.occupation}
Employment: {profile.employment_status}
Income: {profile.income}
Category: {profile.social_category}
Disability: {profile.disability}
Student: {profile.student}
Farmer: {profile.farmer}

इस profile को केवल relevant assistance देने के लिए उपयोग करें।
"""

    def _explain_scheme_results(self, results, user_question):
        if not results:
            return (
                "आपकी अभी दी गई जानकारी के आधार पर कोई matching सरकारी योजना नहीं मिली। "
                "अगर आप चाहें तो मैं आपकी profile की जरूरी जानकारी लेकर दोबारा जांच कर सकता हूँ।"
            )

        structured = []
        for result in results[:5]:
            scheme = result.scheme
            structured.append({
                "name": scheme.name,
                "status": result.status,
                "benefits": scheme.benefits[:3] if scheme.benefits else [],
                "reasons": result.reasons[:4] if result.reasons else [],
                "missing": result.missing[:6] if result.missing else [],
                "documents": scheme.documents[:6] if scheme.documents else [],
                "application_steps": scheme.application_steps[:5] if scheme.application_steps else [],
                "application_url": scheme.application_url,
                "official_source_url": scheme.official_source_url,
                "last_verified": scheme.last_verified,
            })

        import json
        grounding = json.dumps(structured, ensure_ascii=False, indent=2)
        prompt = f"""User का सवाल: {user_question}

यह verified/structured scheme data है। इसे बदलना, अनुमान लगाना या नई eligibility बनाना मना है:
{grounding}

इस data के आधार पर 2-5 छोटे Hindi/Hinglish वाक्यों में phone-call के लिए natural जवाब दें।
Status को ऐसे समझाएं: eligible = उपलब्ध नियमों के अनुसार पात्रता मानदंड पूरे हो रहे हैं, लेकिन अंतिम सरकारी पुष्टि जरूरी है; possibly_eligible = कुछ जानकारी बाकी है।
अगर missing fields हैं तो केवल वही पूछें। Benefits और documents को सरल Hindi में बताएं। URL हो तो उसे जस का तस रखें।
"""
        return self.brain.generate([{
            "role": "user",
            "content": prompt,
        }])
