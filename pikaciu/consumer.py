# -*- coding: utf-8 -*-
import pika
import time
import os

def call_back(ch, method, properties, body):
    """
    Create a function which is called on incoming message
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    print("Message received:")
    print(body)
    time.sleep(2)


def _run_as_standalone_script():
    """Runs program as standalone script."""
    url = os.environ.get("url")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)  # connect to AMQP
    channel = connection.channel()  # start channel
    channel.queue_declare(queue="pdf_process")  # declare queue

    # set up subscription on the queue
    channel.basic_consume(call_back, queue="pdf_process", no_ack=True)

    # start consuming (blocks)
    channel.start_consuming()
    channel.close()

if __name__ == '__main__':
    _run_as_standalone_script()