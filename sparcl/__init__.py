# List of packages to import when "from sparcl import *" is used
__all__ = ["client"]


# See semantic versioning

# BUT PyPi requires honoring versions like this:
# https://packaging.python.org/specifications/core-metadata/
# https://www.python.org/dev/peps/pep-0440/
#
# '0.3.0-alpha3.23' is an invalid value for Version.
#  Error: Start and end with a letter or numeral containing only ASCII
#  numeric and '.', '_' and '-'.
#
# https://semver.org/ yields possible versions that violate PEP-0440

#__version__ = '0.3.21'
#__version__ = '0.1a3.dev22'
#__version__ = '0.3.0-alpha3.23'
#__version__ = '0.3.22'

# must mach: [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
# Example of a correct version string: '0.4.0a3.dev35'
#__version__ = '0.4.0b1.dev8'
#__version__ = '0.4.0b1.dev10'
#__version__ = '1.0.0'
__version__ = '1.0.0b1.dev7'
