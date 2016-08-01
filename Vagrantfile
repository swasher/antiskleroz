# -*- mode: ruby -*-
# vi: set ft=ruby :

internal_ip = "172.28.128.4"
project_name = "blog"
user = 'ubuntu'

Vagrant.configure(2) do |config|

  # native ubuntu/x
  #config.vm.box = "ubuntu/xenial64"
  config.vm.box = "ubuntu/wily64"
  #config.vm.box = "gbarbieru/xenial"
  #config.vm.box = "geerlingguy/ubuntu1604"
  config.vm.network "private_network", ip: internal_ip
  config.vm.hostname = "blog"

  config.vm.provider :virtualbox do |v|
    v.name = project_name
    v.memory = 1024
    v.gui = false
  end

  # for supress "stdin: is not a tty error"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.synced_folder ".", "/home/vagrant/" + project_name,
    id: "vagrant-root",
    owner: 'vagrant',
    group: 'vagrant',
    mount_options: ["dmode=775,fmode=664"]

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update -q
    apt-get autoremove -y
    apt-get install mc npm -y
    apt-get install python3-venv python3-dev -y
    npm install -g bower
    usermod -aG vagrant www-data
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv virtualenvironment
    source /home/vagrant/virtualenvironment/bin/activate && cd ~/blog && pip install wheel
    source /home/vagrant/virtualenvironment/bin/activate && cd ~/blog && pip install -r requirements.txt
    pip completion --bash >> ~/.profile
    git config --global user.email "mr.swasher@gmail.com"
    git config --global user.name "swasher"
  SHELL

end