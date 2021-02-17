import os

# system properties
TAG_SYSTEM = 'System_'
TAG_VERSION_RAISE = f'{TAG_SYSTEM}raise'
TAG_VERSION_KEEP = f'{TAG_SYSTEM}keep'

# versions
VERSION_NAME = 'version_name'
VERSION_CODE = 'version_code'

PROJECT_APP = "app"
PROJECT_MAIN = os.path.join(PROJECT_APP, "src/main")
PROJECT_STRINGS_FILE = os.path.join(PROJECT_MAIN, 'res/values/strings.xml')
PROJECT_ASSETS_DIR = os.path.join(PROJECT_MAIN, 'assets')
PROJECT_BUILD_GRADLE_FILE = os.path.join(PROJECT_APP, 'build.gradle')
PROJECT_MANIFEST = os.path.join(PROJECT_MAIN, 'AndroidManifest.xml')
