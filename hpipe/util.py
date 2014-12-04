#!/usr/bin/env python
# -*- encoding: utf-8; indent-tabs-mode: nil -*-
"""
    util
    ~~~~

    Utilities.

    :copyright: (c) 2014 Menglong TAN.
"""

import os
import sys
import logging

def setup_logger(logger):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s:  %(message)s',
                                  '%y/%m/%d %H:%M:%S')
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(int(os.environ["hpipe_log_level"]))
