import argparse
import csv
from datetime import date
import os

from misc.common import advisor_dict, department_dict, core_faculty

CURRENT_YEAR = date.today().year


def RecordToLineTuple(record):  # [name, webpage, year, advisors, departments]
    assert (record[0])
    if record[1]:
        line_1 = "<a href=\"{0}\" style=\"text-decoration:none\">{1}</a>".format(record[1], record[0])
    else:
        line_1 = record[0]

    if record[2]:
        line_2 = record[2]
    else:
        line_2 = ""

    if record[3]:
        line_3 = ""
        for i in range(len(record[3])):
            line_3 += ", "
            if record[3][i] in advisor_dict:
                line_3 += advisor_dict[record[3][i]]
            else:
                line_3 += record[3][i]
        line_3 = line_3[2:]  # remove initial comma
    else:
        line_3 = ""

    if record[4]:
        line_4 = ""
        for i in range(len(record[4])):
            line_4 += ", "
            if record[4][i] in department_dict:
                line_4 += department_dict[record[4][i]]
            else:
                line_4 += record[4][i]
        line_4 = line_4[2:]  # remove initial comma
    else:
        line_4 = ""

    return (line_1, line_2, line_3, line_4)


def LineTupleToString(line_tuple):
    string = ""
    string += "<tr>\n"
    string += "   <td>{0}</td>\n".format(line_tuple[0])
    string += "   <td>{0}</td>\n".format(line_tuple[1])
    string += "   <td>{0}</td>\n".format(line_tuple[2])
    string += "   <td>{0}</td>\n".format(line_tuple[3])
    string += "</tr>\n"

    return string


def main(table_path):
    postdocs = []
    phds = []
    alums = []

    # Check if the file has header.
    has_header = False
    if table_path.endswith('.csv') or table_path.endswith('.tsv'):
        with open(table_path, 'r') as csvfile:
            sniffer = csv.Sniffer()
            if sniffer.has_header(csvfile.read(2048)):
                has_header = True

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
            exit_year = elements[4].strip()
            advisors = [a.strip() for a in elements[5].split(',')]
            departments = [a.strip() for a in elements[7].split(',')]

            record = [name, webpage, year, advisors, departments]
            # If one of the advisors is a core faculty.
            if len([cf for cf in core_faculty if cf in advisors]) > 0:
                if "alum" in status or (
                    # exit_year can't be empty, can't be ???, and must be <= this year.
                    len(exit_year) > 0 and exit_year != '???' and int(exit_year) <= CURRENT_YEAR
                ):
                    alums.append(record)
                elif "phd" in status:
                    phds.append(record)
                elif "postdoc" in status:
                    postdocs.append(record)

    postdocs.sort()
    phds.sort()
    alums.sort()

    with open('students_template.html', 'r') as f1:
        with open('students.html', 'w') as f2:
            for line in f1.readlines():
                if line.strip() == '<!--POSTDOC-->':
                    for record in postdocs:
                        f2.write(LineTupleToString(RecordToLineTuple(record)))
                elif line.strip() == '<!--PHD-->':
                    for record in phds:
                        f2.write(LineTupleToString(RecordToLineTuple(record)))
                elif line.strip() == '<!--ALUM-->':
                    for record in alums:
                        f2.write(LineTupleToString(RecordToLineTuple(record)))
                else:
                    f2.write(line)


if __name__ == "__main__":
    # Run this script from the root of the repo:
    # python conversion_script.py
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--table_path', type=str, default=os.path.join('.', 'roster.tsv'),
        help="Path to the table with all the students. "
             "Should be pulled from the roster website to a tab-separated format: "
             "https://docs.google.com/spreadsheets/d/1W9D5NFxOXuzpao7aB6BXTnj5uhyPAJXBj9oLkF7IAnc/edit#gid=0"
    )
    args = parser.parse_args()

    main(table_path=args.table_path)
