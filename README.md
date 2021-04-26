For the application, python 3 is required as well as Django version 3.1.7, this Django version is compatible with python 3.6, 3.7, 3.8, 3.9

There are also some python packages used, depending on your system, you can run “pip3 install packagename” or “pip packagename” or “sudo apt install packagename” to install the necessary packages. 

A few of the packages required: moviepy, mutagen, ffmpeg, livereload, requests, colorama
Most of the packages should be included when python and django are installed, but if anything is missing, you will see something like this in the terminal: “No ffmpeg exe could be found” or “ERROR: ffmpeg not found”, which can be fixed by installing the package with pip or sudo

cd into the directory with the “manage.py” file and execute:
python3 manage.py runserver to start the application
the directory should look like: TeamKaraoke (whatever the repo name is)/karaoke
