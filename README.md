Unpack all files to the same directory, 
currently I have not written an installer for the command line version
Tested on linux

For graphing:
run pip install plotly --upgrade

Assumptions

-No filetypes should be excluded from the search

-Ordering of map results is arbitrary

-arbitrary input is allowed for both keyword and folder name

-The three modules should be loosely coupled
so there are some validations i.e. the flags for dirWalk 
that are meant to prevent improper use of the module