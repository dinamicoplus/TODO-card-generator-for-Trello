# TODO card generator for Trello

This script will parse the source code looking for TODO comments so it can
later be posted in your Trello board. Right now it only processes c-style code.

## Behavior

Every TODO comment in the code processed will generate an individual Trello
card in the TODO list which must exist in the specified board. Each TODO
comment must have the following structure:
```
// TODO [Title of the card]
// [Description of the card]
// [...]
//
```
The title of the card is optional so is the description, but at least one of
them must be filled if it is wanted to be posted. If the title is not given
then the title of the card will be ```TODO - %Y-%m-%d```.

## Usage

In order to get the key and the token to get access to the Trello API REST
you must have a Trello account and give permission following the instructions
in the following link https://trello.com/1/appKey/generate

```
./parser_TODO.py file_path board_id key token
```
For more information about Trello API REST http://developers.trello.com
