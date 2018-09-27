#!/usr/bin/python
from __future__ import print_function
import sys
import os
import argparse

from datetime import datetime
import subprocess


EDITOR = '/bin/nano'

class Tt():

  def __init__(self,*args, **kwargs):
    self.ttprojects = str(os.environ['HOME']) + '/ttprojects' 
    if not os.path.exists(self.ttprojects):
        os.makedirs(self.ttprojects)
    projectfiles = [os.path.join(self.ttprojects,basename) for basename in os.listdir(self.ttprojects)]
    if projectfiles:
        self.latest = max(projectfiles, key=os.path.getctime).rpartition('/')[-1]

    self.action = args[0]['action']
    self.data  = args[0]['data']

    if self.action == "projects" :
        for project in os.listdir(self.ttprojects):
            print(project)
        exit()

    if self.action == "report":
        f = open(os.path.join(self.ttprojects,self.latest))
        for line in f.readlines():
            sys.stdout.write(line)
        exit()

    if self.action == "current":
        print("Current project: " + self.latest)
        f = open(os.path.join(self.ttprojects, self.latest), 'r') 
        try: print(f.readlines()[-1]) 
        except: pass
        exit()


    if self.data:

        if ':' in self.data:
            self.project = self.data.split(':')[0]
            self.content = self.data.split(':')[1]

        else:
            self.content= self.data
            if hasattr(self,'latest') :
                self.project = self.latest
            else:
                try:
                    project = input("Project name: ({})".format(self.latest))
                except:
                    project = input("New Project name: ")
                self.project = project
            if self.action == "start":
                self.project = self.data

    else:
        self.project = self.latest
        self.content = ''

    self.file = open(os.path.join(self.ttprojects, self.project), "a")

    now = datetime.now()
    self.nowstr = "{}:{} {}-{}-{} ".format(now.hour, now.minute, now.day, now.month, now.year) 


  def run(self):
   action =  getattr(self, self.action)
   return action()


  def start(self):
    self.file.write("{} {} {}\n".format( self.nowstr, "> ", self.content ))

  def add(self):
    
    self.file.write("{} {} {}\n".format( self.nowstr,"+ ", self.content ))

  def end(self):
    self.file.write("{} {} {} \n".format( self.nowstr, "< ", self.content if not None else "...end"))


  def edit(self):
    if self.data:
        subprocess.check_call([EDITOR, os.path.join(self.ttprojects, self.data)])           
        exit()
    if self.project:
        subprocess.check_call([EDITOR, os.path.join(self.ttprojects, self.project)])           
        exit()

    print("no projects yet. To create a project: start project:task  ")    

  def switch(self):
    if self.data:
       open(os.path.join(self.ttprojects, self.data), 'a').close()
       print("current: {}".format(self.data))
       f = open(os.path.join(self.ttprojects, self.data), 'r') 
       try: 
            print(f.readlines()[-2])
            print(f.readlines()[-1])
       except: pass
       f.close()      

if __name__ == '__main__':

    parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter,
             description=  'Minimalist command-line time tracking application.')
    parser.add_argument( 'action' , type=str, help = 'options: start, end, projects, report, current, switch, edit')
    parser.add_argument( 'data', nargs='?',type=str, help = 'task or project:task')

    args = parser.parse_args()

    actions = ['start','add','end','projects','report', 'current','switch' ,'edit']
    if args.action not in actions:
       parser.print_help()
       parser.exit()

    if args.action == "add" and not args.data :
       parser.print_help()
       parser.exit()

    tracker = Tt(vars(args))
    tracker.run()
