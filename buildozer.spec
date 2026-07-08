[app]

# Название приложения
title = Zombix OFFline

# Пакетное имя
package.name = zombixoffline

# Домен + пакет (обратный DNS)
package.domain = org.example

# Версия приложения
version = 2.3

# Требуемая версия Android SDK
android.api = 30

# Минимальная версия Android
android.minapi = 21

# Разрешения
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# Путь к исходникам
source.dir = .

# Главный скрипт
main.py = main.py

# Зависимости Python
requirements = python3, pygame, opencv-python, numpy

# Ориентация экрана
android.orientation = both

# Версия OpenGL
android.gles_version = 2

# Иконка и заставка (замените на свои файлы, если есть)
icon.filename = icon.png
presplash.filename = splash.png

# Путь к Android SDK (будет использоваться на GitHub Actions)
android.sdk_path = /home/runner/android-sdk

# Версия build-tools
android.build_tools_version = 37.0.0

# Отключаем автоматическую загрузку SDK
android.skip_update = False

# Дополнительные настройки
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.gradle_args = --no-daemon
android.ignore_activities = True
android.debug = True

[buildozer]

# Логирование
log_level = 2

# Папки сборки
build_dir = ./build
cache_dir = ./cache

# Не использовать sudo
warn_on_root = 1
