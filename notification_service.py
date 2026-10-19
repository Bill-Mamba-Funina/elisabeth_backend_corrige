import logging
from threading import Thread

from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client as TwilioClient


logger = logging.getLogger(__name__)


# ============================================================
# UTILITAIRES
# ============================================================

def _clean_phone_number(number: str) -> str:
    """
    Nettoie un numéro et le convertit en format international.

    Exemple :
        0811996914
        devient
        +243811996914
    """

    value = (
        str(number)
        .strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if value.startswith("whatsapp:"):
        value = value.replace(
            "whatsapp:",
            "",
            1,
        )

    if value.startswith("00"):
        value = "+" + value[2:]

    elif value.startswith("0"):
        value = "+243" + value[1:]

    elif value.startswith("243"):
        value = "+" + value

    elif not value.startswith("+"):
        value = "+" + value

    return value


# ============================================================
# EMAIL
# ============================================================

def _send_email_task(
    subject: str,
    message: str,
    recipient_list: list[str] | None = None,
) -> None:
    """
    Envoie une notification par Gmail.
    """

    try:
        recipients = (
            recipient_list
            or getattr(
                settings,
                "ADMIN_NOTIFICATION_EMAILS",
                [],
            )
        )

        if not recipients:
            logger.warning(
                "Aucun destinataire email configuré."
            )
            return

        from_email = getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            None,
        )

        if not from_email:
            logger.error(
                "DEFAULT_FROM_EMAIL n'est pas configuré."
            )
            return

        app_name = getattr(
            settings,
            "APP_NAME",
            "La Casa da Festa Elisabeth",
        )

        final_subject = (
            f"[{app_name}] {subject}"
        )

        send_mail(
            subject=final_subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
            fail_silently=False,
        )

        logger.info(
            "Notification Gmail envoyée à : %s",
            recipients,
        )

    except Exception as error:
        logger.exception(
            "Erreur envoi Gmail : %s",
            error,
        )


# ============================================================
# WHATSAPP
# ============================================================

def _send_whatsapp_task(
    message: str,
    recipient_numbers: list[str] | None = None,
) -> None:
    """
    Envoie une notification WhatsApp via Twilio.
    """

    account_sid = getattr(
        settings,
        "TWILIO_ACCOUNT_SID",
        None,
    )

    auth_token = getattr(
        settings,
        "TWILIO_AUTH_TOKEN",
        None,
    )

    from_number = getattr(
        settings,
        "TWILIO_WHATSAPP_NUMBER",
        None,
    )

    if not account_sid:
        logger.error(
            "TWILIO_ACCOUNT_SID n'est pas configuré."
        )
        return

    if not auth_token:
        logger.error(
            "TWILIO_AUTH_TOKEN n'est pas configuré."
        )
        return

    if not from_number:
        logger.error(
            "TWILIO_WHATSAPP_NUMBER n'est pas configuré."
        )
        return

    recipients = (
        recipient_numbers
        or getattr(
            settings,
            "ADMIN_NOTIFICATION_WHATSAPP",
            [],
        )
    )

    if not recipients:
        logger.warning(
            "Aucun destinataire WhatsApp configuré."
        )
        return

    try:
        client = TwilioClient(
            account_sid,
            auth_token,
        )

        # Le numéro d'envoi doit être :
        # whatsapp:+xxxxxxxxxxx
        clean_from = str(
            from_number
        ).strip()

        if not clean_from.startswith(
            "whatsapp:"
        ):
            clean_from = (
                "whatsapp:"
                + _clean_phone_number(
                    clean_from
                )
            )

        for number in recipients:

            clean_number = _clean_phone_number(
                number
            )

            to_number = (
                f"whatsapp:{clean_number}"
            )

            logger.info(
                "Tentative WhatsApp : %s -> %s",
                clean_from,
                to_number,
            )

            result = client.messages.create(
                body=message,
                from_=clean_from,
                to=to_number,
            )

            logger.info(
                "WhatsApp envoyé. SID Twilio : %s",
                result.sid,
            )

    except Exception as error:
        logger.exception(
            "Erreur envoi WhatsApp : %s",
            error,
        )


# ============================================================
# NOTIFICATION GLOBALE
# ============================================================

def send_notification(
    subject: str,
    message: str,
    recipient_emails: list[str] | None = None,
    recipient_whatsapp: list[str] | None = None,
    send_email: bool = True,
    send_whatsapp: bool = True,
) -> None:
    """
    Envoie une notification :

    - par Gmail
    - par WhatsApp

    Les deux canaux sont indépendants.
    Une erreur WhatsApp ne bloque pas Gmail.
    Une erreur Gmail ne bloque pas WhatsApp.
    """

    logger.info(
        "Notification : %s",
        subject,
    )

    # ========================================================
    # GMAIL
    # ========================================================

    if send_email:

        email_thread = Thread(
            target=_send_email_task,
            args=(
                subject,
                message,
                recipient_emails,
            ),
            daemon=True,
        )

        email_thread.start()

    # ========================================================
    # WHATSAPP
    # ========================================================

    if send_whatsapp:

        whatsapp_message = (
            f"*{subject}*\n\n"
            f"{message}"
        )

        whatsapp_thread = Thread(
            target=_send_whatsapp_task,
            args=(
                whatsapp_message,
                recipient_whatsapp,
            ),
            daemon=True,
        )

        whatsapp_thread.start()