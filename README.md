# Proxy Checker (Python)

[![Downloads](https://pepy.tech/badge/proxy-checker)](https://pepy.tech/project/proxy-checker)

A proxy checker in Python using PycURL, a Python interface to libcurl. To install this modified version unninstall any other version and do:

python3 -m pip install git+https://github.com/Scolymus/proxy-checker-python.git

## Description

The proxy checker takes a proxy as input and uses it to send a request to a proxy judge (a website that outputs the information that was sent to it). If the request succeeds, the proxy checker will use the information it receives from the proxy judge to determine the proxy's:

- Country
- Protocol
- Anonymity
- Speed

## Installation

```console
pip install proxy-checker
```

## Usage

```python3
from proxy_checker import ProxyChecker

checker = ProxyChecker()
checker.check_proxy('<ip>:<port>')
```

```json
{
  "country": "United States",
  "country_code": "US",
  "protocols": ["socks4", "socks5"],
  "anonymity": "Elite",
  "timeout": 1649
}
```

## Parameters

| Name          | Type | Default | Description                                          |
| ------------- | ---- | ------- | ---------------------------------------------------- |
| proxy         | str  |         | The proxy to test                                    |
| check_country | bool | True    | If `true`, the proxy's country will be looked up     |
| check_address | bool | False   | If `true`, the proxy's remote address will looked up |
| user          | str  | None    | The proxy's username                                 |
| password      | str  | None    | The proxy's password                                 |

## Requirements

- Python 3.\*
- [PycURL](http://pycurl.io/) - A Python interface to libcurl \*

###### \* If you have trouble installing PycURL on Windows, try to use Christoph Gohlke's collection of [Python Extension Package for Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE.md)
