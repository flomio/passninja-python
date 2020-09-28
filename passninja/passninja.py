import urllib.parse
import requests


class PassNinjaException(Exception):
    pass


class PassNinjaInvalidArgumentsException(PassNinjaException):
    pass


class SimplePassObject:
    """
    Result of creating a new NFC pass. Contains attributes: `url`, `serialNumber`, `passType`.
    """

    def __init__(self, data):
        self.url = data['urls']['landing']
        self.serialNumber = data['serialNumber']
        self.passType = data['passType']


class PassNinjaClient:
    """
    Use an instance of this class to make requests to PassNinja API.
    """

    _PASSNINJA_BASE_PATH = 'https://api.passninja.com/v1'

    def __init__(self, account_id, api_key):
        """
        :param str account_id: PassNinja API account ID.
        :param str api_key: PassNinja API key.
        """
        if not isinstance(account_id, str) or not isinstance(api_key, str):
            raise PassNinjaInvalidArgumentsException('Invalid argument types in PassNinjaClient constructor. PassNinjaClient(account_id: str, api_key: str)')
        self._session = requests.session()
        self._session.headers = requests.utils.default_headers()
        self._session.headers.update((
            ('user-agent', 'PassNinja python client'),
            ('content-type', 'application/json'),
            ('x-account-id', account_id),
            ('x-api-key', api_key),
        ))

    def _call(self, url, method=None, **kw):
        url = self._PASSNINJA_BASE_PATH + url
        if method is None:
            method = self._session.get
        resp = method(url, **kw)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _check_invalid_keys(client_pass_data):
        invalid_keys = [k
            for k, v in client_pass_data.items()
                if not isinstance(k, str) or not isinstance(v, str)
        ]
        if invalid_keys:
            raise PassNinjaInvalidArgumentsException('Invalid templateStrings provided in client_pass_data object. Invalid keys: ' + ', '.join(map(str, invalid_keys)))

    def _fetch_required_keys_set(self, pass_type):
        resp = self._call('/passtypes/keys/' + pass_type)
        return set(resp['keys'])

    @staticmethod
    def _pass_url(pass_type, serial_number):
        pass_type = urllib.parse.quote(pass_type)
        serial_number = urllib.parse.quote(serial_number)
        return '/passes/%s/%s' % (pass_type, serial_number)

    def pass_create(self, pass_type, client_pass_data):
        """
        Creates a new NFC pass

        :param str pass_type: PassNinja type ID
        :param dict client_pass_data: An object containing any key-value pairs in the passType's
            template fields with keys that match the template strings you want to replace

        :rtype: SimplePassObject
        """
        if not isinstance(pass_type, str) or not isinstance(client_pass_data, dict):
            raise PassNinjaInvalidArgumentsException('Invalid argument types in pass_create method. pass_create(pass_type: str, client_pass_data: dict)' )
        self._check_invalid_keys(client_pass_data)
        required_keys = self._fetch_required_keys_set(pass_type)
        required_keys -= client_pass_data.keys()
        if required_keys:
            raise PassNinjaInvalidArgumentsException('Some keys that are required for this pass_type are missing on the provided client_pass_data object. Missing keys: ' + ', '.join(required_keys))
        data = self._call('/passes', self._session.post, json={
            'passType': pass_type,
            'pass': client_pass_data,
        })
        return SimplePassObject(data)

    def pass_get(self, pass_type, serial_number):
        """
        Get data for an NFC pass

        :param str pass_type: PassNinja type ID
        :param str serial_number: The serial UUID for the pass you are querying.

        :rtype: dict
        """
        if not isinstance(pass_type, str) or not isinstance(serial_number, str):
            raise PassNinjaInvalidArgumentsException('Invalid argument types in pass_get method. pass_get(pass_type: str, serial_number: str)' )
        return self._call(self._pass_url(pass_type, serial_number))

    def pass_put(self, pass_type, serial_number, client_pass_data):
        """
        Update NFC pass.

        :param str pass_type: PassNinja type ID
        :param str serial_number: The serial UUID for the pass you want to update.
        :param dict client_pass_data: An object containing any key-value pairs in the passType's
            template fields with keys that match the template strings you want to replace

        :rtype: dict
        """
        if not isinstance(pass_type, str) or not isinstance(serial_number, str) or not isinstance(client_pass_data, dict):
            raise PassNinjaInvalidArgumentsException('Invalid argument types in pass_put method. pass_put(pass_type: str, serial_number: str, client_pass_data: dict)' )
        self._check_invalid_keys(client_pass_data)
        return self._call(self._pass_url(pass_type, serial_number), self._session.put, json={
            'passType': pass_type,
            'pass': client_pass_data,
        })

    def pass_delete(self, pass_type, serial_number):
        """
        Set a currently existing pass to be invalid/inactive. Returns serial_number.

        :param str pass_type: PassNinja type ID
        :param str serial_number: The serial UUID for the pass you want to update.

        :rtype: str
        """
        if not isinstance(pass_type, str) or not isinstance(serial_number, str):
            raise PassNinjaInvalidArgumentsException('Invalid argument types in pass_delete method. pass_delete(pass_type: str, serial_number: str)' )
        self._call(self._pass_url(pass_type, serial_number), self._session.delete)
        return serial_number
