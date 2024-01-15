# command: setup.py install
import configparser
from Cython.Build import cythonize
import sys
import os
import platform

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools import Extension
import subprocess

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
CONFIG_FILE = os.path.join(ROOT_PATH, 'setup.cfg')
ANYLOG_PY = os.path.join(ROOT_PATH, 'src', 'sample_data_generator.py')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
PKG_NAME = config['metadata']['name']
PKG_VERSION = config['metadata']['version']
PKG_AUTHOR = config['metadata']['author']
PKG_CONTACT = config['metadata']['contact']
PKG_DESCRIPTION = config['metadata']['description']
CPU_TYPE = platform.machine()

subprocess.run(["cython", "--embed", ANYLOG_PY])


class InstallCommand(install):
    def run(self):
        # Run PyInstaller to create an executable
        if not os.path.isfile(ANYLOG_PY):
            raise ValueError(f"Failed to locate {ANYLOG_PY}")
        exe_extension = '.exe' if sys.platform == 'win32' else ''
        subprocess.run(["pyinstaller", "--onefile", f"--name=sample_data_generator_{CPU_TYPE}_v{PKG_VERSION}{exe_extension}", ANYLOG_PY])

        try:
            install.run(self)
        except Exception as error:
            print(f"install.run fails (Error: {error}) | AnyLog Path: {ANYLOG_PY}")


ext_modules = [Extension("src", [ANYLOG_PY])]


try:
    setup(
        name=PKG_NAME,
        version=PKG_VERSION,
        author=PKG_AUTHOR,
        author_email=PKG_CONTACT,
        description=PKG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            # 'requests>=2.26.0',
            # 'pytz>=2021.3',
            # 'python-dateutil>=2.8.2',
            # 'cryptography>=3.4.8'
            # 'psutil>=5.8.0'
        ],
        scripts=["anylog.py"],  # This assumes that your main script is anylog.py
        cmdclass={"install": InstallCommand},
        ext_modules=cythonize(ext_modules)
    )
except Exception as error:
    print(f"setup fails (Error: {error}) | AnyLog Path: {ANYLOG_PY}")
