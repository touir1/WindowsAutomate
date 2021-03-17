# WindowsAutomate

This project is a python tool to create an automate
that is run using a script file. This is meant
to execute simple tasks like clicking with the mouse
and some complex tasks like finding a subimage 
in the screen

## ideas for the project:

- read config from a file
- having a standard format for the file
- \$a is a variable named a
- $a 5 is a variable a with value 5
- click 5,10 is executing the function click 
  with params x=5 and y=10
- $pos find-image 'path' is executing a function 
  find-image that takes a path of an image and 
  returns an object $pos(x,y)