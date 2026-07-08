[app]

# Название приложения (будет отображаться на устройстве)
title = Zombix OFFline

# Пакетное имя (уникальный идентификатор)
package.name = zombixoffline

# Домен + пакет (обратный DNS)
package.domain = org.example

# Версия приложения (целое число)
version = 2.3

# Требуемая версия Android SDK
android.api = 30

# Минимальная версия Android
android.minapi = 21

# Требуемые разрешения (камера, интернет и т.д.)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# Основной файл игры (точка входа)
source.dir = .

# Главный скрипт (должен называться main.py, но можно указать своё)
main.py = main.py

# Требуемые Python-библиотеки (указываем pygame и другие)
requirements = python3, pygame, opencv-python, numpy, json, random, math, sys, os

# Ориентация экрана (portrait / landscape / both)
android.orientation = both

# Разрешение на использование OpenGL ES 2.0
android.gles_version = 2

# Иконка приложения (путь к PNG 512x512)
icon.filename = icon.png

# Заставка (можно указать)
presplash.filename = splash.png

# Включаем поддержку сенсорного экрана
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# Дополнительные аргументы для Gradle
android.gradle_args = --no-daemon

# Отключаем лишние разрешения
android.ignore_activities = True

# Включаем режим отладки (можно убрать перед релизом)
android.debug = True

[buildozer]

# Логирование
log_level = 2

# Папка для сборки
build_dir = ./build

# Кэш скачанных пакетов
cache_dir = ./cache

# Показывать подробный вывод
warn_on_root = 1
