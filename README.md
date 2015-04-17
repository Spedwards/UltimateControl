# Ultimate Control
Version: 1.0.1  
Description: Control Panel for Reddit. Read messages, reply to comments, swap accounts, etc.  
Known Issues: Possible faults on Mac/Linux  
Author: /u/Spedwards

## Requirements
Python 3.0+  
ctypes 1.1.0  
praw 3.0a1

## About
One day I got extremely bored and wanted to build a control panel for Reddit. You can do almost everything you would normally be able to do in the browser.

## Commands
There are quite a few commands (24 + 2 preset shorthands). You can view them all in the control panel with their descriptions by typing `help` or it's shorthand, `?`. Here's a list of all the commands.

 - help
    - help
      - List all the commands
    - help [command]
      - Lists the syntax for the command
 - exit
    - exit
      - Exit Ultimate Control
 - login
    - login
      - Request username and password then log in
    - login [username]
      - Request password then log in
    - login [username] [password]
      - Log into an account
 - unread
    - unread
      - Get all unread messages (requires login)
 - reply
    - reply [id] [m/c]
      - Request message then send (`m` is message, `c` is comment)
    - reply [id] [m/c] [message]
      - Send reply to message/comment
 - user
    - user [me/user] overview
      - Get the user's most recent posts
    - user [me/user] karma
      - Get the user's karma
    - user [me/user] message
      - Request a subject and message then send
    - user [me/user] message [subject]
      - Request message then send
    - user [me/user] message [subject] [message]
      - Send message
    - user available [username]
      - See if username is available
    - user create
      - Request username and password then create new account
    - user create [username]
      - Request password then create new account
    - user create [username] [password]
      - Create new account
 - me
    - me name
      - Get currently logged in username
    - me logged
      - See if someone is logged in
 - shorthand
    - shorthand set [word] [command]
      - Sets a shorthand for a command
    - shorthand rem [word]
      - Removes a shorthand
 - clear
    - clear
      - Clears the window

And the 2 preset shorthands are:

 - ?
   - help
 - cls
   - clear

## Planned Features

 - View subreddit(s)
   - [ ] sidebar
   - [ ] moderators
   - [ ] submit
 - View submission(s)
   - [ ] and comment
   - [ ] get author
