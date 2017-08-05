#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File: parse_TODO.py
TODO card generator for Trello
(C) 2017 Marcos Brito - marbri91@gmail.com
License: MIT License
'''

import datetime
import sys
import requests
import json

class Trello_card:
    def __init__(self,name = "",desc = ""):
        self.name = name;
        self.desc = desc;

# Calls Trello API to get the TODO list id
# inputs:   board = String, key = String, token = String
# output:   list_id = String
def list_id_API_request(board, key, token):
    params_ = {'key': key, 'token': token};
    url = "https://api.trello.com/1/boards/" + board + "/lists";
    response = requests.request("GET", url, params=params_);
    #print(response.text)
    response_json=json.loads(response.text);
    for l in response_json:
        if 'name' in l:
            if l['name']=='TODO':
                list_id=l['id'];
    return list_id;

# Calls Trello API to search for a board id thru its name
# inputs:   name = String, key = String, token = String
# output:   board_id = String
def board_id_API_request(name, key, token):
    params_ = {'key': key, 'token': token,
            'query': name, 'board_fields': 'name'};
    url = "https://api.trello.com/1/search"
    response = requests.request("GET", url, params=params_);
    response_json=json.loads(response.text);
    if 'boards' in response_json:
        for board in response_json['boards']:
            board_id = board['id'];
    return board_id;

# Calls Trello API to post a card in the TODO list
# inputs:   list_id = String, key = String, token = String
#           name = String, desc(Optional) = String
def post_card_API_request(list_id, key, token, name, desc=""):
    params_ = {'key': key, 'token': token,
            'name': name, 'desc': desc, 'idList': list_id};
    url = "https://api.trello.com/1/cards";
    response = requests.request("POST", url, params=params_);
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
    desc = "";
    card = None;
    with open(o_file) as inf:
        for line in inf:
            if line.startswith("// TODO"):
                card = Trello_card();
                # Remove the '// TODO ' part of the line
                card.name = line.split("// TODO ",1)[1].strip();
                if card.name == "":
                    card.name = "TODO - " + datetime.datetime.now().strftime("%Y-%m-%d");

            elif card != None and line.startswith("//"):
                    desc = desc + line.split("//",1)[1];
            elif card != None:
                # Filter the string so it will remove blank lines
                card.desc = clean_string(desc);
                todo_list.append(card);
                desc = "";
                card = None;
    return todo_list;

def main(argv):
    file_path = argv[1];
    board_id = argv[2];
    key = argv[3];
    token = argv[4];

    todo_cards = filter_file(file_path);
    todo_list_id = list_id_API_request(board_id,key,token);

    for idx, card in enumerate(todo_cards):
        post_card_API_request(todo_list_id, key, token, card.name, desc = card.desc);

if __name__ == "__main__":
    main(sys.argv)
