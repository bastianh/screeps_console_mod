
screeps console

![Screenshot](/screenshot/shot1.png?raw=true "Screenshot")

I started to rewrite parts of screeps_console (https://github.com/screepers/screeps_console) to add more window manager functions.

it should support split screen or switchable windows for shards (like screen)

stuff I changed:
  - plugin architecure
  - thread based connection instead of extra process
  - some menu stuff
  
currently not everything is working .. some stuff is hardcoded... everything WIP 

it should start with `python ./scronsole.py` ... I think it currently only works with python 3.*
