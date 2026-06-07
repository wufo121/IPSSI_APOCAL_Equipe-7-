"""
Client OpenAI — génération de quiz via l'API Chat Completions (PAYANT).

[Note pédagogique] Ce client illustre une alternative PAYANTE au modèle local
Ollama : qualité et latence excellentes, mais chaque génération coûte de
l'argent et envoie le cours sur les serveurs d'OpenAI (hors UE → enjeu RGPD,
cf. perturbation J3-bis). En développement, on privilégie Ollama (gratuit,
local). Ce client est pensé pour une FUTURE version « premium » de l'app.

On utilise volontairement `requests` (et non la lib `openai`) : aucune
dépendance supplémentaire, et on voit clairement la requête HTTP brute — plus
pédagogique. Noter la séparation system/user (bonne pratique anti prompt-injection).
"""
import requests
from django.conf import settings

from .base import LLMClient, LLMError
from .quiz_prompt import SYSTEM_PROMPT, build_user_prompt, parse_and_validate_quiz

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class OpenAILLMClient(LLMClient):
    """Client HTTP pour l'API Chat Completions d'OpenAI."""

    def __init__(self) -> None:
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.timeout = settings.LLM_API_TIMEOUT
        if not self.api_key:
            # On échoue tôt et clairement plutôt que de laisser l'API renvoyer un 401 obscur.
            raise LLMError(
                "OPENAI_API_KEY manquante. Renseignez-la dans le .env, ou utilisez "
                "LLM_BACKEND=ollama (gratuit, local) pour le développement."
            )

    def generate_quiz(self, source_text: str, title: str) -> list[dict]:
        raw = self._call_openai(source_text, title)
        return parse_and_validate_quiz(raw)

    # ----- internals -----

    def _call_openai(self, source_text: str, title: str) -> str:
        try:
            response = requests.post(
                OPENAI_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type":  "application/json",
                },
                json={
                    "model": self.model,
                    # Séparation system / user : les consignes sont isolées du
                    # contenu utilisateur (défense de base contre l'injection).
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",   "content": build_user_prompt(source_text, title)},
                    ],
                    # Mode JSON strict : OpenAI garantit une sortie JSON valide.
                    "response_format": {"type": "json_object"},
                    "temperature": 0.4,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMError(f"Appel OpenAI échoué : {exc}") from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise LLMError(f"Réponse OpenAI inattendue : {exc}") from exc
