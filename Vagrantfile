# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Server side running CentOS 7
  # I decided to run HTTP and DNS servers on CentOS instead of Fedora to prevent
  # breakage during frequent updates. HTTP server is using lighttpd server, DNS
  # is running Bind for all of the servers.
  config.vm.define "server" do |server|
    server.vm.box = "fedora/28-cloud-base"
    server.vm.box_version = "20180425"
    #server.vm.box = "centos/7"
    server.vm.hostname = "server"
    server.vm.network "private_network", ip: "192.168.99.100"
    server.vm.network "private_network", ip: "192.168.99.101"
    server.vm.network "private_network", ip: "192.168.99.110"
    server.vm.network "private_network", ip: "192.168.99.120"
    server.vm.network "private_network", ip: "192.168.99.121"
    server.vm.network "private_network", ip: "192.168.99.122"
    server.vm.network "private_network", ip: "192.168.99.199"
  
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
    server.vm.synced_folder "keyring/verification-keys", "/srv/keys", type: "rsync"
  
    server.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook-server.yml"
    end
  end

  # Client side - Fedora 28
  config.vm.define "client" do |client|
    client.vm.box = "fedora/28-cloud-base"
    client.vm.box_version = "20180425"

    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "192.168.99.10"

    client.vm.provider :libvirt do |libvirt|
      libvirt.cpu_mode = "host-model"
      libvirt.memory = 1024
      libvirt.cpus = 1
      libvirt.driver = 'kvm'
    end

    client.vm.synced_folder "configuration/local-repo", "/vagrant/local-repo", type: "rsync"
    client.vm.synced_folder "tests", "/tests", type: "rsync"
    client.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook-client.yml"
    end

  end
end

