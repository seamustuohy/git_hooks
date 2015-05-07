#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import subprocess
from datetime import datetime


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def now():
    """Current date-time"""
    #return str(datetime.now())[:16]
    return datetime.now().strftime('%Y-%m-%d %H:%M')


if __name__ == '__main__':
    modified = re.compile('^[ACM]+\s+(?P<name>.*\.py)', re.MULTILINE)
    files = modified.findall( system('git', 'status', '--porcelain') )

    for name in files:
        # watching ruby | python | lua scripts
        if re.search(r"(\.py|\.rb|\.lua)$", name):
            # current script text
            with open(name, 'r') as fd: script = fd.read()
            # change modification date
            script = re.sub('(@changed\s*:\s+)\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                            lambda m: m.group(1) + now(), script)
            # change script revision
            script = re.sub('(@revision\s*:\s+)(\d+)',
                            lambda m: m.group(1) + str(int(m.group(2))+1), script)
            # change script version
            script = re.sub('(__version__\s*=\s*\d+\.\d+\.)(\d+)',
                            lambda m: m.group(1) + str(int(m.group(2))+1), script)
            # write back to script
            with open(name, 'w') as fd: fd.write(script)
            # add changes to commit
            system('git', 'add', name)

    sys.exit(0)
