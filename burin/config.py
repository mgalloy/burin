import collections
import configparser
import datetime
from typing import Any, Callable, Dict


TYPES = {'int': int, 'bool': bool, 'str': str, 'float': float}


def _apply_bool(value: str) -> bool:
    '''Converts value string to bool. Accepts case-insensitive yes/no or
       true/false. Unknown values raise TypeError.
    '''
    lower_value = value.lower()
    if lower_value in ['yes', 'true']:
        return True
    elif lower_value in ['no', 'false']:
        return False
    else:
        raise TypeError

    return False


def _apply_type(option_type: Callable[[str], Any], value: str) -> Any:
    '''Apply option_type to value. Special rules for bool type to convert
       yes/no or true/false strings
    '''
    if value is None:
        return None

    if option_type == bool:
        return _apply_bool(value)
    else:
        return option_type(value)


def _parse_specline(specline: str) -> Dict[str, Any]:
    '''Parse a sting specline
    '''
    option_type = str
    option_default = None

    for token in specline.split(','):
        name, value = token.split('=')
        name = name.strip()
        if name.strip() == 'type':
            option_type = TYPES[value.strip()]
        elif name == 'default':
            option_default = value.strip()
        else:
            pass

    spec = {'type': option_type,
            'default': _apply_type(option_type, option_default)}
    return spec


def _parse_spec(spec: configparser.ConfigParser, section: str, option: str) -> Dict[str, Any]:
    '''Get specification for a given option. Returns a dict with keys
       "type" and "default".
    '''
    specline = spec.get(section, option)
    return(_parse_specline(specline))


class ConfigParser(configparser.ConfigParser):
    '''ConfigParser subclass which can verify a config file against a specification
       and uses types/defaults from the specification.
    '''

    def __init__(self, spec_filename: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.specification = configparser.ConfigParser()
        self.specification.read(spec_filename)

    def verified_get(self, section: str, option: str, raw=False) -> Any:
        '''Get an option using the type and default from the specification file.
        '''
        spec = _parse_spec(self.specification, section, option)

        if not super().has_option(section, option):
            return spec['default']

        value = super().get(section, option, raw=raw)

        return(_apply_type(spec['type'], value))

    def validate(self, f: str) -> bool:
        '''Verify that the given config file matches the specification.
        '''
        config = configparser.ConfigParser()
        config.read(f)

        # check that every option given by f is in specification
        for s in config.sections():
            for o in config.options(s):
                if not self.specification.has_option(s, o):
                    return False

        # check that all options without a default value are given by f
        for s in self.specification.sections():
            for o in self.specification.options(s):
                spec = _parse_spec(self.specification, s, o)
                if spec['default'] is None:
                    if not config.has_option(s, o):
                        return False

        return True


def parse_datetime(s: str) -> datetime.datetime:
    '''Parses a string in either YYYYMMDD or YYYYMMDD.HHMMSS formats.

       Raises KeyError if not in a valid date or date/time formats.
    '''
    if len(s) == 8:
        return datetime.datetime.strptime(s, '%Y%m%d')
    elif len(s) == 15:
        return datetime.datetime.strptime(s, '%Y%m%d.%H%M%S')
    else:
        raise KeyError


class EpochParser:

    def __init__(self, epochs_filename: str, epochs_spec_filename: str) -> None:
        self.epochs = configparser.ConfigParser()
        self.epochs.read(epochs_filename)

        self.epochs_spec = configparser.ConfigParser()
        self.epochs_spec.read(epochs_spec_filename)

        self.date = '00000000.000000'

    def get(self, option: str) -> Any:
        '''Get an option from the epoch closest, but before, the current time.
        '''
        now = parse_datetime(self.date)

        specs = self.epochs_spec.defaults().copy()
        for k in specs.keys():
            specs[k] = _parse_specline(specs[k])

        secs = self.epochs.sections()
        sec_dts = [parse_datetime(s) for s in secs]
        sorted_secs = sorted(zip(sec_dts, secs), key=lambda x: x[0])

        last = (sorted_secs[0], sorted_secs[1], specs[option]['default'])

        for dt, sec in sorted_secs:
            if dt <= now and self.epochs.has_option(sec, option):
                last = (dt, sec, self.epochs.get(sec, option))

        return _apply_type(specs[option]['type'], last[2])

    def validate(self) -> bool:
        '''Verify that all the variables in the epochs file are given in the
           specification file.
        '''
        varnames = self.epochs_spec.defaults().keys()

        for s in self.epochs.sections():
            for o in self.epochs.options(s):
                if o not in varnames:
                    print('%s, %s' % (s, o))
                    return False

        return True
