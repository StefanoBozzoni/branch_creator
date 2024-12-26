This python program helps to create git branches from task number and description.
It uses tkInter as Graphical user interface and is designed to work with git and it can be used togheter with a chrome extension to get automatically task names and numbers from service now.
It can be easily adapted to work with other dev ops tools since it does grab data directly from the web page of the task.

#to start the application  
in the command terminal issue that commands  

pip install pyperclip  
python main.py  
  
before you start the program be sure to modify the first two line of the main.py file:  
BETTING_FOLDER = <the folder to the betting app that contains the git repository>  
USERNAME = <your user name>  
  
once the program starts you can enter the values of this edit fields:  
SN number is the task number like BUGT0012833 or STRY0012003  
the description is a bried description of the task  
then press "create branch name" button to create the branch name  
press create branch to create the branch in git and checkout it  
  
the "get from clipboard" button can be used in conjuction with the chrome extension so to populate the fields automatically if before you have used the chrome extension to copy the data to the clipboard.  
  
See further instructions.  