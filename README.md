# Zeus

Zeus is a cross platform spyware with strong self persistance ability and command & control server.

This project is for educational purposes only!

### Current Abilities
  - Infect Windows to strong persistance
  - Gather device information - Need to confirm on Linux
  - Take screenshots - cross platform (not yet implemented)
  - Check server every X minutes if there's something to do
  - Command Line/Terminal - cross platform


### Command & Control
Command and control server should be a whole new different project.

### Installation

Configure connection to server and then compile to executable file.

Download and extract the [latest pre-built release](https://github.com/idanmos/Zeus/releases).



### Development

This is ongoing project and I'm welcome help in development

#### Building for source
Compile to target specific (Windows: pyinstaller, Linux: AnyIdeas?, Mac: AnyIdeas?).


### Todo:

 - Disable Windows services during persistancy operation
 - Disable Windows Defender
 - Delete previous restore points in Windows
 - Keylogger - cross platform
 - Infect removable devices - cross platform
 - Mutex: make sure only one process is running - cross platform
 - Check if we're running on virtual machine (kill if we're) - cross platform
 - Ability to self update - cross platform
 - Ability to self delete - cross platform
 - Upload/Download files

License
----

MIT