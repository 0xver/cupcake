from setuptools import setup
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()
readme = (file_path/"README.md").read_text()

setup(
  name="cupcakes",
  version="0.1.7",
  description="Compile, test, deploy, and interact with smart contracts",
  long_description=readme,
  long_description_content_type="text/markdown",
  url="https://github.com/0xver/cupcake",
  author="Sam Larsen",
  license="MIT",
  packages=["cupcake"],
  entry_points = {
    "console_scripts": ["cupcake=cupcake.cli:main"],
  },
  install_requires=[
      "py-solc-x", "py-evm", "eth-tester", "web3", "PyYAML", "python-dotenv", "simple_term_menu",
  ],
  python_requires=">=3.9"
)
