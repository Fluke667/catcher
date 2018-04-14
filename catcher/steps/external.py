import json
import subprocess

from catcher.utils.logger import debug, warning

from catcher.steps.step import Step


class External(Step):
    def __init__(self, body: dict, module: str) -> None:
        super().__init__(body)
        method = Step.filter_predefined_keys(body)
        self._data = {method: body[method]}
        self._module = module

    @property
    def module(self) -> str:
        return self._module

    @property
    def data(self) -> any:
        return self._data

    def action(self, includes: dict, variables: dict) -> dict:
        json_args = json.dumps({'variables': variables, 'data': self.data})
        p = subprocess.Popen([self.module, json_args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if p.wait() == 0:
            out = p.stdout.read().decode()
            debug(out)
            return self.process_register(variables, json.loads(out))
        else:
            out = p.stdout.read().decode()
            warning(out)
            raise Exception('Execution failed.')


