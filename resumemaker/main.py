#!/usr/bin/env python3

import json
from operator import itemgetter
import subprocess

AUTHOR_ME = "Toffalini F."

def run_make(target):
    subprocess.run(["make", target]) 


def get_author_list(author_list_json):
    author_list = []
    for a in author_list_json:
        a_str = " ".join([a[1], a[0][0] + "."])

        if a_str == AUTHOR_ME:
            author_list += [f"\\textbf{{{a_str}}}"]
        else:
            author_list += [a_str]

    return ", ".join(author_list)

def emit_cv(db):

    f = open("cv/publication.tex", "w")

    new_db = sorted(db, key=lambda x: int(x['date']), reverse=True) 

    f.write("\\textbf{Conference}")
    f.write("\\begin{enumerate}[label={[C\\arabic*]},leftmargin=5mm]\n")
    for e in new_db:
        if e["type"] != "conference":
            continue
        
        author_list = get_author_list(e["authors"])
        title = e["title"]
        venue = e["venue"]

        f.write(f"\item {author_list}\\\\``{title}'' Proceeding of {venue}\n")

    f.write("\\end{enumerate}\n")

    f.write("\\textbf{Journal}")
    f.write("\\begin{enumerate}[label={[J\\arabic*]},leftmargin=5mm]\n")
    for e in new_db:
        if e["type"] != "journal":
            continue
        
        author_list = get_author_list(e["authors"])
        title = e["title"]
        venue = e["venue"]
        year = e["date"][:4]

        f.write(f"\item {author_list}\\\\``{title}'' {venue}, {year}\n")

    f.write("\\end{enumerate}\n")


    f.close()

    run_make("cv_d")

def __main():

    with open("database.json") as f:
        db = json.load(f)

    print("Emit CV entries")
    emit_cv(db)

    print("done")


if __name__ == "__main__":
    __main()