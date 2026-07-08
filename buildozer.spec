[app]
title = Zombix OFFline
package.name = zombixoffline
package.domain = org.example
version = 2.3
android.api = 30
android.minapi = 21
android.ndk_api = 24
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK
source.dir = .
main.py = main.py
requirements = python3, pygame, opencv-python, numpy, json, random, math, sys, os
android.orientation = both
android.gles_version = 2
icon.filename = icon.png
presplash.filename = splash.png
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.sdk_path = /home/runner/android-sdk
android.build_tools_version = 37.0.0
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724
android.debug = True

[buildozer]
log_level = 2
build_dir = ./build
cache_dir = ./cache
warn_on_root = 1
