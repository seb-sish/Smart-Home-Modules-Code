_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)
_safe_quoters = {}


class Quoter(dict):
    def __init__(self, safe):
        self.safe = _ALWAYS_SAFE.union(safe)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, dict(self))

    def __missing__(self, b):
        res = chr(b) if b in self.safe else '%{:02X}'.format(b)
        self[b] = res
        return res

    def __getitem__(self, item):
        return self.get(item, self.__missing__(item))


def quote_plus(string, safe='', encoding=None, errors=None):
    if ((isinstance(string, str) and ' ' not in string) or
            (isinstance(string, bytes) and b' ' not in string)):
        return quote(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '
    string = quote(string, safe + space, encoding, errors)
    return string.replace(' ', '+')


def quote(string, safe='/', encoding=None, errors=None):
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)


def quote_from_bytes(bs, safe='/'):
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError("quote_from_bytes() expected bytes")
    if not bs:
        return ''
    if isinstance(safe, str):
        safe = safe.encode('ascii', 'ignore')
    else:
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    try:
        quoter = _safe_quoters[safe]
    except KeyError:
        _safe_quoters[safe] = quoter = Quoter(safe).__getitem__
    return ''.join([quoter(char) for char in bs])


def urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus):
    if hasattr(query, "items"):
        query = query.items()
    else:
        try:
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError

        except TypeError as e:
            print(e)
    l = []
    for k, v in query:
        if isinstance(k, bytes):
            k = quote_via(k, safe)
        else:
            k = quote_via(str(k), safe, encoding, errors)
        if isinstance(v, bytes):
            v = quote_via(v, safe)
            l.append(k + '=' + v)
        elif isinstance(v, str):
            v = quote_via(v, safe, encoding, errors)
            l.append(k + '=' + v)
        else:
            try:
                x = len(v)
            except TypeError:
                v = quote_via(str(v), safe, encoding, errors)
                l.append(k + '=' + v)
            else:
                for elt in v:
                    if isinstance(elt, bytes):
                        elt = quote_via(elt, safe)
                    else:
                        elt = quote_via(str(elt), safe, encoding, errors)
                    l.append(k + '=' + elt)
    return '&'.join(l)