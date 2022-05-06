"""
Reduce the execution and IO priority of this program.
"""

import os
import psutil
import sys


def make_nice():
    """
    Make the process nice.
    """
    pid = os.getpid()
    os.setpriority(os.PRIO_PROCESS, pid, 19)
    p = psutil.Process(pid)
    if hasattr(p, "ionice"):
        p.ionice(psutil.IOPRIO_CLASS_IDLE)
