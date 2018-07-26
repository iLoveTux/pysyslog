# -*- coding: utf-8 -*-

"""Console script for pysyslog."""
import sys
import json
import click
import logging
import logging.config
from threading import Thread
from multiprocessing import JoinableQueue, Process
from pysyslog import (
    log_writer,
    ThreadedTCPServer,
    QueuedTCPRequestHandler,
)


@click.command()
@click.argument("host", default="127.0.0.1")
@click.argument("port", default=514, type=int)
@click.option("-i", "--poll-interval", default=0.5, type=float)
@click.option("-m", "--max-queue-size", default=50000, type=int)
@click.option("-c", "--cert", type=click.Path(exists=True))
@click.option("-k", "--key", type=click.Path(exists=True))
@click.option("--logging-config", "-l", default=None, type=str)
def main(
        host,
        port,
        poll_interval,
        max_queue_size,
        cert,
        key,
        logging_config,
    ):
    """Console script for pysyslog."""
    if logging_config:
        with open(logging_config, "r") as fin:
            logging.config.dictConfig(json.load(fin))
    else:
        logging.basicConfig(stream=sys.stdout, level=20)
    log = logging.getLogger(__name__)
    q = JoinableQueue(maxsize=max_queue_size)
    writer = Process(target=log_writer, args=(q, logging_config))
    writer.daemon = True
    writer.start()
    log.warn("Listening for syslog over TCP on: {}:{} polling: {}".format(host, port, poll_interval))
    server = ThreadedTCPServer(q, (host, port), QueuedTCPRequestHandler)
    server.daemon_threads = True
    if cert and key:
        server.certfile = cert
        server.keyfile = key
    server.serve_forever(poll_interval=poll_interval)
    server.shutdown()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
