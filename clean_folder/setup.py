from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='This app is clean your folders',
    author="Iurii Popov",
    url='https://github.com/ShuguruiUA',
    packages=find_namespace_packages(),
    data_files=[('clean_folder', ['clean_folder/release.txt'])],
    include_package_data=True,
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:clean']}
)
pip