#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/devtop/pacmod_game_control_ui/src"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/devtop/pacmod_game_control_ui/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/devtop/pacmod_game_control_ui/install/lib/python2.7/dist-packages:/home/devtop/pacmod_game_control_ui/build/pacmod_game_control_ui/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/devtop/pacmod_game_control_ui/build/pacmod_game_control_ui" \
    "/usr/bin/python2" \
    "/home/devtop/pacmod_game_control_ui/src/setup.py" \
    build --build-base "/home/devtop/pacmod_game_control_ui/build/pacmod_game_control_ui" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/devtop/pacmod_game_control_ui/install" --install-scripts="/home/devtop/pacmod_game_control_ui/install/bin"
