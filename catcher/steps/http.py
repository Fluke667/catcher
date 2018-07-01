import json

from requests import request

from catcher.steps.step import Step
from catcher.utils.file_utils import read_file
from catcher.utils.logger import debug
from catcher.utils.misc import fill_template, fill_template_str


class Http(Step):
    """
    :Input:

    :<method>: http method. See https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html for details

    - headers: Dictionary with custom headers. *Optional*
    - url: url to call
    - response_code: Code to await. *Optional* default is 200.
    - body: body to send (only for methods which support it).
    - body_from_file: File can be used as data source. *Optional* Either `body` or `body_from_file` should present.

    :Examples:

    Post data to server with custom header
    ::
        http:
          post:
            headers: {Content-Type: 'application/json', Authorization: '{{ token }}'}
            url: 'http://test.com?user_id={{ user_id }}'
            body: {'foo': bar}

    Post file to remote server
    ::
        http:
          post:
            url: 'http://test.com'
            body_from_file: "data/answers.json"

    """
    def __init__(self, body: dict) -> None:
        super().__init__(body)
        method = Step.filter_predefined_keys(body)  # get/post/put...
        self._method = method.lower()
        conf = body[method]
        self._url = conf['url']
        self._headers = conf.get('headers', {})
        self._body = None
        self._code = conf.get('response_code', 200)
        if self.method != 'get':
            self._body = conf.get('body', None)
            if self.body is None:
                self._file = conf['body_from_file']

    @property
    def method(self) -> str:
        return self._method

    @property
    def body(self) -> any:
        return self._body

    @property
    def file(self) -> str:
        return self._file

    @property
    def url(self) -> str:
        return self._url

    @property
    def headers(self) -> dict:
        return self._headers

    @property
    def code(self) -> int:
        return self._code

    def action(self, includes: dict, variables: dict) -> dict:
        url = fill_template(self.url, variables)
        headers = dict(
            [(fill_template_str(k, variables), fill_template_str(v, variables)) for k, v in self.headers.items()])
        body = self.__form_body(variables)
        debug('http ' + str(self.method) + ' ' + str(url) + ', ' + str(headers) + ', ' + str(body))
        if body is None:
            r = request(self.method, url, headers=headers)
        elif isinstance(body, dict):
            r = request(self.method, url, headers=headers, json=body)
        else:
            r = request(self.method, url, headers=headers, data=body)
        debug(r.text)
        if r.status_code != self.code:
            raise RuntimeError('Code mismatch: ' + str(r.status_code) + ' vs ' + str(self.code))
        try:
            response = r.json()
        except ValueError:
            response = r.text
        return self.process_register(variables, response)

    def __form_body(self, variables) -> str or dict:
        if self.method == 'get':
            return None
        body = self.body
        if body is None:
            body = read_file(fill_template_str(self.file, variables))
        if isinstance(body, dict):  # dump body to json to be able fill templates in
            body = json.dumps(body)
        return fill_template(body, variables)
