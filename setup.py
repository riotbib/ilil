from distutils.core import setup

setup(
        name="ilil",
        version="0.1",
        author="xkey",
        author_email="xkey@systemli.org",
        scripts=["ilil.py"],
        install_requires=[
           'bottle', 'toml', 'pillow', 'numpy',
        ],
)
