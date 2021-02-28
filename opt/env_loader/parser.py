import re

from .consts import BOOL_TRUE_VALUES, BOOL_FALSE_VALUES, NULL_VALUES


class DefaultEnvParser:
    def parse(self, v):
        v = self.clear_value(v)

        if self.is_null(v):
            return None
        if self.is_true(v):
            return True
        if self.is_false(v):
            return False
        if self.is_list(v):
            v_list = v.split(",")
            new_v_list = []
            for v in filter(lambda x: len(x) > 0, v_list):
                new_v_list.append(self.parse(v))
            return new_v_list
        if self.is_int(v):
            return int(v)
        if self.is_float(v):
            return float(v)
        # default:
        return v

    def clear_value(self, v):
        return str(v).replace("\n", "")

    def is_null(self, v):
        return v in NULL_VALUES

    def is_true(self, v):
        return v in BOOL_TRUE_VALUES

    def is_false(self, v):
        return v in BOOL_FALSE_VALUES

    def is_int(self, v):
        return v.isdigit()

    def is_float(self, v):
        pattern = re.compile(r"[+-]?[0-9]+\.[0-9]*$")
        return pattern.match(v)

    def is_list(self, v):
        return "," in v
