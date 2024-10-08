"""
A client for getting spectra and meta-data from NOIRLab.
"""

# List of packages to import when "from sparcl import *" is used
__all__ = ["client", "align_records"]


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

# __version__ = '0.3.21'
# __version__ = '0.1a3.dev22'
# __version__ = '0.3.0-alpha3.23'
# __version__ = '0.3.22'

# must mach: [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
# Example of a correct version string: '0.4.0a3.dev35'
# __version__ = '1.1'
# __version__ = '1.2.0b4'
# __version__ = '1.2.0'  # Release
# __version__ = "1.2.1b3"
# __version__ = "1.2.1"
# FIRST uncommented value will be used! (so only leave one uncommented)
#__version__ = "1.2.2"
__version__ = "1.2.3"
