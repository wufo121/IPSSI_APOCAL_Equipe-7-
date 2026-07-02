"""
Endpoints d'authentification (Lot 3 : email-identifiant + validation + reset).

    POST /api/accounts/signup/                  — créer un compte (par email)
    POST /api/accounts/login/                   — se connecter (par email) -> token
    POST /api/accounts/logout/                  — se déconnecter
    GET  /api/accounts/me/                       — utilisateur courant (+ email_verified)
    POST /api/accounts/verify-email/             — confirmer l'email (token du lien)
    POST /api/accounts/resend-verification/      — renvoyer l'email de validation
    POST /api/accounts/password-reset/           — demander un reset (envoie un email)
    POST /api/accounts/password-reset/confirm/   — définir le nouveau mot de passe
"""

import csv
import io
import json
import logging
from datetime import timezone

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone as django_timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import EmailError, send_password_reset_email, send_verification_email
from .models import DataRequest, get_or_create_profile
from .serializers import (
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileUpdateSerializer,
    SignupSerializer,
    UserSerializer,
)
from .tokens import read_email_verify_token, read_password_reset_tokens

logger = logging.getLogger(__name__)


class SignupView(APIView):
    """Inscription par email. Envoie l'email de validation (best-effort)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(request=SignupSerializer, responses={201: UserSerializer})
    def post(self, request):
        # Lot 8 : l'admin peut fermer les inscriptions depuis l'interface.
        from administration.models import SiteConfig

        if not SiteConfig.load().allow_signups:
            return Response(
                {"detail": "Les inscriptions sont actuellement fermées."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Validation SOFT : on tente d'envoyer l'email de confirmation, mais on
        # NE bloque PAS l'inscription si l'envoi échoue (clé Brevo expirée, etc.).
        try:
            send_verification_email(user)
        except EmailError as exc:
            logger.warning("Email de validation non envoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Connexion par email + mot de passe. Renvoie un token DRF + crée la session."""

    permission_classes = [AllowAny]
    # Endpoint PUBLIC (pré-auth) : on désactive l'authentification de requête.
    # Sinon DRF SessionAuthentication, dès qu'un cookie `sessionid` résiduel est
    # présent (posé par django_login au login précédent), impose un contrôle CSRF
    # et rejette l'appel : « CSRF Failed: CSRF token missing ». Le frontend
    # s'authentifie par token, pas par session — il n'envoie pas de jeton CSRF.
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer, responses={200: OpenApiResponse(description="{ token, user }")}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)
        django_login(request, user)  # session utile pour la Swagger UI
        return Response({"token": token.key, "user": UserSerializer(user).data})


class LogoutView(APIView):
    """Déconnexion : invalide le token + détruit la session."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={204: OpenApiResponse(description="Déconnexion réussie")})
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """Renvoie l'utilisateur connecté (avec email_verified pour le bandeau front)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class VerifyEmailView(APIView):
    """Confirme l'adresse email à partir du token reçu par email."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=EmailVerifySerializer,
        responses={200: OpenApiResponse(description="Email confirmé")},
    )
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = read_email_verify_token(serializer.validated_data["token"])
        if uid is None:
            return Response(
                {"detail": "Lien de validation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur introuvable."}, status=status.HTTP_400_BAD_REQUEST
            )

        profile = get_or_create_profile(user)
        profile.email_verified = True
        profile.save(update_fields=["email_verified"])
        return Response({"detail": "Adresse email confirmée avec succès."})


class ResendVerificationView(APIView):
    """Renvoie l'email de validation à l'utilisateur connecté."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiResponse(description="Email renvoyé")})
    def post(self, request):
        if get_or_create_profile(request.user).email_verified:
            return Response({"detail": "Votre email est déjà confirmé."})
        try:
            send_verification_email(request.user)
        except EmailError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"detail": "Email de validation renvoyé."})


class PasswordResetRequestView(APIView):
    """Demande de réinitialisation : envoie un email avec un lien (si le compte existe)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Email envoyé si le compte existe")},
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()

        user = User.objects.filter(email__iexact=email).first()
        if user is not None:
            try:
                send_password_reset_email(user)
            except EmailError as exc:
                logger.warning("Email de reset non envoyé pour %s : %s", email, exc)

        # Anti-énumération : réponse IDENTIQUE que le compte existe ou non
        # (on ne révèle pas quels emails sont enregistrés).
        return Response(
            {
                "detail": "Si un compte existe pour cet email, un lien "
                "de réinitialisation vient d'être envoyé."
            }
        )


class PasswordResetConfirmView(APIView):
    """Définit le nouveau mot de passe à partir du lien (uid + token)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Mot de passe réinitialisé")},
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = read_password_reset_tokens(
            serializer.validated_data["uid"], serializer.validated_data["token"]
        )
        if user is None:
            return Response(
                {"detail": "Lien de réinitialisation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Mot de passe réinitialisé. Vous pouvez vous connecter."})


# ---------------------------------------------------------------------------
# Gestion du profil (Lot 4)
# ---------------------------------------------------------------------------


