from glob import glob
import re


def add_misc(misc, new):
    if misc == "_":
        return new
    else:
        annos = misc.split("|")
        new_key = new.split("=")[0]
        out_annos = [new]
        for anno in annos:
            if anno.startswith(new_key + "="):
                continue
            out_annos.append(anno)
        return "|".join(sorted(out_annos))


files = glob("*.tok")
files += glob("*.conllu")

for file_ in files:
    output = []
    lines = open(file_).read().split("\n")
    for line in lines:
        if "\t" in line:
            fields = line.split("\t")
            if ".tok" in file_:
                if fields[-1] in ["BeginSeg=Yes","Seg=B-Seg"]:
                    fields[-1] = "Seg=B-seg"
                elif fields[-1] == "Seg=B-Conn":
                    fields[-1] = "Conn=B-conn"
                elif fields[-1] == "Seg=I-Conn":
                    fields[-1] = "Conn=I-conn"
                elif fields[-1] == "_":
                    if "pdtb" in file_:
                        fields[-1] = "Conn=O"
                    else:
                        fields[-1] = "Seg=O"
            elif ".conllu" in file_:
                if 'Seg=B-Seg' in fields[-1]:
                    fields[-1] = fields[-1].replace('Seg=B-Seg','Seg=B-seg')
                elif 'Seg=B-Conn' in fields[-1]:
                    fields[-1] = fields[-1].replace('Seg=B-Conn','Conn=B-conn')
                elif 'Seg=I-Conn' in fields[-1]:
                    fields[-1] = fields[-1].replace('Seg=I-Conn','Conn=I-conn')
                elif "Seg=" not in fields[-1]:
                    if "pdtb" in file_:
                        fields[-1] = add_misc(fields[-1],"Conn=O")
                    else:
                        fields[-1] = add_misc(fields[-1],"Seg=O")
            line = "\t".join(fields)
        output.append(line)

    with open(file_,"w") as f:
        f.write("\n".join(output))