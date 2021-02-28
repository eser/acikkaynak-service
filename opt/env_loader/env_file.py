import os

from .parser import DefaultEnvParser


def mergeDictsOverwriteEmpty(d1, d2):
    res = d1.copy()

    for key, value in d2.items():
        if key not in d1 or d1[key] == "":
            res[key] = value

    return res

class EnvFile:
    def __init__(self, auto_parse=True, parser_class=DefaultEnvParser):
        self.parser = parser_class()
        self.auto_parse = auto_parse
        self.vars = {}

    def get(self, key, default=None):
        v = self.vars.get(key, os.environ.get(key))
        return v if v is not None else default

    def __getitem__(self, item):
        return self.get(item)

    def update(self, data_dict):
        if self.auto_parse:
            data_dict = self._parse_values(data_dict)
        else:
            data_dict = self._clear_values(data_dict)

        self.vars = mergeDictsOverwriteEmpty(self.vars, data_dict)

    def export(self):
        for k, v in self.vars.items():
            os.environ.setdefault(k, str(v))

    def _parse_values(self, data_dict):
        for k, v in data_dict.items():
            data_dict[k] = self.parser.parse(v)
        return data_dict

    def _clear_values(self, data_dict):
        for k, v in data_dict.items():
            data_dict[k] = self.parser.clear_value(v)
        return data_dict

    def __iter__(self):
        for k, v in self.vars.items():
            yield k, v

    def __str__(self):
        return "env file"
