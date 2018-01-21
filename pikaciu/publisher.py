# -*- coding: utf-8 -*-


import logging
import sys

import pika

logging.basicConfig()


def pass_message(channel, message):
    if sys.argv[1]:
        channel.basic_publish(exchange="", routing_key="pdf_process", body=str(message))
    else:
        channel.basic_publish(exchange="", routing_key="pdf_process", body="Sent from python script ;)")


def _run_as_standalone_script():
    """Runs program as standalone script."""

    try:
        url = "amqp://iqsipgjs:-GFw6o-wd2WQRZ3KmBA7RTx4rDOVcZs_@termite.rmq.cloudamqp.com/iqsipgjs"
        params = pika.URLParameters(url)
        params.socket_timeout = 5

        connection = pika.BlockingConnection(params)  # connect to AMQP
        channel = connection.channel()  # start channel

        channel.queue_declare(queue="pdf_process")  # declare queue

        # send message
        pass_message(channel, sys.argv[1])

    finally:
        connection.close()


if __name__ == '__main__':
    _run_as_standalone_script()
