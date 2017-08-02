import sys
import requests

def API_request(board,key,token):
    params_ = {'key': key, 'token': token};
    url = "https://api.trello.com/1/boards/" + board + "/lists";
    response = requests.request("GET", url, params=params_);
    print(response.text)

# Clean the input string of blank lines and tabs
# input:    String
# output:   String
def clean_string(string):
    cleaned_string = "\n".join([i.strip() for i in string.split("\n") if i.split()]);
    return(cleaned_string);

# Filter the file and stores the TODO comments separated in
# the todo_list string list.
# input:    String path
# output:   String list
def filter_file(o_file):
    todo_list = list();
    strg = "";
    with open(o_file) as inf:
        for line in inf:
            if line.startswith("// TODO"):
                # Remove the '// TODO ' part of the line
                strg = line.split("// TODO ",1)[1];
            elif strg != "" and line.startswith("//"):
                    strg = strg + line.split("//",1)[1];
            elif strg != "":
                # Filter the string so it will remove blank lines
                todo_list.append(clean_string(strg));
                strg = "";
    return todo_list;

def main(argv):
    todo_list = filter_file(argv[1]);
    for l in todo_list:
        print(l);

if __name__ == "__main__":
    main(sys.argv)
