[app]

# Название приложения
title = Zombix OFFline

# Пакетное имя
package.name = zombixoffline

# Домен
package.domain = org.example

# Версия
version = 2.3

# Android API
android.api = 30

# Минимальная версия
android.minapi = 21

# Разрешения
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# Путь к исходникам (текущая папка)
source.dir = .

# Главный скрипт
main.py = main.py

# Требования
requirements = python3, pygame, opencv-python, numpy, json, random, math, sys, os

# Ориентация
android.orientation = both

# OpenGL
android.gles_version = 2

# Иконка
icon.filename = icon.png

# Заставка
presplash.filename = splash.png

# Дополнительные зависимости
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# Путь к SDK (указываем для GitHub Actions)
android.sdk_path = /home/runner/android-sdk

# Версия build-tools
android.build_tools_version = 37.0.0

# Отладка
android.debug = True

[buildozer]

# Логирование
log_level = 2

# Папка сборки
build_dir = ./build

# Кэш
cache_dir = ./cache

warn_on_root = 1
