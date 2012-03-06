#!/usr/bin/env python
# coding=utf-8

import unittest
import Request

import sys,os
sys.path.insert(0,os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
        ),".."))

suite = unittest.TestSuite()
suite.addTest(Request.suite())

unittest.TextTestRunner(verbosity=2).run(suite)
