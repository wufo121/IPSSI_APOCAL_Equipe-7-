"""
Factory de client LLM selon settings.LLM_BACKEND.

[Note pédagogique] Le « factory pattern » centralise le choix du fournisseur.
Le reste de l'application (views, services) appelle simplement get_llm_client()
sans savoir si c'est Ollama, OpenAI, Claude ou le mock derrière. Pour ajouter
un nouveau fournisseur : écrire un client qui respecte LLMClient, puis l'ajouter
ici. Rien d'autre à changer dans le code métier.
"""
import logging

from django.conf import settings

from .anthropic_client import AnthropicLLMClient
from .base import LLMClient
from .mock_client import MockLLMClient
from .ollama_client import OllamaLLMClient
from .openai_client import OpenAILLMClient

logger = logging.getLogger(__name__)

# Fournisseurs PAYANTS (clé API + facturation à l'usage + données hors UE).
# En développement pédagogique, on reste sur Ollama (gratuit, local).
PAID_BACKENDS = {"openai", "anthropic"}

_BACKENDS = {
    "mock":      MockLLMClient,
    "ollama":    OllamaLLMClient,
    "openai":    OpenAILLMClient,
    "anthropic": AnthropicLLMClient,
}


def get_llm_client() -> LLMClient:
    """Renvoie le client LLM correspondant à la configuration courante."""
    backend = (settings.LLM_BACKEND or "ollama").lower()

    if backend in PAID_BACKENDS:
        # Garde-fou pédagogique : on rappelle (dans les logs) que ce backend
        # est payant. On NE bloque PAS — c'est un choix assumé via le .env.
        logger.warning(
            "[LLM] Backend PAYANT activé : '%s'. En développement, préférez "
            "LLM_BACKEND=ollama (gratuit, local). Les API payantes (OpenAI/Claude) "
            "sont prévues pour une future version premium de l'application.",
            backend,
        )

    client_cls = _BACKENDS.get(backend)
    if client_cls is None:
        raise ValueError(
            f"LLM_BACKEND inconnu : '{backend}'. "
            "Valeurs autorisées : 'ollama' | 'openai' | 'anthropic' | 'mock'."
        )
    return client_cls()
