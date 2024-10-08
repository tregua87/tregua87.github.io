#!/usr/bin/python3

import os, subprocess

def get_template(content_file):
    with open(content_file) as f:
        l = f.readline()
        if not l.startswith("<!--"):
            return None
        tmp_name = l.replace("<!--","").replace("-->","").strip()

        return tmp_name
    
def get_content(content_file):
    content_text = ""
    with open(content_file) as f:
        content_text = "\n".join(f.readlines())

    return content_text

def __main__():

    # update resume
    subprocess.run(["./main.py"], cwd="_resumemaker")

    content_folder = "_content"
    template_folder = "_template"

    PUB_PLACEHOLDER = "<!-- !!!!CONTENT!!!!! -->"
    
    for c in os.listdir(content_folder):

        content_file = os.path.join(content_folder, c)

        print(c)

        # get correct template
        tmp_name = get_template(content_file)
        content_text = get_content(content_file)

        tmp_file = os.path.join(template_folder, tmp_name)

        fin = open(tmp_file, "rt")
        data = ""
        for l in fin:
            if PUB_PLACEHOLDER in l:
                data += PUB_PLACEHOLDER + content_text + "\n"
            else:
                data += l

        fin.close()
        fin = open(c, "wt")
        fin.write(data)
        fin.close()

        print(tmp_name)




if __name__ == "__main__":
    __main__()