# Natural Language Proof-Checking project - Summer 2022

## Setup

### CS Machines

0.  Use `mkdir` to create a personal directory inside `/research/proofcheck`. Clone this repository into that folder.

1.  Create a virtual environment `.venv` for this project in the cloned repository:

         cd proof-corpus
         python -m venv .venv

    The virtual environment is a "local" version of Python; we can install whatever packages
    into this environment without affecting any other users.

2.  Activate the Python virtual environment by running

        source .venv/bin/activate

    (You will need to re-run this command every time you log in.)

3.  Install the necessary packages (listed in `requirements.txt`)

        pip install -r requirements.txt

4.  Create a symbolic link `texes` to the arXiv TeX source files

        ln -s /research/proofcheck/texes texes

### Individual Machines (Mac or Unix)

0.  Chose where you're going to work, and clone the `proof-corpus` repository there.

1.  On a Mac, you may want to go to System Preferences, select the `Spotlight` pane, choose the `Privacy` tab, and the
    newly created proof-corpus directory. We're going to put millions of files here, and the costs of asking the Mac to
    index them all outweighs any benefits.

2.  Make sure you have Python installed (a version >= 3.8)

    If you don't want to pollute your global Python installation, create a virtual environment
    in the cloned repository:

        cd proof-corpus
        python -m venv .venv

    and then run

        source .venv/bin/activate

    now and every time you create a new shell/terminal for working on this project.

3.  Install the necessary packages listed in `requirements.txt` (either globally or in your virtual environment) by running

    pip install -r requirements.txt

4.  Copy the (very large!) `texes` directory. If you have `rsync` installed, you can do

        rsync -arvz knuth:/research/proofcheck/texes texes

    or

        scp -rp knuth:/research/proofcheck/texes texes

    (If for some reason you already downloaded the `texes` folder elsewhere on your computer,
    you can just make `texes` here a symbolic link to that directory.)

## Extracting Proofs.

1.  To test that things are working correctly, we can try extracting a few proofs from `.tex` source. Run

         ./naive.py -m matches/matches2a

    This extracts proofs from the files listed in the `matches/matches2a` file and puts the output into corresponding
    subdirectories of the new `proofs` directory.

    (The name `naive` comes from the fact that this treats `.tex` source code in a very naive and oversimplified
    fashion, rather than trying to simulate the full behavior of a real TeX system.)

    If you get an error about the `bs4` package not being installed, make sure that you are using the
    version of python installed in the virtual environment; otherwise, run `source .venv/bin/activate`
    and try again.

2.  A different small subset of `.tex` files is in `matches/matches3a`

        ./naive.py -m matches/matches2a

3.  A different (and 100x bigger) subset of `.tex` files is in `matches/matches08'. This is big enough that it might be worth running many instances of extraction in parallel. To use up to 16 cores, we can run

         time ./naive.py -p16 -m matches/matches08 > log.txt 2>&1

    This takes a while, so wrapping it in the `time` command lets us wander off but
    see how long it took when we come back later. The `log.txt` file can be examined to see which
    `.tex` files failed under our naive extraction.

4.  To do a complete extraction of all the English-language `.tex` files, we can run

         rm -rf proofs
         time ./naive.py -p30 -m matches/eng-matches > log.txt 2>&1

    This will take hours, so it's best to let this run overnight.

    **Note**: Normally, on a department server, if you're running code for many hours, it's important to mark your
    processes as "low priority"
    so you're not interfering with the work of others. One way to do this would be
    to [use `nice -19` to run the command](https://www.cs.hmc.edu/twiki/bin/view/QREF/LongJobs).
    But we expect to run `naive.py` for long periods of times, so the script
    automatically "nices" itself (using both `nice` to avoid hogging the CPU and `ionice` to avoid hogging the disk,
    and slowing other people's work down).

# Combining and Cleaning Proofs

1.  Here's a quick and dirty way to get the proofs from each year into a single file (assuming `zsh` is your shell):

         rm -f proofs*.raw
         foreach y (`seq 92 99` `seq -w 0 20`)
           find proofs/$y* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs$y.raw
         end

    This creates text files `proofs92.raw`, `proofs93.raw`, ..., `proofs20.raw' for the years 1992-2020,
    with one proof per line.

    If you just want to do 2000 or 2008, though:

         find proofs/00* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs00.raw

    or

         find proofs/08* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs08.raw

2.  To run the ad-hoc cleanup script on each of these files (in parallel), we can do

         rm -f proofs*.txt
         nohup foreach y (`seq 92 99` `seq -w 0 20`); ./cleanup.py -p16 proofs$y.raw > proofs$y.txt; end

    This creates files `proofs92.txt`, `proofs93.txt`, ..., `proofs20.txt' for the years 1992-2020, with one proof per line. (It can take up to an hour, but fortunately `cleanup.py`also nices itself so it's OK as a long-running process. The`nohup` keeps the cleanup running even if you close the terminal window or ssh session.)

    And if you just want to do 2008,

        time ./cleanup.py proofs00.raw > proofs00.txt

    or

        time ./cleanup.py proofs08.raw > proofs08.txt

## Splitting into Sentences

1.  There are a couple scripts with different ways of splitting proofs into individual sentences
    (one per line). At the moment, I think sentize2.py does a reasonable job, and processes around 8 or 9 thousand
    proofs per second.

    For one year's (cleaned) proofs:

         time ./sentize2.py proofs08.txt > sent08.txt

    Or to do all years:

         foreach y (`seq 92 99` `seq -w 0 20`)
           nohup ./sentize2.py proofs$y.txt > sent$y.txt &
         end
         wait

2.  One thing we can do with sentences is to sort them (shuffling parts of different proofs together),
    and then use `uniq` to count how many times each sentence occurs, e.g.

        sent*.txt | uniq -c | sort -rn > all-sentences.txt

    then we can look at, say, the top 100 most common sentences:

        head -100 all-sentences.txt

    or scroll/search the entire file

        less all-sentences.txt

    (you'll want to hit `^C` if `less` starts counting lines. It's not worth the time.)
