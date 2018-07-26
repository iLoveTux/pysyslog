=====
Usage
=====

Pysyslog is meant to be a command line utility and as such all options are
exposed as command line options, please take a look at the help message
which can be seen by running `pysyslog --help`::

  Usage: pysyslog [OPTIONS] [HOST] [PORT]

    Console script for pysyslog.

  Options:
    -i, --poll-interval FLOAT     Number of seconds to poll for shutdown
    -m, --max-queue-size INTEGER  The number of messages to allow in the queue
    -c, --cert PATH               The PEM formatted public certificate, must
                                  also provide --key
    -k, --key PATH                The PEM formatted private key, must also
                                  provide --cert
    -l, --logging-config TEXT     The JSON formatted file containing the
                                  logging config
    --help                        Show this message and exit.

`HOST` defaults to `127.0.0.1` and specifies the interface to bind to and `PORT`
defaults to `514` and is the port on which to listen.

If you want to run this as a service on Windows, we recommend `NSSM <https://nssm.cc/>`_
alternatively if you want to run this as a service on Linux, a systemd unit file
is probably what you need.
