---
title: "Virtual Machines"
menu:
  main:
    parent: "contest"
    weight: 2
draft: false
no_header: true
---

{{< section title="Virtual Machines" link="/../vms/rmi-image-v1.zip" >}}

We prepared a Linux based Virtual Machine to provide a ready-to-use contest environment for contestants, with development environments, compilers, debuggers,
terminal multiplexers, and auto-snapshotting for fault-tolerance. The virtual machine also uses the same compiler version as the contest server.

**Contestants are not required to use the Virtual Machine!** However, we encourage you to do so.

The virtual machine includes the following software:

* XFCE Desktop Environment
* Firefox
* Evince document viewer
* XFCE Terminal, GNOME Terminal, and Konsole
* tmux and byobu
* Code::Blocks, Eclipse C++ Edition, Geany, Sublime Text 3, Vim, and Neovim
* Python 3 and Ruby
* GCC and G++ 7.5.0, GDB, DDD (Data Display Debugger), Valgrind
* GNU Make
* C++ Man Pages (C++ Reference can also be viewed from the contest server)

Requirements for the virtual machine:

* Latest version of [Virtual Box](https://www.virtualbox.org/), 64 bit version
* Virtualization technology enabled in the BIOS (can also be found under the names VT-x, VT-d, SVM, AMD-V)
* Intel or AMD 64-bit CPU with at least two cores and four threads
* At least 8 GB of RAM
* At least 64 GB of free storage

{{< section title="Usage instructions" >}}

* Make sure that you have virtualization enabled in BIOS and install Virtual Box
* Download the zip file at the top of the page and unzip it in a folder
* Double click the `.ovf` file, Virtual Box should open. If it doesn't, open Virtual Box and click on File - Import Appliance and select the `.ovf` file.
* Click OK to import the virtual machine
* Start the VM
* Log in with user "RMI Contestant" and password `rmi`
