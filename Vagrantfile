# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "debian/jessie64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../acm.mst.edu", "/www/acm.mst.edu"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  $updates = <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip postgresql libpq-dev
  SHELL

  $db = <<-DB
    sudo -u postgres psql -c "create database django_acmgeneral" \
         -c "create user djangouser with password 'djangoUserPassword'" \
         -c "grant all privileges on database django_acmgeneral to djangouser"
  DB

  $migrate = <<-MIGRATE
    cd /vagrant 
    pip3 install -r requirements.txt
    cd ACM_General/
    cp ACM_General/settings_local.template ACM_General/settings_local.py
    python3 manage.py makemigrations
    python3 manage.py migrate
  MIGRATE

  config.vm.provision :shell, inline: $updates
  config.vm.provision :shell, inline: $db
  config.vm.provision :shell, inline: $migrate
end