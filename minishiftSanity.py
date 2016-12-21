#!/usr/bin/python

from avocado import Test
from avocado.utils import process
import os, re, pexpect, platform, sys

class minishiftSanity(Test):
    def test_ms_start(self):
        cmd = "minishift start"
        self.log.info("Starting minishift...")
        child = pexpect.spawn(cmd)
        index = child.expect(["The server is accessible via web console at:", pexpect.EOF, pexpect.TIMEOUT], timeout=120)
        if index==0:
            self.log.info("Minishift start finished, OpenShift is started")
        else:
            self.fail("Minishift start failed")

    def test_ms_stop(self):
        cmd = "minishift stop"
        self.log.info("Stopping minishift...")
        child = pexpect.spawn(cmd)
        index = child.expect(["Machine stopped.", pexpect.EOF, pexpect.TIMEOUT], timeout=60)
        if index==0:
            self.log.info("Machine stopped.")
        else:
            self.fail("Error while stopping the machine")
            
    def test_ms_delete_existing(self):
        self.log.info("Trying to delete existing machine...")
	cmd = "minishift delete"
	child = pexpect.spawn(cmd)
	index = child.expect(["Machine deleted", "Host does not exist", pexpect.EOF, pexpect.TIMEOUT],timeout=60)
	if index==0:
            self.log.info("Machine deleted.")
        else:
            self.fail("Delete attempt failed.")

    def test_ms_repetetive_use(self):
        self.log.info("Testing repetetive use of minishifrt (start-stop-start...)")
        for x in range(10):
            self.test_ms_start()
            self.test_ms_stop()
            self.log.info("Start-stop of machine OK - run number: " + str(x))
