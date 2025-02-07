from celery import shared_task
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='email_notification_task')
def send_otp(self, email, otp):
    try:
        message = {
            "email": email,
            "subject": "Account Verification OTP",
            "body": f"Your OTP for account verification is: {otp}.\nPlease enter this OTP on the verification page."}
        
        # Instead of using RabbitMQ manually, send this message using Celery’s queue
        logging.info(f"Sending OTP email to Celery queue: {message}")

        return message  # The message will be handled by Celery workers

    except Exception as err:
        logging.error(f"Failed to process email: {err}")
        raise self.retry(exc=err)  # Retry on failure




