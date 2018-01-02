# -*- coding: utf-8 -*-

import os
import sys

import simdem
from simdem.executor import bash
from simdem.parser import codeblock, context
from simdem.render import demo

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
