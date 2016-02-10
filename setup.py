
# python setup.py --dry-run --verbose install

import os.path
from setuptools import setup, find_packages
from distutils.command.install_scripts import install_scripts

from distutils.core import setup

class install_scripts_and_symlinks(install_scripts):
    '''Like install_scripts, but also replicating nonexistent symlinks'''
    def run(self):
        install_scripts.run(self)
        # Replicate symlinks if they don't exist
        for script in self.distribution.scripts:
            if os.path.islink(script):
                newlink = os.path.join(self.install_dir, os.path.basename(script))


setup(
    name='RainEagle',
    version='0.1.8',
    author='Peter Shipley',
    author_email='Peter.Shipley@gmail.com',
    packages=find_packages(),
    scripts=[ 'bin/meter_status.py', 'bin/plot_power.py' ],
    data_files=[
        ('examples', ['bin/plot_power.py', 'bin/gnup_poweruse.txt']),
        ('bin', ['bin/meter_status.py']) ],
    url='https://github.com/evilpete/RainEagle',
    license='BSD',
    description='Python Class for utilizing the Rainforest Automation Eagle ( RFA-Z109 ) socket API.',
    download_url='https://github.com/evilpete/RainEagle/archive/0.1.8.tar.gz',
    long_description=open('README.txt').read(),
    cmdclass = { 'install_scripts': install_scripts_and_symlinks }
)




