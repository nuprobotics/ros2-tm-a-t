from setuptools import setup

package_name = 'task03'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/task03.launch']),
        ('share/' + package_name + '/config', ['config/task03.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tmat',
    maintainer_email='todo@todo.com',
    description='Task 03 - Trigger service client and server node',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'trigger_node = task03.trigger_node:main',
        ],
    },
)
