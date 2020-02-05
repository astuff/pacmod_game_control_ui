cmake_minimum_required(VERSION 2.8.3)

project(pacmod_game_control_ui)

find_package(catkin REQUIRED COMPONENTS
  
  roslint
  roscpp
  rospy
  std_msgs
  pacmod_msgs
)

## find_package(Qt4 REQUIRED COMPONENTS QtCore QtGui)
###########
# NON-ROS #
###########
find_package(Qt5 COMPONENTS Core Gui Widgets)

roslint_python()
catkin_python_setup()

############
# SECTIONS #
############

file(GLOB QT_FORMS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ui/*.ui)
file(GLOB QT_RESOURCES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} resources/*.qrc)

QT5_ADD_RESOURCES(QT_RESOURCES_CPP ${QT_RESOURCES})
QT5_WRAP_UI(QT_FORMS_HPP ${QT_FORMS})

include_directories(
    ${Qt5Core_INCLUDE_DIRS}
    ${Qt5Gui_INCLUDE_DIRS}
    ${Qt5Widgets_INCLUDE_DIRS}
    )


###########
# SOURCES #
###########

set(QT_SOURCES
    src/main.cpp
    src/mainwindow.cpp
    src/qnode.cpp

    include/nav_ui/mainwindow.hpp
    include/nav_ui/qnode.hpp
    )

###################################
## catkin specific configuration ##
###################################
catkin_package(
  LIBRARIES pacmod_game_control_ui
  CATKIN_DEPENDS pacmod_msgs roscpp rospy std_msgs
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

