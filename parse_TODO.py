import sys

# Filter the file and stores the TODO comments separated in
# the todo_list string list.
def main(argv):

    todo_list = list();
    strg = "";
    with open(argv[1]) as inf:
        for line in inf:
            if line.startswith("// TODO"):
                # Remove the '// TODO ' part of the line
                strg = line.split("// TODO ",1)[1];
            elif strg != "" and line.startswith("//"):
                    strg = strg + line.split("//",1)[1];
            elif strg != "":
                # Filter the string so it will remove blank lines
                todo_list.append("\n".join([i for i in strg.split("\n") if i.split()]));
                strg = "";
    for l in todo_list:
        print(l);

if __name__ == "__main__":
    main(sys.argv)
