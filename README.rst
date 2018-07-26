========
pysyslog
========


.. image:: https://img.shields.io/pypi/v/pysyslog.svg
        :target: https://pypi.python.org/pypi/pysyslog

.. image:: https://img.shields.io/travis/ilovetux/pysyslog.svg
        :target: https://travis-ci.org/ilovetux/pysyslog

.. image:: https://readthedocs.org/projects/pysyslog/badge/?version=latest
        :target: https://pysyslog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Fast, efficient and useful syslog collector using TCP and optional TLS


* Free software: GNU General Public License v3
* Documentation: https://pysyslog.readthedocs.io.

Features
--------

* TLS support
* Persistent TCP connections
* Flexible logging configuration (powered by Python's logging module)
* Fast


About
-----

pysyslog is a fast and flexible Syslog-over-TCP collector written in Python
with TLS support.

In order to achieve the speed required, we have made some compromises the most
notable one is that we do not attempt to be compliant with any RFCs. We do not
parse any of the messages nor do we offer any syslog-specific functionality. That
being said, since syslog is just plain-text over a transport we should be
interoperable with most (if not all) syslog clients.

Installation
------------

you can install with::

  $ pip install pysyslog

Usage
-----

To start a local syslog collector (listening on TCP 127.0.0.1:514) you can
issue the following command::

  $ pysyslog

If you want to customize the listening host and port they can be passed as
positional arguments respectively. For instance, if you want to listen on
all available interfaces at port 8000 you can issue the following command::

  $ pysyslog 0.0.0.0 8000

If you want to enable TLS, you must provide the path to the key and cert
(must be in PEM format) you can issue the following command::

  $ pysyslog --cert /path/to/cert.pem --key /path/to/key.pem

If the key and cert are contained within the same file, you must pass that file
path to both the `--key` and `--cert`::

  $ pysyslog --cert /path/to/key-and-cert.pem --key /path/to/key-and-cert.pem

All log messages will be sent to stdout. If you want to customize the
destination, you must provide a logging configuration in json format::

  $ pysyslog --logging-config /path/to/logging.json

And in `logging.json`, something like this would send everything to stdout
and also send everything from 127.0.0.1 to a file `./localhost.log`::

  {
    "version": 1,
    "root": {
        "level": "DEBUG",
        "propagate": true,
        "handlers": ["stdout"]
    },
    "formatters": {
        "brief": {
            "format": "%(asctime)s %(message)s"
        }
    },
    "handlers": {
        "stdout": {
          "class": "logging.StreamHandler",
          "formatter": "brief",
          "level": "DEBUG",
          "stream": "ext://sys.stdout"
        },
        "localhost-file": {
            "class": "logging.FileHandler",
            "formatter": "brief",
            "level": "DEBUG",
            "filename": "./localhost.log",
            "delay": true
        }
    },
    "loggers": {
        "127.0.0.1": {
            "handlers": ["localhost-file"],
            "level": "DEBUG",
            "propagate": true
      }
    }
  }

for more information on the logging configuration format please see
https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema

Architecture
------------

The Python's socketserver module provides the TCP server functionality. When
a client connects, a thread is spawned and the socket will be polled for data.
These connections are not closed after receiving one message, rather we utilize
the streaming capabilities of TCP to keep these connections open so we do not
need to perform our three-way-handshake more than once unless the client closes
the connection.

Once a connection is established each line received will be placed on a queue. The
queue is read by a seperate writer process. Which then submits the message to
the Python logging system through a logger named after the IP Address of the
remote peer. This allows a fine-grained configuration where the output can be
sent to many destinations such as a file, stdout or even another syslog
collector.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
