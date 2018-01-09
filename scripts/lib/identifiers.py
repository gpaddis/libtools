import isbnlib


def extract_isbns(row):
    "Extract all canonical isbns from a row in the CSV file."
    all_isbns = []
    for field in row:
        isbns = isbnlib.get_isbnlike(field)
        for isbn in isbns:
            all_isbns.append(isbnlib.canonical(isbn))

    return list(set(all_isbns))  # Deduplicate the ISBNs
