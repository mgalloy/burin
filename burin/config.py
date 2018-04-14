import collections
import configparser

TYPES = {'int': int, 'bool': bool, 'str': str, 'float': float}


class VerifiedConfigParser(configparser.ConfigParser):

    def __init__(self, spec_filename, **kwargs):
        super().__init__(**kwargs)
        self.specification = configparser.ConfigParser()
        self.specification.read(spec_filename)

    def _apply_bool(self, value):
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

    def _apply_type(self, option_type, value):
        '''Apply option_type to value. Special rules for bool type to convert
           yes/no or true/false strings
        '''
        if value is None:
            return None

        if option_type == bool:
            return self._apply_bool(value)
        else:
            return option_type(value)

    def get_spec(self, section, option):
        '''Get specification for a given option. Returns a dict with keys
           "type" and "default".
        '''
        _type = str
        _default = None

        spec_str = self.specification.get(section, option)
        for token in spec_str.split(','):
            name, value = token.split('=')
            name = name.strip()
            if name.strip() == 'type':
                _type = TYPES[value.strip()]
            elif name == 'default':
                _default = value.strip()
            else:
                pass

        spec = {'type': _type, 'default': self._apply_type(_type, _default)}
        return spec

    def verified_get(self, section, option, raw=False):
        '''Get an option using the type and default from the specification file.
        '''
        spec = self.get_spec(section, option)

        if not super().has_option(section, option):
            return spec['default']

        value = super().get(section, option, raw=raw)

        return(self._apply_type(spec['type'], value))

    def verify(self, f):
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
                spec = self.get_spec(s, o)
                print(spec['default'])
                if spec['default'] is None:
                    if not config.has_option(s, o):
                        return False

        return True
