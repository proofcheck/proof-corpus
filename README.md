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





