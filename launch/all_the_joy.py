import roslaunch 

#roslaunch.configure_logging(uuid)
launch = roslaunch.scriptapi.ROSLaunch()
launch.start()


package = 'pacmod_game_control_ui'
executable = 'game_controller'
node = roslaunch.core.Node(package,required=True,executable)
process = launch.launch(node)
print(process.is_alive())
#process.stop()

try 
launch.spin
finally 
launch.shutdown()

#<node pkg="pacmod_game_control" type="pacmod_game_control_node.cpp" name="pacmod_game_control"/>



