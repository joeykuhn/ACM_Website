# ACM-General Django Project

Welcome to the ACM-General Django Project!

## Installation
### Vagrant
Vagrant is a development tool we use to help ease the burden of configuring the different components of the project. With Vagrant, we don't have to worry about installing various things such as Django, Python3, postgreSQL, etc onto our local computer. Although we do recommend installing Python and Django if you haven't already so that you can practice with them in case you aren't familiar with them. Using Vagrant simply makes it so that when testing the website, all required components will be installed on a virtual machine and the website will be locally hosted for further viewing & testing.

#### Requirements
1. [Virtualbox](https://virtualbox.org)
  + Or another virtualization tool, but `virtualbox` works nicely with vagrant. (We suggest using VirtualBox unless you have previous experience with other virtualization tools).
2. [Vagrant](https://vagrantup.com)
  + Download the version compatible with your host operating system.

After satisfying these requirements, clone the repository down into the directory of your choosing using the command:
```bash
$ git clone https://github.com/MST-ACM/acm.mst.edu.git

# Or if you have a ssh key linked to your computer
$ git clone git@github.com:MST-ACM/acm.mst.edu.git
```

Then change to the directory in which the Vagrant file is located and run the following command: (This will initialize and provision the vagrant box; this may take some time)
```bash
$ vagrant up
```
After running `vagrant up`, you should be ready to start developing and working on the website! To access the site running on your computer locally, open up a web browser and enter `localhost:8000` into the address bar.

Here are some additional commands that allow you to interact with Vagrant more and that you'll most likely need to use:
```bash
$ vagrant reload --provision # this will restart and reprovision the vm

$ vagrant halt # this will shutdown the vm

$ vagrant status # this will report the current status of the vm

$ vagrant destroy # this will delete the vm

$ vagrant up # this will, of course, build the vm if it has been destroyed
```

## Apps
In order to see detailed information about each of the apps, please see the readme in each of the app directories.
1. [Core](ACM_General/core/)
  + This app handles the core components of the ACM\_General project such as the base templates, global static css documents, and a variety of other generic needs which the project requires
2. [Accounts](ACM_General/accounts/)
  + This app handles the main components of the account features of the project such as login, logout, registering of a user, and authenticating users.
  + This is where the custom authentication backend and custom BaseUser are stored.
3. [Events](ACM_General/events/)
  + This app handles the main event components of the project such as registering an event and registering for an event.
  + This app is also able to list out events in some organized fashion.
4. [Home](ACM_General/home/)
  + This app handles the main index of the project and the homepage.
5. [Payments](ACM_General/payments/)
  + This app handles transactions done with Stripe.
6. [Rest Api](ACM_General/rest_api/)
  + This app is used for interacting with the Django REST framework.
7. [Sigs](ACM_General/sigs/)
  + This app is used for creation and management of the different Special Interest Groups inside of ACM.
8. [Third Party Authentication](ACM_General/thirdparty_auth/)
  + This app handles third party authentication services which allow users to sign-in to the acm.mst.edu by using sites such as Google and Github.

## Contributing
Please contact [acm@mst.edu](acm@mst.edu) if you wish to contribute to this project.
