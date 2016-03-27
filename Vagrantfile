# -*- mode: ruby -*-
# vi: set ft=ruby :

internal_ip = "172.28.128.4"
project_name = "blog"

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/wily64"
  config.vm.network "private_network", ip: internal_ip
  config.vm.hostname = "blog"

  config.vm.provider :virtualbox do |v|
    v.memory = 1024
    v.gui = false
  end

  # for supress "stdin: is not a tty error"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.synced_folder ".", "/home/vagrant/" + project_name, id: "vagrant-root",
    owner: "vagrant",
    group: "vagrant",
    mount_options: ["dmode=775,fmode=664"]

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update -q
    apt-get autoremove -y
    apt-get install mc npm -y
    apt-get install python3-venv python3-dev -y
    npm install -g bower
    usermod -aG vagrant www-data
    echo '    IdentityFile /home/vagrant/.ssh/github' >> /etc/ssh/ssh_config
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv virtualenvironment
    source /home/vagrant/virtualenvironment/bin/activate && pip install pelican Markdown beautifulsoup4
    pip completion --bash >> ~/.profile
  SHELL

  # config.vm.provision "shell", privileged: false, inline: "pyvenv virtualenvironment"
  # config.vm.provision "shell", privileged: false, inline: "source /home/vagrant/virtualenvironment/bin/activate && pip install pelican Markdown"

end
