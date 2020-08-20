from setuptools import setup, find_packages

setup(name="Hive",
      version="0.0.1",
      description="A minimal framework for parallelizing tasks in python",
      author="Rajkumar Ramamurthy",
      author_email="raj1514@gmail.com",
      packages=find_packages(),
      install_requires=["rich", "torch"])