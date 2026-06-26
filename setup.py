from glob import glob
from setuptools import find_packages, setup

package_name = 'cognitive_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),        (
            'share/' + package_name + '/launch',
            glob('launch/*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Esther Aguado',
    maintainer_email='e.aguado.glez@gmail.com',
    description='Introduction to cognitive navigation architecture',
    license='MIT',
    entry_points={
        'console_scripts': [
            'symbolic_node = cognitive_nav.symbolic_node:main',
            'probabilistic_node = cognitive_nav.probabilistic_node:main',
        ],
    },
)