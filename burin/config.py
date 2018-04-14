import collections
import configparser

TYPES = {'int': int, 'bool': bool, 'str': str, 'float': float}


class VerifiedConfigParser(configparser.ConfigParser):

    def __init__(self, spec_filename, **kwargs):
        super().__init__(**kwargs)
        self.specification = configparser.ConfigParser()
        self.specification.read(spec_filename)

    def verify(self, f):
        '''Verify that the given config file matches the specification.
        '''
        config = configparser.ConfigParser()
        config.read(f)
        for s in config.sections():
            for o in config.options(s):
                if not self.specification.has_option(s, o):
                    return False

        return True

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

        spec = {'type': _type, 'default': _type(_default)}
        return spec

    def verified_get(self, section, option, raw=False):
        '''Get an option using the type and default from the specification file.
        '''
        spec = self.get_spec(section, option)

        if not super().has_option(section, option):
            return spec['default']

        value = super().get(section, option, raw=raw)

        return(spec['type'](value))
