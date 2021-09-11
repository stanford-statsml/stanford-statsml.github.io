"""Find people with missing columns.

python -m misc.filter_people --task "find_people_with_no_enter_year"
python -m misc.filter_people --task "find_people_with_no_sponsor"
"""

import argparse
import csv
import os

from .common import core_faculty


def find_people_with_no_enter_year(record, ignore_faculty=True, only_email=True):
    out = [entry for entry in record if len(entry["year"]) == 0]
    if ignore_faculty:
        out = [entry for entry in out if entry["status"] != "faculty"]
    if only_email:
        out = [entry["email"] for entry in out]
    print('people with no enter year:')
    # For easier copy-paste into email.
    for outi in out:
        print(outi)
    return out


def find_people_with_no_sponsor(record, ignore_not_current=True, ignore_faculty=True, only_email=True):
    out = []
    for entry in record:
        # Only check for their sponsor if no advisor is in the core faculty.
        if all(advisor not in core_faculty for advisor in entry["advisors"]):
            if len(entry["sponsors"][0]) > 0:  # There is at least one sponsor.
                continue
            if ignore_faculty:
                if entry["status"] == "faculty":
                    continue
            if ignore_not_current:
                if entry['current'] != 'x':  # Not current.
                    continue
            out.append(entry)
    if only_email:
        out = [entry["email"] for entry in out]
    print('people with no sponsor:')
    # For easier copy-paste into email.
    for outi in out:
        print(outi)
    return out


def table2dicts(table_path):
    """Convert table (in .txt or .csv) to a list of Python dictionaries."""

    # Check if the file has header.
    has_header = False
    if table_path.endswith('.csv') or table_path.endswith('.tsv'):
        with open(table_path, 'r') as csvfile:
            sniffer = csv.Sniffer()
            if sniffer.has_header(csvfile.read(2048)):
                has_header = True

    record = []
    with open(table_path, 'r') as f:
        lines = f.readlines()
        if has_header:
            lines = lines[1:]

        for line in lines:
            elements = line.split('\t')
            name = elements[0].strip()
            webpage = elements[1].strip()
            status = elements[2].strip()
            year = elements[3].strip()
            advisors = [a.strip() for a in elements[4].split(',')]
            sponsors = [a.strip() for a in elements[5].split(',')]
            departments = [a.strip() for a in elements[6].split(',')]
            email = elements[7].strip()
            in_google_group = elements[8].strip()
            current = elements[9].strip()

            record.append(
                dict(
                    name=name,
                    webpage=webpage,
                    status=status,
                    year=year,
                    advisors=advisors,
                    sponsors=sponsors,
                    departments=departments,
                    email=email,
                    in_google_group=in_google_group,
                    current=current,
                )
            )
    return record


def main(task, table_path):
    record = table2dicts(table_path)
    if task == "find_people_with_no_enter_year":
        find_people_with_no_enter_year(record)
    elif task == "find_people_with_no_sponsor":
        find_people_with_no_sponsor(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--table_path', type=str, default=os.path.join('.', 'roster.tsv'),
        help="Path to the table with all the students. "
             "Should be pulled from the roster website to a tab-separated format: "
             "https://docs.google.com/spreadsheets/d/1W9D5NFxOXuzpao7aB6BXTnj5uhyPAJXBj9oLkF7IAnc/edit#gid=0"
    )
    parser.add_argument('--task', type=str,
                        choices=("find_people_with_no_enter_year", "find_people_with_no_sponsor"),
                        required=True)
    args = parser.parse_args()

    main(task=args.task, table_path=args.table_path)
