#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File: parse_TODO.py
TODO card generator for Trello
(C) 2017 Marcos Brito - marbri91@gmail.com
License: MIT License
'''

import argparse
import datetime
import sys
import requests
import json

class Trello_card:
    def __eq__(self, other):
            return self.__dict__ == other.__dict__
    def __init__(self, name = "", desc = "", line = 0, t_id = ""):
        self.name = name;
        self.desc = desc;
        self.line = line;
        self.t_id = t_id;

# Calls Trello API to get the TODO list id
# inputs:   board = String, key = String, token = String
# output:   list_id = String
def list_id_API_request(board, key, token, list_name):
    params_ = {'key': key, 'token': token};
    url = "https://api.trello.com/1/boards/" + board + "/lists";
    response = requests.request("GET", url, params=params_);
    #print(response.text)
    response_json=json.loads(response.text);
    for l in response_json:
        if 'name' in l:
            if l['name']==list_name:
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
def post_card_API_request(list_id, key, token, card):
    params_ = {'key': key, 'token': token,
            'name': card.name, 'desc': card.desc, 'idList': list_id};
    url = "https://api.trello.com/1/cards";
    response = requests.request("POST", url, params=params_);
    card.t_id = response.json()['id']
    print(response.text)

# Clean the input string of blank lines and tabs
# input:    String
# output:   String
def clean_string(string):
    cleaned_string = "\n".join([i.strip() for i in string.split("\n") if i.split()]);
    return(cleaned_string);

# Filter the file and stores the TODO comments separated in
# the todo_list string list.
# input:    o_file = String path, filetype(Optional) = String
# output:   String list
def searchAllCardsOnFile(o_file,filetype = None):
    todo_list = list();
    desc = "";
    card = None;

    ext = {
        'c': '//',
        'py': '#'
    }

    if filetype is None:
        wildcard = ext[o_file.split('.')[1]]
    else:
        wildcard = ext[filetype]

    with open(o_file) as inf:
        for idx, line in enumerate(inf):
            if line.startswith(wildcard + " TODO"):
                card = Trello_card();
                card.line = idx; # Do not like the solution
                # Remove the '// TODO ' part of the line
                card.name = line.split(wildcard + " TODO",1)[1].strip().split(" - ")[0].strip();
                if len(line.split(" - ",1))>1:
                    card.t_id = line.split(" - ",1)[1].strip();
                if card.name == "":
                    card.name = "TODO - " + datetime.datetime.now().strftime("%Y-%m-%d");

            elif card is not None and line.startswith(wildcard):
                    desc = desc + line.split(wildcard,1)[1];
            elif card is not None:
                # Filter the string so it will remove blank lines
                if desc != "":
                    card.desc = clean_string(desc);
                    todo_list.append(card);
                    desc = "";
                card = None;
    return todo_list;

# Do not like this solution
def add_id_TODO_comment(o_file,card):
    with open(o_file, 'r') as f:
        data = f.readlines()

    if card.t_id != "":
        data[card.line] = data[card.line].strip() + " - " + card.t_id + "\n"

    with open(o_file, 'w') as f:
        f.writelines(data);

def main(args_):

    parser = argparse.ArgumentParser(description='Process file to find TODO comments and upload them as cards to the preferred kanban board website')

    p_trello_key = argparse.ArgumentParser(add_help=False)
    p_trello_key.add_argument('key', help = 'Trello developer key')

    p_trello_token = argparse.ArgumentParser(add_help=False)
    p_trello_token.add_argument('token', help = 'Trello developer token')

    p_trello_path = argparse.ArgumentParser(add_help=False)
    p_trello_path.add_argument('fpath', help = 'Source code path')

    sp_trello = parser.add_subparsers()

    p_trello = sp_trello.add_parser('trello',parents = [p_trello_key, p_trello_token])

    parser.add_argument('fpath', help = 'Source code path')
    parser.add_argument('-la','--lang', help = 'The language of the source code')
    parser.add_argument('-wi','--write-card-id', help = 'Writes the card id in the TODO comment after posted', action='store_true')

    p_board_id = argparse.ArgumentParser(add_help=False)
    p_board_id.add_argument('bid', help = 'Trello board id')

    p_board_name = argparse.ArgumentParser(add_help=False)
    p_board_name.add_argument('bname', help = 'Trello board name')

    p_list = argparse.ArgumentParser(add_help=False)
    g_list = p_list.add_mutually_exclusive_group()
    g_list.add_argument('-lid','--list-id', help = 'List id in the selected board instead of the default TODO list')
    g_list.add_argument('-lname','--list-name', help = 'List name in the selected board instead of the default TODO list')

    sp_board = p_trello.add_subparsers(dest = 'board')
    sp_board.required = True
    sp_board.add_parser('with-board-id',parents = [p_board_id,p_list], help = 'Upload the found cards into the board with the id given')
    sp_board.add_parser('with-board-name',parents = [p_board_name,p_list], help = 'Upload the found cards into the first board found with the name given')

    if not len(args_[1:]) > 1:
        parser.parse_args(['-h'])
    else:
        args = parser.parse_args(args_[1:])

    file_path = args.fpath;
    key = args.key;
    token = args.token;
    list_name = args.list_name;
    list_id = args.list_id;

    todo_cards = searchAllCardsOnFile(file_path, filetype = args.lang);
    if hasattr(args, 'bid'):
        board_id = args.bid;

    if hasattr(args, 'bname'):
        board_name = args.bname;
        board_id = board_id_API_request(board_name, key, token);

    if list_id is not None:
        todo_list_id = list_id;
    elif list_name is not None:
        todo_list_id = list_id_API_request(board_id, key, token, list_name);
    else:
        todo_list_id = list_id_API_request(board_id, key, token, 'TODO');

    for idx, card in enumerate(todo_cards):
        if card.t_id == "":
            post_card_API_request(todo_list_id, key, token, card);
            # Write id in TODO comment
            if args.write_card_id == True:
                add_id_TODO_comment(file_path,card);

if __name__ == "__main__":
    main(sys.argv)
