# mttt

Minimalistic timetracking tool



### install

`pip install --user mttt`

`chmod +x ~/.local/lib/python2.7/site-packages/mttt/t.py`

`echo "alias mttt='~/.local/lib/python2.7/site-packages/mttt/t.py'" >> .bashrc`


## commands:

* start

initiate a project / task

* add

create a new task in a project
  If no project name is given, it will use the latest (current) project

example:

`mttt add myproject:"My latest task" `

example:

`mttt add secondtask `



* end

end a Task

example:

`mttt end finished`

* projects

list all projects

* report

Display the project data  

* current

Show current project

* edit

Edit the project data in a text editor

### plain text

Data is stored in simple (per project) text-files in `~/ttprojects` folder  
