# Proxy Checker (Python)

A proxy checker in Python using PycURL, a Python interface to libcurl.

## Description

The proxy checker takes a proxy as input and use it to send a request to a proxy judge (a website that outputs the information that was sent to it). If the request succeeds, the proxy checker will use the information it receive from the proxy judge to determine the proxy's:

- Country
- Protocol
- Anonymity
- Speed

## Usage

```python3
checker = ProxyChecker()
checker.check_proxy('<ip>:<port>')
```

```json
{
  "country": "United States",
  "country_code": "US",
  "protocols": [
    "socks4",
    "socks5"
  ],
  "anonymity": "Elite",
  "timeout": 1649
}
```

## Requirements

- Python 3.*
- [PycURL](http://pycurl.io/) - A Python interface to libcurl *

###### \* If you have trouble installing PycURL on Windows, try to use Christoph Gohlke's collection of [Python Extension Package for Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE.md)
