[app]
title = EdgeOS Solution

# (str) Package name
package.name = edgeos_solution

# (str) Package domain (needed for android packaging)
package.domain = org.security.antivirus

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,spec,tflite,pkl

# (str) Application versioning
version = 3.1

# =============================================================================
# CONFIGURAÇÕES UNIFICADAS - SEM DUPLICIDADE
# =============================================================================

# (list) Todas as dependências do projeto reunidas em uma única linha contínua
requirements = python3, kivy, pyjnius, https://github.com

# (list) Permissões nativas de sistema exigidas para o Antivírus monitorar os APKs
android.permissions = QUERY_ALL_PACKAGES, REQUEST_DELETE_PACKAGES, READ_SMS, READ_CONTACTS

# (list) Declaração do motor de Inteligência Artificial em segundo plano
android.services = Antivirus:service.py

# (int) Nível de API correto e homologado para o processador do Moto G32
android.api = 33
android.minapi = 21

# (str) Logotipo adaptativo oficial do aplicativo na interface do Android
icon.adaptive_foreground.filename = %(source.dir)s/logo.png
icon.adaptive_background.filename = %(source.dir)s/logo.png
# =============================================================================

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# Mantido vazio para evitar conflito com as permissões unificadas acima

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
