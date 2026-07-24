[app]
title = EdgeOS Solution
package.name = edgeossolution
package.domain = org.criador
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 3.1
requirements = python3,kivy,reportlab,urllib3

orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.private_storage = True
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

[buildozer]
log_level = 2
warn_on_root = 0
