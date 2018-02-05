import isbnlib


def extract_isbns(fields_list):
    "Extract all canonical isbns from a list of fields."
    all_isbns = [isbnlib.get_isbnlike(field) for field in fields_list]
    canonical_isbns = [isbnlib.canonical(str(isbn)) for isbn in all_isbns if isbn != []]
    return list(set(canonical_isbns))  # Deduplicate the ISBNs
