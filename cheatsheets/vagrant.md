# Vagrant Cheatsheet

## Install Vagrant

```sh
sudo apt install vagrant vagrant-qt virtualbox
#                (1)     (2)        (3)
```

1.  Install Vagrant!
2.  Necessary for running in GUI mode
3.  Vagrant uses this under the hood


## Add VM From File

```sh
vagrant box add my-vm /path/to/box/file.box
vagrant init my-vm
vagrant up
vagrant halt
vagrant destroy
```


## Change Resources Available for VM

In the `Vagrantfile`, edit this section:

```ruby
config.vm.provider "virtualbox" do |vb|
  vb.gui = true
  vb.memory = "8192"
  vb.cpus = 2
end
```

