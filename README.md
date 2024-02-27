<p align="center">
    <img width="400px" src=https://user-images.githubusercontent.com/1587270/74537466-25c19e00-4f08-11ea-8cc9-111b6bbf86cc.png>
</p>
<h1 align="center">passninja-python</h1>
<h3 align="center">
Use <a href="https://passninja.com/docs">passninja-python</a> as a PyPi or Anaconda module.</h3>

<div align="center">
    <a href="https://github.com/flomio/passninja-python">
        <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg" />
    </a>
    <a href="https://github.com/flomio/passninja-python/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/flomio/passninja-cs.svg" />
    </a>
    <a href="https://www.pypi.com/package/@passninja/passninja-python">
        <img alt="pypi package" src="https://img.shields.io/pypi/v/@passninja/passninja-cs.svg?style=flat-square" />
    </a>
</div>

# Contents

- [Contents](#contents)
- [Installation](#installation)
- [Usage](#usage)
  - [`PassNinjaClient`](#passninjaclient)
  - [`PassNinjaClient Methods`](#passninjaclientmethods)
  - [Examples](#examples)
- [Documentation](#documentation)

# Installation

Install via pip:

```sh
pip install passninja
```

# Usage

## `PassNinjaClient`

Use this class to create a `PassNinjaClient` object. Make sure to
pass your user credentials to make any authenticated requests.

```python
import passninja

account_id = '**your-account-id**'
api_key = '**your-api-key**'

pass_ninja_client = passninja.PassNinjaClient(account_id, api_key)
```

We've placed our demo user API credentials in this example. Replace it with your
[actual API credentials](https://passninja.com/auth/profile) to test this code
through your PassNinja account and don't hesitate to contact
[PassNinja](https://passninja.com) with our built in chat system if you'd like
to subscribe and create your own custom pass type(s).

For more information on how to use `passninja-python` once it loads, please refer to
the [PassNinja JS API reference](https://passninja.com/docs/js)

## `PassNinjaClientMethods`

This library currently supports methods for creating, getting, updating, and
deleting passes via the PassNinja api. The methods are outlined below.

### Create

```python
simple_pass_object = pass_ninja_client.passes.create(
    'ptk_0x14', # passType
    {'discount': '50%', 'memberName': 'John'} # passData
)
print(simple_pass_object.url)
print(simple_pass_object.passType)
print(simple_pass_object.serialNumber)
```

### Find

Finds issued passes for a given pass template key

```python
pass_objects = pass_ninja_client.passes.find(
    'ptk_0x14', # passType aka pass template key
)
```

### Get

```python
detailed_pass_object = pass_ninja_client.passes.get(
    'ptk_0x14', # passType
    '97694bd7-3493-4b39-b805-20e3e5e4c770' # serialNumber
)
```

### Get Pass Template Details

```python
pass_template_object = pass_ninja_client.pass_templates.find(
  'ptk_0x14', # pass template key
)
print(pass_template_object.pass_type_id)
```

### Decrypt

Decrypts issued passes payload for a given pass template key

```python
decrypted_pass_object = pass_ninja_client.passes.decrypt(
    'ptk_0x14', # passType
    '55166a9700250a8c51382dd16822b0c763136090b91099c16385f2961b7d9392d31b386cae133dca1b2faf10e93a1f8f26343ef56c4b35d5bf6cb8cd9ff45177e1ea070f0d4fe88887' # payload
)
```

### Update

```python
simple_pass_object = pass_ninja_client.passes.put(
    'ptk_0x14', # passType
    '97694bd7-3493-4b39-b805-20e3e5e4c770', # serialNumber
    {'discount': '100%', 'memberName': 'Ted'} # passData
)
```

### Delete

```python
deleted_pass_serial_number = pass_ninja_client.passes.delete(
    'ptk_0x14', # passType,
    '97694bd7-3493-4b39-b805-20e3e5e4c770' # serialNumber
)
print('Pass deleted. Serial_number: ', deleted_pass_serial_number)
```

# Documentation

- [PassNinja Docs](https://www.passninja.com/documentation)
