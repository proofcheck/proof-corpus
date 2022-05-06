# Natural Language Proof-Checking project - Summer 2022

## Setup

0. On a CS machine, create a personal directory inside `/research/proofcheck'. Clone this repository into that folder.

1. Create a virtual environment for this project.  `cd` inside the cloned repository and run

        python -m venv .venv

    to create a Python "virtual environment" in the `.venv` subdirectory.

2. Activate the Python virtual environment by running

        source .venv/bin/activate

    (You will need to re-run this command every time you log in.)

3. Install the necessary packages (listed in `requirements.txt`)

        pip install -r requirements.txt
        
4. Create a symbol link `texes` to the arXiv TeX source files

        ln -s /research/proofcheck/texes texes
        
        
## Extracting Proofs.





