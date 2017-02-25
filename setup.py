from setuptools import setup, find_packages

setup(
    name='penguin',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'PyPDF2'
    ],
    entry_points='''
        [console_scripts]
        penguin=penguin.scripts.penguin_cli:penguin
    ''',
)
