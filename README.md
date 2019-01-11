# Event blogger
This is a flask based webserver application that uses third-party oauth authentication, SQL Alchemy, consumes a public API and exposes an API endpoint. With this, the user is able to publish events and see what other users publish.
## Preparation / installation

### Requirements
#### Git: 
If you don't already have Git installed, download Git from [this link](git-scm.com). Install the version for your operating system.
On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash). (On Mac or Linux systems you can use the regular terminal program.)
#### Virtual Box:
VirtualBox is the software that actually runs the VM. You can download it from [here](virtualbox.org). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.
Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
#### Vagrant: 
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from [here](vagrantup.com). Install the version for your operating system.
Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
#### SQLalchemy:
Open source ORM for python. Used to setup database in a python file. This is already installed in the vagrant file. You can download it [here](https://www.sqlalchemy.org/)
#### SQLite:
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
#### Flask: 
Web framework for python that does not require particular tools or libraries. To install, run `$ pip install Flask`


### The virtual machine
This project makes use of a Linux-based virtual machine (VM)

This will give you the SQLite database and support software needed to run the code.

To bring the virtual machine online, use `$ vagrant up`. Then log into it with `$ vagrant ssh`.

### Clone the project
Next, you should clone the project using this repository. This project already contains the initial database. It is recommended to use the database already setup, but if you want to restart it, you can delete `catalogandusers.db`and set it up again by running `python3 DB_setup.py` on the command line. Note: this won't recreate the categories needed to add items while using the platform, so they would need tobe generated manually by running the following commands on the command line: 

#### Open python:
`$ python3`

#### Import dependencies: 
`$ from sqlalchemy import create_engine`
`$ from sqlalchemy.orm import sessionmaker`
`$ from DB_setup import Base, EventType, Event, User`

#### Create connection and start session:
`$ engine = create_engine('sqlite:///catalogandusers.db', connect_args={'check_same_thread': False})`
`$ Base.metadata.bind = engine`
`$ DBSession = sessionmaker(bind=engine)`
`$ session = DBSession()`

#### Add category example:

`$ dummyCategory1 = EventType(name='sports', description='example')`
`$ session.add(dummyCategory1)`
`$ session.commit()`


## Usage
Either if you're using the inital database provided or started a new one, you can run the webserver by running on the terminal:
`$ python 3 project.py`
This will start a connection on port 5000. 
On your browser, go to http://localhost:5000/ to browse the webserver. 
### Main screen
Here, there is an event log of the latest items added by all the users. You won't be able to look at certain information unless logged in, which you can do by clicking `login`at the top-right corner. You can browse items by categories, add categories, and edit categories and delete them if you created them. 

## Known bugs
If a certain amount of time has passed since you log in, the session token expires and you can't log out. 


## License
MIT License

Copyright (c) 2018 Bernardo Suárez Sepúlveda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.