# Natural Language Proof-Checking project - Summer 2022

## Setup

0. On a CS machine, create a personal directory inside `/research/proofcheck`. Clone this repository into that folder.

1. Create a virtual environment `.venv` for this project in the cloned repository:

        cd proof-corpus
        python -m venv .venv
        
   The virtual environment is a "local" version of Python; we can install whatever packages 
   into this environment without affecting any other users.

2. Activate the Python virtual environment by running

        source .venv/bin/activate

    (You will need to re-run this command every time you log in.)

3. Install the necessary packages (listed in `requirements.txt`)

        pip install -r requirements.txt
        
4. Create a symbol link `texes` to the arXiv TeX source files

        ln -s /research/proofcheck/texes texes
        
        
## Extracting Proofs.

1. To test that things are working correctly, we can try extracting a few proofs from `.tex` source. Run

        ./naive.py -m matches/matches2a
        
   This extracts proofs from the files listed in the `matches/matches2a` file and puts the output into corresponding
   subdirectories of the new `proofs` directory.
   
   (The name `naive` comes from the fact that this treats `.tex` source code in a very naive and oversimplified
   fashion, rather than trying to simulate the full behavior of a real TeX system.)

   If you get an error about the `bs4` package not being installed, make sure that you are using the 
   version of python installed in the virtual environment; otherwise, run `source .venv/bin/activate`
   and try again.

2. A different small subset of `.tex` files is in `matches/matches3a`

        ./naive.py -m matches/matches2a
              
3. A different (and 100x bigger) subset of `.tex` files is in `matches/matches08'. This is big enough that it might be worth running many instances of extraction in parallel. To use up to 16 cores, we can run

        time ./naive.py -p16 -m matches/matches08 > log.txt 2>&1

   This takes a while, so wrapping it in the `time` command lets us wander off but 
   see how long it took when we come back later. The `log.txt` file can be examined to see which 
   `.tex` files failed under our naive extraction.
   
4. To do a complete extraction of all the English-language `.tex` files, we can run

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

1. Here's a quick and dirty way to get the proofs from each year into a single file (assuming `zsh` is your shell):

        rm -f proofs*.raw
        foreach y (`seq 92 99` `seq -w 0 20`)
          find proofs/$y* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs$y.raw
        end

   This creates text files `proofs92.raw`, `proofs93.raw`, ..., `proofs20.raw' for the years 1992-2020,
   with one proof per line.

   If you just want to do 2000 or 2008, though

        find proofs/00* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs00.raw

        find proofs/08* -type f -name "*.txt" -print0 | xargs -0 cat >! proofs08.raw
   

2. To run the ad-hoc cleanup script on each of these files (in parallel), we can do 

        rm -f proofs*.txt
        foreach y (`seq 92 99` `seq -w 0 20`)
          ./cleanup.py proofs$y.raw > proofs$y.txt &
        end
        wait

   This creates files `proofs92.txt`, `proofs93.txt`, ..., `proofs20.txt' for the years 1992-2020,
   with one proof per line. (It can take up to an hour, but fortunately `cleanup.py` also nices itself
   so it's OK as a long-running process.)
   
   And if you just want to do 2008,

       time ./cleanup.py proofs00.raw > proofs00.txt

       time ./cleanup.py proofs08.raw > proofs08.txt
   
## Splitting into Sentences

1. There are a couple scripts with different ways of splitting proofs into individual sentences
   (one per line). At the moment, I think sentize2.py does a reasonable job, and processes around 8 or 9 thousand 
   proofs per second.
   
   For one year's (cleaned) proofs:
   
        time ./sentize2.py proofs08.txt > sent08.txt
        
   Or to do all years:
   
        foreach y (`seq 92 99` `seq -w 0 20`)
          ./sentize2.py proofs$y.txt > sent$y.txt &
        end
        wait
   
2. One thing we can do with sentences is to sort them (shuffling parts of different proofs together),
   and then use `uniq` to count how many times each sentence occurs, e.g.,
   
        sort sent08.txt | uniq -c | head -100
        
   so see counts for the first 100 sentences alphabetically.
   
   More interestingly, we can take that output and 
   sort by number of occurrences to find the top-200 most 
   common sentence forms:
   
        sort sent08.txt | uniq -c | sort -rn | head -200
   
        

