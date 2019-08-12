cmake_minimum_required(VERSION 2.8.3)

project(pacmod_game_control_ui)

find_package(catkin REQUIRED COMPONENTS
  
  roslint
  qt_gui_app
  roscpp
  rospy
  std_msgs
  pacmod_msgs
)

roslint_python()
catkin_python_setup()

###################################
## catkin specific configuration ##
###################################
catkin_package(
  LIBRARIES pacmod_game_control_ui
  CATKIN_DEPENDS pacmod_msgs qt_gui_app roscpp rospy std_msgs
)

###########
## Build ##
###########
include_directories(include ${catkin_INCLUDE_DIRS} )

#############
## Install ##
#############

catkin_install_python(PROGRAMS src/game_controller_ui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

## Mark executables and/or libraries for installation
# install(TARGETS ${PROJECT_NAME} ${PROJECT_NAME}_node
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

 install(FILES joygui.launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION} )

