import os
import platform
import sys
import json
import os.path
from setuptools import setup, find_packages
from setuptools.command.install import install

pkg_name = 'sideboard'
__here__ = os.path.abspath(os.path.dirname(__file__))

# http://stackoverflow.com/a/16084844/171094
with open(os.path.join(__here__, pkg_name, '_version.py')) as version:
    exec(version.read())

def fetchgit():
    # SIDEBOARD_GITPLUGINS is a json list of objects for each plugin
    # {"plugin_directory": "uber", "git_url": "https://github.com/bitbyt3r/ubersystem.git", "branch": "master"}
    gitplugins = json.loads(os.environ.get('SIDEBOARD_GITPLUGINS', '[]'))
    for gitplugin in gitplugins:
        plugin_directory = ""
        if 'plugin_directory' in gitplugin:
            plugin_directory = os.path.join(__here__, "plugins", gitplugin['plugin_directory'])
        branch = gitplugin.get("branch", "master")
        clone_cmd = "git clone --depth=1 --branch {} {} {}".format(branch, gitplugin['git_url'], plugin_directory)
        os.system(clone_cmd)
        requirements_file = os.path.join(plugin_directory, "requirements.txt")
        if os.path.isfile(requirements_file):
            os.system("pip install -r {}".format(requirements_file))

class FetchCommand(install):
    def run(self):
        fetchgit()

setup_requires = {'setup_requires': ['distribute']} if sys.version_info[0] == 2 else {}
setup(
    name=pkg_name,
    version=__version__,
    description='Sideboard plugin container.',
    license='BSD',
    scripts=[],
    install_requires=[
        'configobj>=5.0.5',
        'cherrypy==17.3.0',
        'ws4py>=0.3.2',
        'SQLAlchemy>=1.1.0',
        'six>=1.5.2',
        'Jinja2>=2.7',
        'rpctools>=0.3.1',
        'logging_unterpolation>=0.2.0',
        'requests>=2.2.1',
        'paver>=1.2.2',
        'wheel>=0.24.0',
        'pip>=1.5.6',
        'sh>=1.09',
        'psutil>=5.4.1',
    ] + ['python-prctl>=1.6.1'] if 'linux' in sys.platform else [],
    packages=find_packages(),
    include_package_data=True,
    package_data={pkg_name: []},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sep = sideboard.sep:run_plugin_entry_point'
        ]
    },
    extras_require={
        'perftrace': ['python-prctl>=1.6.1', 'psutil>=4.3.0']
    },
    cmdclass={
        'fetchplugins': FetchCommand
    },
    **setup_requires
)
