from string import printable
def replace_line(file_name, line_num, text):
    with open(file_name) as iha:
        oof = iha.readlines()
        oof[line_num] = text
    with open(file_name, "w+") as out:
        out.writelines(oof)

def main(cat, inputo):
    temp = []
    inputo = inputo.replace("\\", "\\\\")
    inputo = inputo.replace("\"", "\"")
    inputo = inputo.replace("\'", "\\\'")
    cat = cat.replace(" ", "_")
    for a in list(inputo):
        if a in printable:
            temp.append(a)
    ques = ''.join([str(elem) for elem in temp])

    with open(f"questions\{cat}.txt", "w") as file:
        file.writelines(ques)