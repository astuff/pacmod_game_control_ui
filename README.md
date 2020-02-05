# pacmod_game_control_ui
User interface for pacmod_game_control using PyQt4.

**************************AS OF Wednesday February 5th 2020************************** "\n"
NOTE! The current best branch for Ros Melodic running on Ubuntu 18.04 is melodic_2020
*************************************************************************************

Current best branch will be merged into master in the near future.

Ros Melodic does not support the qt-build dependency anymore. The package.xml and CMakeList file have been updated to reflect that. The application is still dependent on Qt and all dependencies can be install with the following command ran in the pacmod_game_control_ui directory

rosdep install --from-paths src --ignore-src --rosdistro=melodic -y

Launch file depends on pacmod_game_control and all its dependencies to be installed



