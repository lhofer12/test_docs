version: 2

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
      extra_requirements:
        - docs
    - method: setuptools
      path: another/package
  system_packages: true

 extensions = ['myst_parser']
