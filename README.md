# *TODO* card generator for Trello

This script will parse the source code looking for *TODO* comments so it can
later be posted in your Trello board. Right now it only processes c-style code.

## Behavior

Every *TODO* comment in the code processed will generate an individual Trello
card in the *TODO* list which must exist in the specified board. Each *TODO*
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

An example of a typical usage:

```
python3 parser_TODO.py trello <file_path> <key> <token> with-board-id <id>
```
The previous command will create a Trello card for each *TODO* comment in the
file and will post them in the *TODO* list inside the board with the id given.

In order to get the key and the token to get access to the Trello API REST
you must have a Trello account and give permission following the instructions
in the following link https://trello.com/1/appKey/generate.

For more information about Trello API REST http://developers.trello.com
Use ```python3 parser_TODO.py --help``` to get more information on how to use
this script.

## Changes

**current version: v0.2.0-alpha**

**v0.2.0**

- **BREAKING CHANGE** In general the argument parsing has changed. The first
positional argument now is the desired platform followed by the required
arguments.

**v0.1.0**

- Initial release
