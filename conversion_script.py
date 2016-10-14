advisor_dict = {"John Duchi": "<a href=\"http://stanford.edu/~jduchi/\">John Duchi</a>",
                "Stefano Ermon": "<a href=\"https://cs.stanford.edu/~ermon/\">Stefano Ermon</a>",
                "Percy Liang": "<a href=\"https://cs.stanford.edu/~pliang/\">Percy Liang</a>",
                "Chris Re": "<a href=\"http://cs.stanford.edu/people/chrismre/\">Chris Re</a>",
                "Greg Valiant": "<a href=\"http://theory.stanford.edu/~valiant/\">Greg Valiant</a>",
                "Kunle Olukotun": "<a href=\"http://arsenalfc.stanford.edu/kunle\">Kunle Olukotun</a>",
                "Jure Leskovec": "<a href=\"https://cs.stanford.edu/people/jure/\">Jure Leskovec</a>",
                "Nick Bambos": "<a href=\"http://web.stanford.edu/~bambos/\">Nick Bambos</a>",
                "Serafim Batzoglou": "<a href=\"http://www.serafimb.org/\">Serafim Batzoglou</a>",
                "Peter Glynn": "<a href=\"http://web.stanford.edu/~glynn/\">Peter Glynn</a>",
                }

department_dict = {"cs": "<a href=\"http://www-cs.stanford.edu\">Computer Science</a>",
                "stats": "<a href=\"https://statistics.stanford.edu\">Statistics</a>",
                "ee": "<a href=\"https://ee.stanford.edu/\">Electrical Engineering</a>",
                "mse": "<a href=\"http://msande.stanford.edu/\">Management Science & Engineering</a>",
                }


def RecordToLineTuple(record):
    assert(record[0])
    if record[1]:
        line_1 = "<a href=\"{0}\">{1}</a>".format(record[1], record[0])
    else:
        line_1 = record[0]
        
    if record[2]:
        line_2 = advisor_dict[record[2][0]]
        for i in range(1, len(record[2])):
            line_2 += ", "
            line_2 += advisor_dict[record[2][i]]
    else:
        line_2 = ""
            
    if record[3]:
        line_3 = department_dict[record[3][0]]
        for i in range(1, len(record[3])):
            line_3 += ", "
            line_3 += department_dict[record[3][i]]
    else:
        line_3 = ""    
    
    return (line_1, line_2, line_3)
    
def PrintLineTuple(line_tuple):
    print("            <tr>")
    print("              <td>{0}</td>".format(line_tuple[0]))
    print("              <td>{0}</td>".format(line_tuple[1]))
    print("              <td>{0}</td>".format(line_tuple[2]))
    print("            </tr>")

postdocs = []
phds = []

with open("table.txt") as f:
    for line in f.readlines():
        print(line)
        elements = line.split('\t')
        name = elements[0].strip()
        webpage = elements[1].strip()
        status = elements[2].strip()
        advisors = [a.strip() for a in elements[3].split(',')]
        departments = [a.strip() for a in elements[4].split(',')]
        
        record = [name, webpage, advisors, departments]
        assert(status in ["postdoc", "phd"])
        if status == "postdoc":
            postdocs.append(record)
        else:
            phds.append(record)
        
postdocs.sort()
phds.sort()

print("POSTDOCS")
print("")
for record in postdocs:
    PrintLineTuple(RecordToLineTuple(record))
print("")
print("")
print("")
print("PHDS")
print("")
for record in phds:
    PrintLineTuple(RecordToLineTuple(record))

