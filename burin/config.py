import configparser
import datetime
import io
from typing import Callable, Dict, TypeVar


OptionValue = TypeVar('OptionValue', bool, float, int, str)
DateValue = TypeVar('DateValue', str, datetime.datetime)

TYPES = {'bool': bool, 'float': float, 'int': int, 'str': str}


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


def _apply_type(option_type: Callable[[str], OptionValue],
                value: str) -> OptionValue:
    '''Apply option_type to value. Special rules for bool type to convert
       yes/no or true/false strings
    '''
    if value is None:
        return None

    if option_type == bool:
        return _apply_bool(value)
    else:
        return option_type(value)


def _parse_specline(specline: str) -> Dict[str, OptionValue]:
    '''Parse a sting specline
    '''
    option_type = str
    option_default = None

    for token in specline.split(','):
        name, value = token.split('=')
        name = name.strip()
        if name == 'type':
            option_type = TYPES[value.strip()]
        elif name == 'default':
            option_default = value.strip()
        else:
            raise ConfigParser.OptionError(f'unknown option attribute {name}')

    spec = {'type': option_type,
            'default': _apply_type(option_type, option_default)}

    return spec


def _parse_spec(spec: configparser.ConfigParser,
                section: str,
                option: str) -> Dict[str, OptionValue]:
    '''Get specification for a given option. Returns a dict with keys
       "type" and "default".
    '''
    specline = spec.get(section, option)
    return _parse_specline(specline)


class ConfigParser(configparser.ConfigParser):
    '''ConfigParser subclass which can verify a config file against a specification
       and uses types/defaults from the specification.

       Todo: handle list of a type
    '''

    def __init__(self, spec_filename: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.specification = configparser.ConfigParser()
        self.specification.read(spec_filename)

    def typed_get(self, section: str, option: str, raw=False) -> OptionValue:
        '''Get an option using the type and default from the specification file.
        '''
        spec = _parse_spec(self.specification, section, option)

        if not super().has_option(section, option):
            return spec['default']

        value = super().get(section, option, raw=raw)

        return value if raw else _apply_type(spec['type'], value)

    def _write(self, fileobject):
        max_len = 0
        for s in self.specification.sections():
            for o in self.specification.options(s):
                max_len = max(max_len, len(o))

        new_line = '\n'
        first_section = True
        for s in self.specification.sections():
            new_line = '' if first_section else '\n'
            fileobject.write(f'{new_line}[{s}]\n')
            first_section = False
            for o in self.specification.options(s):
                v = self.typed_get(s, o)
                fileobject.write(f'{o:{max_len}s} = {v}\n')

    def write(self, file):
        if isinstance(file, str):
            with open(file, 'w') as f:
                self._write(f)
        else:
            self._write(file)

    def __str__(self):
        f = io.StringIO()
        self._write(f)
        f.seek(0)
        return f.read()

    def is_valid(self, f: str) -> bool:
        '''Verify that the given config file matches the specification.
        '''
        config = configparser.ConfigParser()
        config.read(f)

        # check that every option given by f is in specification
        for s in config.sections():
            for o in config.options(s):
                if config.has_option('DEFAULT', o):
                    continue
                if not self.specification.has_option(s, o):
                    return False

        # check that all options without a default value are given by f
        for s in self.specification.sections():
            for o in self.specification.options(s):
                if self.specification.has_option('DEFAULT', o):
                    continue
                spec = _parse_spec(self.specification, s, o)
                if spec['default'] is None:
                    if not config.has_option(s, o):
                        return False

        # TODO: make sure values are the correct type

        return True


def parse_datetime(s: str) -> datetime.datetime:
    '''Parses a string in either YYYYMMDD or YYYYMMDD.HHMMSS formats. Also,
       passes a datetime object through without change.

       Raises `ValueError` if not in a valid datetime or string in recognized
       date/time formats.
    '''
    if type(s) == str:
        # TODO: should use a date parsing library for this to recognize more
        #       formats for dates
        if len(s) == 8:
            return datetime.datetime.strptime(s, '%Y%m%d')
        elif len(s) == 15:
            return datetime.datetime.strptime(s, '%Y%m%d.%H%M%S')
        else:
            raise ValueError('unrecognized format for string date')
    else:
        if isinstance(s, datetime.datetime):
            return s
        else:
            raise ValueError('datetime must be a str or datetime object')


class EpochParser:
    '''EpochParser parses config files with dates as section names. Retrieving
       an option for a given date returns the option value on the date closest,
       but before, the given date.
    '''

    def __init__(self,
                 epochs_filename: str,
                 epochs_spec_filename: str) -> None:
        self.epochs = configparser.ConfigParser()
        self.epochs.read(epochs_filename)

        self.epochs_spec = configparser.ConfigParser()
        self.epochs_spec.read(epochs_spec_filename)

        self._date = None

        if not self.is_valid():
            raise KeyError('epochs filename does not satisfy specification')

    @property
    def date(self):
        '''Get the current date as a `datetime.datetime` object.
        '''
        return self._date

    @date.setter
    def date(self, date: DateValue):
        '''Set the date with a string of the form YYYYMMDD or YYMMDD.HHMMSS or a
           datetime.datetime object.
        '''
        self._date = parse_datetime(date)

    def get(self, option: str, date: DateValue=None) -> OptionValue:
        '''Get an option from the epoch closest, but before, the current time.

           Either set the `date` property or pass the `date` keyword to set the
           current time.
        '''
        now = self.date if date is None else parse_datetime(date)

        if now is None:
            raise KeyError('no date for access given')

        specs = self.epochs_spec.defaults().copy()
        for k in specs.keys():
            specs[k] = _parse_specline(specs[k])

        secs = self.epochs.sections()
        sec_dts = [parse_datetime(s) for s in secs]
        sorted_secs = sorted(zip(sec_dts, secs), key=lambda x: x[0])

        try:
            last = (sorted_secs[0], sorted_secs[1], specs[option]['default'])
        except KeyError:
            raise KeyError(f'option name "{option}" not found')

        for dt, sec in sorted_secs:
            if dt <= now and self.epochs.has_option(sec, option):
                last = (dt, sec, self.epochs.get(sec, option))

        return _apply_type(specs[option]['type'], last[2])

    def is_valid(self) -> bool:
        '''Verify that all the variables in the epochs file are given in the
           specification file.
        '''
        varnames = self.epochs_spec.defaults().keys()

        for s in self.epochs.sections():
            for o in self.epochs.options(s):
                if o not in varnames:
                    return False

        return True
