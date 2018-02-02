Some useful python scripts for librarians.
To install the scripts, clone the repo and add the `scripts/` directory to your PATH.

## Scripts
### diff_ebooks.py
Compare two lists of eBooks checking for differences and matches.

### datalo.py
Extract all identifiers from a title list and prepare a list for the SFX dataloader.

### csv_to_tsv.py
Convert a CSV file to TSV.

### cleangpr.py
Extract the XML configuration from a GPR file (specific to the software [CAS](http://www.cas-crm.com/)).

### countmedia.py
(Specific to the KLU Library) Count the list of available media divided by category.

## Requirements
**Python 3.6** is required to run the scripts.
External libraries are specified in the file requirements.txt: install them with `pip install -r requirements.txt`.