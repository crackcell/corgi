#!/usr/bin/env python
# -*- encoding: utf-8; indent-tabs-mode: nil -*-
"""
    launcher
    ~~~~~~~~

    Launch workflow.

    :copyright: (c) 2014 Menglong TAN.
"""

import os
import logging

from subprocess import Popen

from hpipe import consts
from hpipe.engine.entity import *
from hpipe.engine.scheduler import *
from hpipe.engine.client import *
from hpipe.engine.filesystem import *

logger = logging.getLogger(__name__)
setup_logger(logger)

class Launcher(object):
    """Launch jobs to hadoop"""

    def __init__(self):
        if os.environ[consts.HPIPE_ENV_SCHEDULER] == "simple":
            self.scheduler = SimpleScheduler()
        else:
            self.scheduler = SimpleScheduler()
        if os.environ[consts.HPIPE_ENV_CLIENT] == "hadoop":
            self.client = HadoopClient()
        else:
            self.client = HadoopClient()
        if os.environ[consts.HPIPE_ENV_FILESYSTEM] == "hdfs":
            self.filesystem = HDFSFilesystem()
        else:
            self.filesystem = HDFSFilesystem()

    def launch(self, tree):
        processes = []

        runnables = []
        self.scheduler.get_runnables(tree, runnables)

        while len(runnables) != 0:
            runnables = self.__preprocess_flags(runnables)

            self.client.launch(runnables)
            # post-process
            self.__postprocess_flags(runnables)

            runnables = []
            self.scheduler.get_runnables(tree, runnables)

    def __preprocess_flags(self, runnables):
        torun = []
        for node in runnables:
            # check DONE
            filename = node.job.properties[consts.HPIPE_OUTPUT_DIR] + ".done"
            if self.filesystem.test(filename, "-e") == 0:
                logger.info("DONE flag found, skip: %s" % filename)
                continue
            # check and remove FAIL
            filename = node.job.properties[consts.HPIPE_OUTPUT_DIR] + ".fail"
            if self.filesystem.test( filename, "-e") == 0:
                logger.info("FAIL flag found, removed: %s" % filename)
                if 0 != self.filesystem.rmr(filename):
                    raise RuntimeError("rmr failed")
                logger.info("remove failed output: %s" %
                            node.job.properties[consts.HPIPE_OUTPUT_DIR])
                self.filesystem.rmr(
                    node.job.properties[consts.HPIPE_OUTPUT_DIR])
            # check BUSY
            filename = node.job.properties[consts.HPIPE_OUTPUT_DIR] + ".busy"
            if self.filesystem.test(filename, "-e") == 0:
                logger.fatal("BUSY flag found: %s" % filename)
                raise RuntimeError("job busy")
            # touch BUSY
            if self.filesystem.touch(filename) != 0:
                logger.fatal("can't touch flag: %s" % filename)
                raise RuntimeError("touch failed")
            torun.append(node)
        return torun

    def __postprocess_flags(self, runnables):
        for node in runnables:
            # remove BUSY
            self.filesystem.rm(node.job.properties[consts.HPIPE_OUTPUT_DIR] + \
                               ".busy")

            # touch DONE or FAIL
            filename = None
            if node.returncode == 0:
                filename = node.job.properties[consts.HPIPE_OUTPUT_DIR] + \
                           ".done"
                node.state = "DONE"
            else:
                filename = node.job.properties[consts.HPIPE_OUTPUT_DIR] + \
                           ".fail"
            logger.debug("touching %s" % filename)
            if 0 != self.filesystem.touch(filename):
                logger.fatal("can't touch flag: %s" % filename)
                raise RuntimeError("touch failed")
