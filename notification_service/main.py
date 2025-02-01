import pika
import sys
import os
import time
import logging
from dotenv import load_dotenv
import email_service

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

if not RABBITMQ_URL:
    logging.error("RABBITMQ_URL is not set. Please check your environment variables.")
    sys.exit(1)

# RabbitMQ connection placeholder for graceful shutdown
connection = None

def main():
    global connection

    # Establish RabbitMQ connection
    try:
        logging.info("Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_URL))
        channel = connection.channel()
        logging.info("Connected to RabbitMQ.")

       

        def callback(ch, method, properties, body):
            try:
                # Process the message using email_service
                logging.info(f"Received message: {body}")
                err = email_service.notification(body)
                if err:
                    logging.warning(f"Message processing failed: {err}. Requeuing...")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                else:
                    logging.info("Message processed successfully.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logging.error(f"Error processing message: {e}", exc_info=True)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel.basic_consume(
            queue="email_notification",
            on_message_callback=callback
        )

        logging.info("Waiting for messages. To exit, press CTRL+C.")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted. Shutting down gracefully...")
        if connection and not connection.is_closed:
            logging.info("Closing RabbitMQ connection...")
            connection.close()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
