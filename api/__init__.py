# See semantic versioning

# BUT PyPi requires honoring versions like this:
# https://packaging.python.org/specifications/core-metadata/
# https://www.python.org/dev/peps/pep-0440/
#
# '0.3.0-alpha3.23' is an invalid value for Version.
#  Error: Start and end with a letter or numeral containing only ASCII
#  numeric and '.', '_' and '-'.
#
# https://semver.org/
# Given a version number MAJOR.MINOR.PATCH, increment the:
#
# 1. MAJOR version when you make backwards incompatible API changes,
#
# 2. MINOR version when you add functionality in a backwards compatible
#    manner, and
#
# 3. PATCH version when you make backwards compatible bug fixes.
#
# Additional labels for pre-release and build metadata are available
# as extensions to the MAJOR.MINOR.PATCH format.
# https://regex101.com/r/Ly7O1x/3/

# sver = '0.3.0-a3.dev22'
#
# mo = re.match('^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$',sver)
#
# mo.group('major') =>  '0'
# mo.group('minor') =>  '3'
# mo.group('patch') =>  '0'
# mo.group('prerelease') => 'alpha3.22'


#__version__ = '0.3.21'
#__version__ = '0.1a3.dev22'
#__version__ = '0.3.0-alpha3.23'
__version__ = '0.3.0-a3.dev24'
#__version__ = '0.3.22'
