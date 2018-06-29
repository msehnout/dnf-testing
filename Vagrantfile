# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "server" do |server|
    server.vm.box = "centos/7"
    server.vm.hostname = "server"
    server.vm.network "private_network", ip: "192.168.99.100"
    server.vm.network "private_network", ip: "192.168.99.101"
    server.vm.network "private_network", ip: "192.168.99.102"
    server.vm.network "private_network", ip: "192.168.99.110"
  
    server.vm.provider :libvirt do |libvirt|
      libvirt.cpu_mode = "host-model"
      libvirt.memory = 1024
      libvirt.cpus = 1
      libvirt.driver = 'kvm'
    end
  
    server.vm.synced_folder "configuration", "/vagrant", type: "rsync"
    server.vm.synced_folder "unit-files", "/var/run/systemd/system", type: "rsync"
    server.vm.synced_folder "keyring", "/keyring", type: "rsync"
    server.vm.synced_folder "packages/rpms", "/srv/f27", type: "rsync"
  
    server.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook-server.yml"
    end
  end
end

