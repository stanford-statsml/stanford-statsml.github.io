advisor_dict = {"John Duchi": "<a href=\"http://stanford.edu/~jduchi/\" style=\"text-decoration:none\">John Duchi</a>",
                "Stefano Ermon": "<a href=\"https://cs.stanford.edu/~ermon/\" style=\"text-decoration:none\">Stefano Ermon</a>",
                "Percy Liang": "<a href=\"https://cs.stanford.edu/~pliang/\" style=\"text-decoration:none\">Percy Liang</a>",
                "Chris Re": "<a href=\"http://cs.stanford.edu/people/chrismre/\" style=\"text-decoration:none\">Chris Re</a>",
                "Greg Valiant": "<a href=\"http://theory.stanford.edu/~valiant/\" style=\"text-decoration:none\">Greg Valiant</a>",
                "Kunle Olukotun": "<a href=\"http://arsenalfc.stanford.edu/kunle\" style=\"text-decoration:none\">Kunle Olukotun</a>",
                "Jure Leskovec": "<a href=\"https://cs.stanford.edu/people/jure/\" style=\"text-decoration:none\">Jure Leskovec</a>",
                "Nick Bambos": "<a href=\"http://web.stanford.edu/~bambos/\" style=\"text-decoration:none\">Nick Bambos</a>",
                "Serafim Batzoglou": "<a href=\"http://www.serafimb.org/\" style=\"text-decoration:none\">Serafim Batzoglou</a>",
                "Peter Glynn": "<a href=\"http://web.stanford.edu/~glynn/\" style=\"text-decoration:none\">Peter Glynn</a>",
                "Moses Charikar": "<a href=\"https://www.cs.princeton.edu/~moses/\" style=\"text-decoration:none\">Moses Charikar</a>",
                "Chris Manning": "<a href=\"http://nlp.stanford.edu/manning/\" style=\"text-decoration:none\">Chris Manning</a>",
                "James Zou": "<a href=\"https://profiles.stanford.edu/james-zou\" style=\"text-decoration:none\">James Zou</a>",
                "Emma Brunskill": "<a href=\"http://www.cs.cmu.edu/~ebrun/\" style=\"text-decoration:none\">Emma Brunskill</a>",
                }

department_dict = {"cs": "<a href=\"http://www-cs.stanford.edu\" style=\"text-decoration:none\">Computer Science</a>",
                "stats": "<a href=\"https://statistics.stanford.edu\" style=\"text-decoration:none\">Statistics</a>",
                "ee": "<a href=\"https://ee.stanford.edu/\" style=\"text-decoration:none\">Electrical Engineering</a>",
                "mse": "<a href=\"http://msande.stanford.edu/\" style=\"text-decoration:none\">Management Science & Engineering</a>",
                "ml": "<a href=\"https://www.ml.cmu.edu//\" style=\"text-decoration:none\">CMU Machine Learning</a>"
                }


def RecordToLineTuple(record):
    assert(record[0])
    if record[1]:
        line_1 = "<a href=\"{0}\" style=\"text-decoration:none\">{1}</a>".format(record[1], record[0])
    else:
        line_1 = record[0]
        
    if record[2]:
        line_2 = record[2]
    else:
        line_2 = ""
        
    if record[3]:
        line_3 = advisor_dict[record[3][0]]
        for i in range(1, len(record[3])):
            line_3 += ", "
            line_3 += advisor_dict[record[3][i]]
    else:
        line_3 = ""
            
    if record[4]:
        line_4 = department_dict[record[4][0]]
        for i in range(1, len(record[4])):
            line_4 += ", "
            line_4 += department_dict[record[4][i]]
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

postdocs = []
phds = []
alums = []

with open("table.txt") as f:
    for line in f.readlines():
        print(line)
        elements = line.split('\t')
        name = elements[0].strip()
        webpage = elements[1].strip()
        status = elements[2].strip()
        year = elements[3].strip()
        advisors = [a.strip() for a in elements[4].split(',')]
        departments = [a.strip() for a in elements[5].split(',')]
        
        record = [name, webpage, year, advisors, departments]
        assert(status in ["postdoc", "phd", "alum"])
        if status == "postdoc":
            postdocs.append(record)
        elif status == "phd":
            phds.append(record)
        else:
            alums.append(record)
        
postdocs.sort()
phds.sort()
alums.sort()

with open('students_template.html','r') as f1:
    with open('students.html','w') as f2:
        for line in f1.readlines():
            if line=='<!--POSTDOC-->\n':
                for record in postdocs:
                    f2.write(LineTupleToString(RecordToLineTuple(record)))               
            elif line=='<!--PHD-->\n':
                for record in phds:
                    f2.write(LineTupleToString(RecordToLineTuple(record)))
            elif line=='<!--ALUM-->\n':
                for record in alums:
                    f2.write(LineTupleToString(RecordToLineTuple(record)))
            else:
                f2.write(line)
