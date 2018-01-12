# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import simdem
from simdem.render import demo
from simdem.parser import codeblock,context,simdem1
from simdem.executor import bash