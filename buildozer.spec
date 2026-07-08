[app]

# Название приложения
title = Zombix OFFline

# Пакетное имя
package.name = zombixoffline

# Домен + пакет
package.domain = org.example

# Версия
version = 2.3

# Требуемая версия Android SDK
android.api = 30

# Минимальная версия Android
android.minapi = 21

# Разрешения
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# Основной файл
source.dir = .

# Главный скрипт
main.py = main.py

# Требуемые библиотеки
requirements = python3, pygame, opencv-python, numpy, json, random, math, sys, os

# Ориентация
android.orientation = both

# OpenGL
android.gles_version = 2

# Иконка
icon.filename = icon.png

# Заставка
presplash.filename = splash.png

# Дополнительные зависимости Gradle
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# Путь к SDK (указываем, чтобы Buildozer не скачивал свой)
android.sdk_path = /home/runner/android-sdk
android.build_tools_version = 37.0.0

# Режим отладки (можно убрать)
android.debug = True

[buildozer]

log_level = 2
build_dir = ./build
cache_dir = ./cache
warn_on_root = 1
