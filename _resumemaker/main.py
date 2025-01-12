#!/usr/bin/env python3

import json
from operator import itemgetter
import subprocess

AUTHOR_ME = "Toffalini F."
PUB_PLACEHOLDER = "<!-- !!!!PUBLICATIONS!!!!! -->"
PUBLICATION_PAGE = "../_content/publications.html"

def run_make(target):
    subprocess.run(["make", target]) 

def update_cb():
    subprocess.run(["cp", "cv/cv.pdf", "../files/"])

def emit_publications(db):

    pub_list = "<ul>"
    
    new_db = sorted(db, key=lambda x: int(x['date']), reverse=True) 

    for e in new_db:
        p_type = e["type"]
        author_list = get_author_list(e["authors"], True)
        title = e["title"]
        venue = e["venue"].replace("\\&", "&")
        year = e["date"][:4]

        pub_list += "<li>"
        if p_type in ["conference", "workshop"]:
            pub_list += f"{author_list}. ''{title}'' Proceeding of {venue}<br />"
        elif p_type == "journal":
            pub_list += f"{author_list}. ''{title}'' {venue}, {year}<br />"
        pub_list += "</li>"

    pub_list += "</ul>"

    fin = open(PUBLICATION_PAGE, "rt")
    data = ""
    for l in fin:
        if PUB_PLACEHOLDER in l:
            data += PUB_PLACEHOLDER + pub_list + "\n"
        else:
            data += l

    fin.close()
    fin = open(PUBLICATION_PAGE, "wt")
    fin.write(data)
    fin.close()


def get_author_list(author_list_json, is_html = False):
    author_list = []
    for a in author_list_json:
        a_str = " ".join([a[1], a[0][0] + "."])

        if a_str == AUTHOR_ME:
            if is_html:
                author_list += [f"<b>{a_str}</b>"]
            else:
                author_list += [f"\\textbf{{{a_str}}}"]
        else:
            author_list += [a_str]

    return ", ".join(author_list)

def emit_cv(db):

    f = open("cv/publication.tex", "w")

    new_db = sorted(db, key=lambda x: int(x['date']), reverse=True) 

    f.write("\\textbf{Conference}")
    f.write("\\begin{enumerate}[leftmargin=5mm]\n")
    # f.write("\\begin{enumerate}[label={[C\\arabic*]},leftmargin=5mm]\n")
    cnt = len([e for e in new_db  if e["type"] == "conference"])
    for e in new_db:
        if e["type"] != "conference":
            continue
        
        author_list = get_author_list(e["authors"])
        title = e["title"]
        venue = e["venue"]

        f.write(f"\\item[C{cnt}] {author_list}\\\\``{title}'' Proceeding of {venue}\n")
        cnt = cnt - 1

    f.write("\\end{enumerate}\n")

    f.write("\\textbf{Workshop}")
    cnt = len([e for e in new_db  if e["type"] == "workshop"])
    f.write("\\begin{enumerate}[leftmargin=5mm]\n")
    for e in new_db:
        if e["type"] != "workshop":
            continue
        
        author_list = get_author_list(e["authors"])
        title = e["title"]
        venue = e["venue"]

        f.write(f"\\item[W{cnt}] {author_list}\\\\``{title}'' Proceeding of {venue}\n")
        cnt = cnt - 1

    f.write("\\end{enumerate}\n")

    f.write("\\textbf{Journal}")
    cnt = len([e for e in new_db  if e["type"] == "journal"])
    f.write("\\begin{enumerate}[leftmargin=5mm]\n")
    for e in new_db:
        if e["type"] != "journal":
            continue
        
        author_list = get_author_list(e["authors"])
        title = e["title"]
        venue = e["venue"]
        year = e["date"][:4]

        f.write(f"\\item[J{cnt}] {author_list}\\\\``{title}'' {venue}, {year}\n")
        # f.write(f"\\item {author_list}\\\\``{title}'' {venue}, {year}\n")
        cnt = cnt - 1

    f.write("\\end{enumerate}\n")


    f.close()

    run_make("cv_d")

    update_cb()

def __main():

    with open("database.json") as f:
        db = json.load(f)

    print("Emit CV entries")
    emit_cv(db)

    print("Emit publications")
    emit_publications(db)

    print("done")


if __name__ == "__main__":
    __main()