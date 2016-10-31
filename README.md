# Zeus

Zeus is aim to be a cross platform spyware with strong persistence ability with command & control server (separate project).

This project is for educational purposes only!

### Current Abilities:
 - [x] Infect Windows
 - [x] Gather device information - Need to confirm on Linux
 - [x] Take screenshots
 - [x] Check server every X minutes if there's something to do
 - [x] Command Line/Terminal - cross platform


### Command & Control
Command and control server should be a whole new different project.

### Installation

Configure connection to server and then compile to executable file.

Download and extract the [latest pre-built release](https://github.com/idanmos/Zeus/releases).



### Development

This is ongoing project and I'm welcome help in development

#### Building for source
Compile to target specific:
* Windows - pyinstaller
* Linux - ?
* macOS - ?
 

### Todo:

 - [ ] Disable Windows services during persistancy operation
 - [ ] Disable Windows Defender
 - [ ] Delete previous restore points in Windows
 - [ ] Keylogger
 - [ ] Infect removable devices
 - [ ] Mutex: make sure only one process is running
 - [ ] Check if we're running on virtual machine (kill if we're)
 - [ ] Ability to self update
 - [ ] Ability to self delete
 - [ ] Upload/Download files
 - [ ] Infect UEFI Bios to strong persistence to survive OS reinstall and hard disk format
 - [ ] Steal cookies
 - [ ] Steal passwords: Browsers, Outlook

License
----

MIT