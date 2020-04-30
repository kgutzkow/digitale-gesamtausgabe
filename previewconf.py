#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
import subprocess
sys.path.append(os.curdir)
from publishconf import *

result = subprocess.run(['git', 'branch', '--show-current'], encoding='utf-8', capture_output=True)
SITEURL = 'https://gutzkow.uzi.uni-halle.de/preview/{0}'.format(result.stdout.strip())
