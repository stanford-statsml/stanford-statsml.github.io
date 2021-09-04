import argparse
import csv
import os

# @formatter:off
# TODO(lxuechen): Update urls for Emily Fox and Carlos Guestrin once their stanford websites are finalized.
advisor_dict = {
    "John Duchi": "<a href=\"http://stanford.edu/~jduchi/\" style=\"text-decoration:none\">John Duchi</a>",
    "Stefano Ermon": "<a href=\"https://cs.stanford.edu/~ermon/\" style=\"text-decoration:none\">Stefano Ermon</a>",
    "Percy Liang": "<a href=\"https://cs.stanford.edu/~pliang/\" style=\"text-decoration:none\">Percy Liang</a>",
    "Chris Re": "<a href=\"http://cs.stanford.edu/people/chrismre/\" style=\"text-decoration:none\">Chris Re</a>",
    "Greg Valiant": "<a href=\"http://theory.stanford.edu/~valiant/\" style=\"text-decoration:none\">Greg Valiant</a>",
    "Jure Leskovec": "<a href=\"https://cs.stanford.edu/people/jure/\" style=\"text-decoration:none\">Jure Leskovec</a>",
    "Emma Brunskill": "<a href=\"http://www.cs.cmu.edu/~ebrun/\" style=\"text-decoration:none\">Emma Brunskill</a>",
    "Tengyu Ma": "<a href=\"https://ai.stanford.edu/~tengyuma/\" style=\"text-decoration:none\">Tengyu Ma</a>",
    "Chelsea Finn": "<a href=\"http://ai.stanford.edu/~cbfinn/\" style=\"text-decoration:none\">Chelsea Finn</a>",
    "Emily Fox": "<a href=\"https://statistics2.sites.stanford.edu/people/emily-b-fox\" style=\"text-decoration:none\">Emily Fox</a>",
    "Carlos Guestrin": "<a href=\"https://profiles.stanford.edu/carlos-guestrin\" style=\"text-decoration:none\">Carlos Guestrin</a>",
    # "Nick Bambos": "<a href=\"http://web.stanford.edu/~bambos/\" style=\"text-decoration:none\">Nick Bambos</a>",
    # "Serafim Batzoglou": "<a href=\"http://www.serafimb.org/\" style=\"text-decoration:none\">Serafim Batzoglou</a>",
    # "Peter Glynn": "<a href=\"http://web.stanford.edu/~glynn/\" style=\"text-decoration:none\">Peter Glynn</a>",
    # "Moses Charikar": "<a href=\"https://www.cs.princeton.edu/~moses/\" style=\"text-decoration:none\">Moses Charikar</a>",
    # "Chris Manning": "<a href=\"http://nlp.stanford.edu/manning/\" style=\"text-decoration:none\">Chris Manning</a>",
    # "James Zou": "<a href=\"https://profiles.stanford.edu/james-zou\" style=\"text-decoration:none\">James Zou</a>",
    # "Kunle Olukotun": "<a href=\"http://arsenalfc.stanford.edu/kunle\" style=\"text-decoration:none\">Kunle Olukotun</a>",
}

department_dict = {
    "Computer Science": "<a href=\"http://www-cs.stanford.edu\" style=\"text-decoration:none\">Computer Science</a>",
    "Statistics": "<a href=\"https://statistics.stanford.edu\" style=\"text-decoration:none\">Statistics</a>",
    "Electrical Engineering": "<a href=\"https://ee.stanford.edu/\" style=\"text-decoration:none\">Electrical Engineering</a>",
    # "mse": "<a href=\"http://msande.stanford.edu/\" style=\"text-decoration:none\">Management Science & Engineering</a>",
    # "ml": "<a href=\"https://www.ml.cmu.edu//\" style=\"text-decoration:none\">CMU Machine Learning</a>"
}

# @formatter:on

core_faculty = [
    "John Duchi", "Stefano Ermon", "Percy Liang", "Chris Re", "Greg Valiant", "Emma Brunskill", "Tengyu Ma",
    "Chelsea Finn", "Jure Leskovec",
    "Emily Fox", "Carlos Guestrin"
]


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
    if table_path.endswith('.csv'):
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
            advisors = [a.strip() for a in elements[4].split(',')]
            sponsors = [a.strip() for a in elements[5].split(',')]
            departments = [a.strip() for a in elements[6].split(',')]

            record = [name, webpage, year, advisors, departments]
            if len([cf for cf in core_faculty if cf in advisors]) > 0:
                if "alum" in status:
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
        '--table_path', type=str, default=os.path.join('.', 'roster.csv'),
        help="Path to the table with all the students. "
             "Should be pulled from the roster website: "
             "https://docs.google.com/spreadsheets/d/1W9D5NFxOXuzpao7aB6BXTnj5uhyPAJXBj9oLkF7IAnc/edit#gid=0"
    )
    args = parser.parse_args()

    main(table_path=args.table_path)
