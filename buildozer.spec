[app]
title = English Quiz
package.name = englishquiz
package.domain = org.example
version = 1.0
version.code = 1
author = Your Name
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,ttf

requirements = python3==3.10.5,kivy==3.2.1,openssl
android.sdk = 30
android.api = 30
android.ndk_path = auto
android.arch = arm64-v8a
android.permissions = INTERNET
android.features =
p4a.branch = develop

log_level = 2
debug = 0
fullscreen = 1
orientation = portrait
