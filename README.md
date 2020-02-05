# pacmod_game_control_ui
User interface for pacmod_game_control using PyQt4.

NOTE! The current best branch for Ros Melodic running on Ubuntu 18.04 is melodic_2020

Ros Melodic does not support the qt-build dependency anymore and the  package.xml and CMakeList.txt have been updated to reflect that. The application is still dependent on Qt and all dependencies can be install with the following command ran in the pacmod_game_control_ui directory


rosdep install --from-paths src --ignore-src --rosdistro=melodic -y

