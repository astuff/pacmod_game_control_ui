# pacmod_game_control_ui
User interface for pacmod_game_control using PyQt4.

To install on a platform the following dependencies need to be installed
- pyqt4 
- qtbuild

This can be achieved with the following terminal commands 

rosdep install --from-paths src --ignore-src --rosdistro=kinetic -y

sudo apt-get install python-qt4

Currently the image files included in the package need to be set for each platform the application is installed on, but once set should not have to change.

Qt has two methods to make image resources independent of full system path.

The first method:

is setup upon file generation and abstracts the absolute path with ../, but would not work for me in the LEXUS_RH_450H despite trying to manipulate the path with ../ and versus having to us the absolute path for example (/home/platform/ws/src/package/src/images/file.png)

The second method:

is making a resource folder with a xml file that identifies the relative path within the ros package directory and is still being researched for implementation in this applicaiton to make the pacmod_game_control_ui work across all platforms without having to set the absolute path for each image.
