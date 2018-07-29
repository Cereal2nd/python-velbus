"""
:author: Maikel Punie <maikel.punie@gmail.com> and Thomas Delaet <thomas@delaet.org>
"""
class CommandRegistry:

    def __init__(self, module_directory):
        self._module_directory = module_directory
        self._default_commands = {}
        self._overrides = {}

    def register_command(self, command_value, command_class, module_type=0):
        assert isinstance(command_value, int)
        assert command_value >= 0 and command_value <= 255
        assert isinstance(command_class, type)
        assert module_type in self._module_directory or module_type == 0 
        if module_type:
            self._register_override(command_value, command_class, module_type)
        else:
            self._register_default(command_value, command_class)
        
    def _register_override(self, command_value, command_class, module_type):
        if module_type not in self._overrides:
            self._overrides[module_type] = {}
        if command_value not in self._overrides[module_type]:
            self._overrides[module_type][command_value] = command_class
        else:
            raise Exception("double registration in command registry")

    def _register_default(self, command_value, command_class):
        if command_value not in self._default_commands:
            self._default_commands[command_value] = command_class
        else:
            raise Exception("double registration in command registry")

    def has_command(self, command_value, module_type=0):
        if module_type in self._overrides:
            if command_value in self._overrides[module_type]:
                return True
        if command_value in self._default_commands:
            return True
        return False

    def get_command(self, command_value, module_type=0):
        assert self.has_command(command_value)
        if module_type in self._overrides:
            if command_value in self._overrides[module_type]:
                return self._overrides[module_type][command_value]
        if command_value in self._default_commands:
            return self._default_commands[command_value]