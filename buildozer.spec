[app]
title = Zombix OFFline
package.name = zombixoffline
package.domain = org.example
version = 2.3
android.api = 30
android.minapi = 21
android.ndk_api = 21
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK
source.dir = .
main.py = main.py
requirements = python3, pygame, sdl2, sdl2_image, sdl2_mixer, sdl2_ttf, json, random, math, sys, os
android.orientation = both
android.gles_version = 2
icon.filename = icon.png
presplash.filename = splash.png
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.sdk_path = /home/runner/android-sdk
android.build_tools_version = 37.0.0
android.ndk = 25c
android.debug = True

[buildozer]
log_level = 3
build_dir = ./build
cache_dir = ./cache
warn_on_root = 1
