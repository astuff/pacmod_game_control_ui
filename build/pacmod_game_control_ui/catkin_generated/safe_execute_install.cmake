execute_process(COMMAND "/home/devtop/pacmod_game_control_ui/build/pacmod_game_control_ui/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/devtop/pacmod_game_control_ui/build/pacmod_game_control_ui/catkin_generated/python_distutils_install.sh) returned error code ")
endif()