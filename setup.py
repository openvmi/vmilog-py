from setuptools import setup, find_packages

VERSION = "0.3.0"

install_requires = [
]

setup(
    name="vmilog-py",
    version=VERSION,
    description="log library for vmilabs",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="vmilabs",
    author_email="zeekzhou@163.com",
    license="Apache-2.0",
    url="https://github.com/openvmi/vmilog-py",
    python_requires='>=3.6',
    keywords="vmilabs log sdk",
    install_requires=install_requires,
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
