"""Check if an input normally comes from texlive."""

# database file was created via the command
#
# egrep '\.sty$|.cls$|\.tex$'
#        /usr/local/texlive/2021/texmf-dist/ls-R > texmf-dist.txt
#

import subprocess

standard_files = set()
with open("texmf-dist.txt") as fd:
    for filename in fd.readlines():
        filename = filename.strip()
        standard_files.add(filename.strip())
        if filename.endswith(".tex"):
            standard_files.add(filename[:-4])


def in_TeX_path(filename: str) -> bool:
    """Check if filename is a standard package."""
    answer1: bool = filename in standard_files
    # try:
    #     subprocess.check_call(  # nosec
    #         ["/Library/TeX/texbin/kpsewhich", filename],
    #         stdout=subprocess.DEVNULL,
    #     )
    #     answer2: bool = True
    # except subprocess.CalledProcessError:
    #     answer2 = False

    # if answer1 != answer2:
    #     print(f"Error: kpsewhich answer mismatch for {filename}")
    #     print(f"texmf-dist.txt: {answer1}")
    #     print(f"kpsewhich:      {answer2}")
    #     exit(-1)

    return answer1


"""
@functools.lru_cache
def in_TeX_path(filename: str) -> bool:
    "Check if filename is a standard package."
    try:
        subprocess.check_call(  # nosec
            ["/Library/TeX/texbin/kpsewhich", filename],
            stdout=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False
"""
