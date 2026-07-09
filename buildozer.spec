[app]
title = Zombix OFFline
package.name = zombixoffline
package.domain = org.example
version = 2.3
android.api = 30
android.minapi = 21
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK
source.dir = .
main.py = main.py
requirements = python3, pygame, json, random, math, sys, os
android.orientation = both
android.gles_version = 2
icon.filename = icon.png
presplash.filename = splash.png
android.ndk = 23c
android.debug = True

[buildozer]
log_level = 2
build_dir = ./build
cache_dir = ./cache
warn_on_root = 1
