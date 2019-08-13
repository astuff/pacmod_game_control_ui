###########
## CMake ##
###########

cmake_minimum_required(VERSION 2.8.3)

project(pacmod_game_control_ui)

find_package(catkin REQUIRED COMPONENTS

  qt_build
  roscpp
  rospy
  std_msgs
  pacmod_msgs
)

catkin_python_setup()

###################################
## catkin specific configuration ##
###################################
catkin_package(
#  INCLUDE_DIRS include
  LIBRARIES pacmod_game_control_ui
  CATKIN_DEPENDS pacmod_msgs qt_build roscpp rospy std_msgs
# DEPENDS system_lib
)


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
 include
  ${catkin_INCLUDE_DIRS}
)


#############
## Install ##
#############

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS src/game_controller_ui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

# Mark other files for installation (e.g. launch and bag files, etc.)
 install(FILES
    joygui.launch
   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
 )