class ProfileView(APIView):
    """Profil de l'utilisateur connecté : consulter, modifier, supprimer.

    GET    /api/accounts/profile/  — lire son profil
    PATCH  /api/accounts/profile/  — modifier prénom / nom / email
    DELETE /api/accounts/profile/  — supprimer définitivement son compte
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(request=ProfileUpdateSerializer, responses={200: UserSerializer})
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Si l'email a changé, on (re)envoie un email de validation (best-effort,
        # validation SOFT : on ne bloque pas si l'envoi échoue).
        if getattr(user, "_email_changed", False):
            try:
                send_verification_email(user)
            except EmailError as exc:
                logger.warning("Email de validation non renvoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data)

    @extend_schema(
        request=DeleteAccountSerializer,
        responses={204: OpenApiResponse(description="Compte supprimé")},
    )
    def delete(self, request):
        # Suppression DURE (hard delete) : confirmée par le mot de passe.
        # [TODO J3-bis RGPD] Avant de supprimer, proposer un export des données
        #   personnelles (droit à la portabilité). Voir Lot futur "export RGPD".
        serializer = DeleteAccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        Token.objects.filter(user=user).delete()  # invalide le token courant
        django_logout(request)
        user.delete()  # supprime aussi le Profile (on_delete=CASCADE)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    """Changement de mot de passe (en étant connecté, avec l'ancien mot de passe)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Mot de passe modifié")},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        # Changer le mot de passe invalide les tokens DRF existants : on en
        # régénère un pour que l'utilisateur reste connecté sans avoir à se
        # reconnecter manuellement.
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({"detail": "Mot de passe modifié.", "token": token.key})


# ---------------------------------------------------------------------------
# Export RGPD (J3-bis — Art. 15 & 20)
# ---------------------------------------------------------------------------


def _build_export_payload(user) -> dict:
    """Construit le dictionnaire complet des données personnelles d'un utilisateur.

    Filtrage strict par user : aucune donnée d'un autre compte ne peut fuir.
    """
    from quizzes.models import Question, Quiz

    profile = get_or_create_profile(user)

    quizzes_data = []
    for quiz in Quiz.objects.filter(user=user).prefetch_related("questions"):
        quizzes_data.append(
            {
                "id": quiz.id,
                "title": quiz.title,
                "source_text": quiz.source_text,
                "score": quiz.score,
                "created_at": quiz.created_at.isoformat(),
                "updated_at": quiz.updated_at.isoformat(),
                "questions": [
                    {
                        "index": q.index,
                        "prompt": q.prompt,
                        "options": q.options,
                        "correct_index": q.correct_index,
                        "selected_index": q.selected_index,
                    }
                    for q in quiz.questions.all()
                ],
            }
        )

    sar_logs = [
        {
            "requested_at": dr.requested_at.isoformat(),
            "status": dr.status,
            "responded_at": dr.responded_at.isoformat() if dr.responded_at else None,
            "export_hash": dr.export_hash,
        }
        for dr in DataRequest.objects.filter(user=user)
    ]

    return {
        "export_date": django_timezone.now().isoformat(),
        "rgpd_basis": "Art. 15 & 20 RGPD — droit d'accès et portabilité",
        "account": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "email_verified": profile.email_verified,
            "profile_created_at": profile.created_at.isoformat(),
        },
        "quizzes": quizzes_data,
        "signalements": [],
        "sar_audit_trail": sar_logs,
    }


class ExportMyDataView(APIView):
    """Export RGPD Art. 15 & 20 — renvoie toutes les données personnelles de l'utilisateur.

    GET /api/accounts/me/export/          → JSON (défaut)
    GET /api/accounts/me/export/?format=csv → CSV (une ligne par quiz)
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OpenApiResponse(description="Export RGPD (JSON ou CSV)")}
    )
    def get(self, request):
        user = request.user
        fmt = request.query_params.get("format", "json").lower()

        payload = _build_export_payload(user)
        json_bytes = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")

        # Audit trail : on enregistre la demande et on la marque immédiatement répondue.
        dr = DataRequest.objects.create(
            user=user,
            status=DataRequest.STATUS_COMPLETED,
            responded_at=django_timezone.now(),
            export_hash=DataRequest.compute_hash(json_bytes),
        )

        timestamp = django_timezone.now().strftime("%Y%m%d_%H%M%S")

        if fmt == "csv":
            return self._csv_response(payload, timestamp)

        response = HttpResponse(json_bytes, content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="export_rgpd_{timestamp}.json"'
        )
        return response

    @staticmethod
    def _csv_response(payload: dict, timestamp: str) -> HttpResponse:
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["# Export RGPD EduTutor IA", f"date={payload['export_date']}"])
        writer.writerow([])

        # Compte
        writer.writerow(["=== COMPTE ==="])
        acc = payload["account"]
        writer.writerow(["id", "email", "prénom", "nom", "date_inscription", "email_vérifié"])
        writer.writerow([
            acc["id"], acc["email"], acc["first_name"], acc["last_name"],
            acc["date_joined"], acc["email_verified"],
        ])
        writer.writerow([])

        # Quizz
        writer.writerow(["=== QUIZZ ==="])
        writer.writerow(["quiz_id", "titre", "score", "créé_le", "question_index",
                         "énoncé", "options", "bonne_réponse", "réponse_donnée"])
        for quiz in payload["quizzes"]:
            if not quiz["questions"]:
                writer.writerow([quiz["id"], quiz["title"], quiz["score"],
                                 quiz["created_at"], "", "", "", "", ""])
            for q in quiz["questions"]:
                writer.writerow([
                    quiz["id"], quiz["title"], quiz["score"], quiz["created_at"],
                    q["index"], q["prompt"], "|".join(q["options"]),
                    q["correct_index"], q["selected_index"],
                ])
        writer.writerow([])

        # SAR
        writer.writerow(["=== HISTORIQUE DES DEMANDES D'ACCÈS (SAR) ==="])
        writer.writerow(["demandé_le", "statut", "répondu_le", "hash_export"])
        for sar in payload["sar_audit_trail"]:
            writer.writerow([sar["requested_at"], sar["status"],
                             sar["responded_at"], sar["export_hash"]])

        csv_bytes = output.getvalue().encode("utf-8-sig")  # BOM pour Excel
        response = HttpResponse(csv_bytes, content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = (
            f'attachment; filename="export_rgpd_{timestamp}.csv"'
        )
        return response
