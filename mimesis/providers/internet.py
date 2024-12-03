"""Provides data related to internet."""
import typing as t
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode
from ipaddress import IPv4Address, IPv6Address
from mimesis.datasets import CONTENT_ENCODING_DIRECTIVES, CORS_OPENER_POLICIES, CORS_RESOURCE_POLICIES, HTTP_METHODS, HTTP_SERVERS, HTTP_STATUS_CODES, HTTP_STATUS_MSGS, PUBLIC_DNS, TLD, USER_AGENTS, USERNAMES
from mimesis.enums import DSNType, Locale, MimeType, PortRange, TLDType, URLScheme
from mimesis.providers.base import BaseProvider
from mimesis.providers.code import Code
from mimesis.providers.date import Datetime
from mimesis.providers.file import File
from mimesis.providers.text import Text
from mimesis.types import Keywords
__all__ = ['Internet']

class Internet(BaseProvider):
    """Class for generating data related to the internet."""
    _MAX_IPV4: t.Final[int] = 2 ** 32 - 1
    _MAX_IPV6: t.Final[int] = 2 ** 128 - 1

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize attributes.

        :param args: Arguments.
        :param kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._file = File(seed=self.seed, random=self.random)
        self._code = Code(seed=self.seed, random=self.random)
        self._text = Text(locale=Locale.EN, seed=self.seed, random=self.random)
        self._datetime = Datetime(locale=Locale.EN, seed=self.seed, random=self.random)

    class Meta:
        name = 'internet'

    def content_type(self, mime_type: MimeType | None=None) -> str:
        """Generates a random HTTP content type.

        :return: Content type.

        :Example:
            application/json
        """
        mime_type = self.validate_enum(mime_type, MimeType)
        return self._file.mime_type(type_=mime_type)

    def dsn(self, dsn_type: DSNType | None=None, **kwargs: t.Any) -> str:
        """Generates a random DSN (Data Source Name).

        :param dsn_type: DSN type.
        :param kwargs: Additional keyword-arguments for hostname method.
        """
        dsn_type = self.validate_enum(dsn_type, DSNType)
        hostname = self.hostname(**kwargs)
        port = self.port()
        
        if dsn_type == DSNType.POSTGRES:
            return f"postgresql://user:password@{hostname}:{port}/database"
        elif dsn_type == DSNType.MYSQL:
            return f"mysql://user:password@{hostname}:{port}/database"
        elif dsn_type == DSNType.MONGODB:
            return f"mongodb://user:password@{hostname}:{port}/database"
        else:
            return f"{dsn_type.value}://user:password@{hostname}:{port}/database"

    def http_status_message(self) -> str:
        """Generates a random HTTP status message.

        :return: HTTP status message.

        :Example:
            200 OK
        """
        return self.random.choice(HTTP_STATUS_MSGS)

    def http_status_code(self) -> int:
        """Generates a random HTTP status code.

        :return: HTTP status.

        :Example:
            200
        """
        return self.random.choice(HTTP_STATUS_CODES)

    def http_method(self) -> str:
        """Generates a random HTTP method.

        :return: HTTP method.

        :Example:
            POST
        """
        return self.random.choice(HTTP_METHODS)

    def ip_v4_object(self) -> IPv4Address:
        """Generates a random :py:class:`ipaddress.IPv4Address` object.

        :return: :py:class:`ipaddress.IPv4Address` object.
        """
        return IPv4Address(self.random.randint(0, self._MAX_IPV4))

    def ip_v4_with_port(self, port_range: PortRange=PortRange.ALL) -> str:
        """Generates a random IPv4 address as string.

        :param port_range: PortRange enum object.
        :return: IPv4 address as string.

        :Example:
            19.121.223.58:8000
        """
        ip = self.ip_v4()
        port = self.port(port_range)
        return f"{ip}:{port}"

    def ip_v4(self) -> str:
        """Generates a random IPv4 address as string.

        :Example:
            19.121.223.58
        """
        return str(self.ip_v4_object())

    def ip_v6_object(self) -> IPv6Address:
        """Generates random :py:class:`ipaddress.IPv6Address` object.

        :return: :py:class:`ipaddress.IPv6Address` object.
        """
        return IPv6Address(self.random.randint(0, self._MAX_IPV6))

    def ip_v6(self) -> str:
        """Generates a random IPv6 address as string.

        :return: IPv6 address string.

        :Example:
            2001:c244:cf9d:1fb1:c56d:f52c:8a04:94f3
        """
        return str(self.ip_v6_object())

    def mac_address(self) -> str:
        """Generates a random MAC address.

        :return: Random MAC address.

        :Example:
            00:16:3e:25:e7:f1
        """
        return ':'.join([f'{self.random.randint(0, 255):02x}' for _ in range(6)])

    @staticmethod
    def stock_image_url(width: int | str=1920, height: int | str=1080, keywords: Keywords | None=None) -> str:
        """Generates a random stock image URL hosted on Unsplash.

        See «Random search term» on https://source.unsplash.com/
        for more details.

        :param width: Width of the image.
        :param height: Height of the image.
        :param keywords: Sequence of search keywords.
        :return: URL of the image.
        """
        base_url = f"https://source.unsplash.com/random/{width}x{height}"
        if keywords:
            keyword_string = ','.join(keywords)
            return f"{base_url}?{urllib.parse.quote(keyword_string)}"
        return base_url

    def hostname(self, tld_type: TLDType | None=None, subdomains: list[str] | None=None) -> str:
        """Generates a random hostname without a scheme.

        :param tld_type: TLDType.
        :param subdomains: List of subdomains (make sure they are valid).
        :return: Hostname.
        """
        domain = self._text.word().lower()
        tld = self.top_level_domain(tld_type)
        
        if subdomains:
            subdomain = '.'.join(subdomains)
            return f"{subdomain}.{domain}.{tld}"
        return f"{domain}.{tld}"

    def url(self, scheme: URLScheme | None=URLScheme.HTTPS, port_range: PortRange | None=None, tld_type: TLDType | None=None, subdomains: list[str] | None=None) -> str:
        """Generates a random URL.

        :param scheme: The scheme.
        :param port_range: PortRange enum object.
        :param tld_type: TLDType.
        :param subdomains: List of subdomains (make sure they are valid).
        :return: URL.
        """
        scheme = self.validate_enum(scheme, URLScheme)
        hostname = self.hostname(tld_type, subdomains)
        url = f"{scheme.value}://{hostname}"
        
        if port_range:
            port = self.port(port_range)
            url += f":{port}"
        
        return url + self.path()

    def uri(self, scheme: URLScheme | None=URLScheme.HTTPS, tld_type: TLDType | None=None, subdomains: list[str] | None=None, query_params_count: int | None=None) -> str:
        """Generates a random URI.

        :param scheme: Scheme.
        :param tld_type: TLDType.
        :param subdomains: List of subdomains (make sure they are valid).
        :param query_params_count: Query params.
        :return: URI.
        """
        url = self.url(scheme, tld_type=tld_type, subdomains=subdomains)
        if query_params_count:
            params = self.query_parameters(query_params_count)
            query_string = urllib.parse.urlencode(params)
            return f"{url}?{query_string}"
        return url

    def query_string(self, length: int | None=None) -> str:
        """Generates an arbitrary query string of given length.

        :param length: Length of query string.
        :return: Query string.
        """
        if length is None:
            length = self.random.randint(1, 10)
        
        params = self.query_parameters(length)
        return urllib.parse.urlencode(params)

    def query_parameters(self, length: int | None=None) -> dict[str, str]:
        """Generates an arbitrary query parameters as a dict.

        :param length: Length of query parameters dictionary (maximum is 32).
        :return: Dict of query parameters.
        """
        if length is None:
            length = self.random.randint(1, 10)
        length = min(length, 32)
        
        params = {}
        for _ in range(length):
            key = self._text.word().lower()
            value = self._text.word().lower()
            params[key] = value
        
        return params

    def top_level_domain(self, tld_type: TLDType=TLDType.CCTLD) -> str:
        """Generates random top level domain.

        :param tld_type: Enum object :class:`enums.TLDType`
        :return: Top level domain.
        :raises NonEnumerableError: if tld_type not in :class:`enums.TLDType`.
        """
        tld_type = self.validate_enum(tld_type, TLDType)
        return self.random.choice(TLD[tld_type.value])

    def tld(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random TLD.

        An alias for :meth:`top_level_domain`
        """
        return self.top_level_domain(*args, **kwargs)

    def user_agent(self) -> str:
        """Get a random user agent.

        :return: User agent.

        :Example:
            Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)
            Gecko/20100101 Firefox/15.0.1
        """
        return self.random.choice(USER_AGENTS)

    def port(self, port_range: PortRange=PortRange.ALL) -> int:
        """Generates a random port.

        :param port_range: PortRange enum object.
        :return: Port number.
        :raises NonEnumerableError: if port_range is not in PortRange.

        :Example:
            8080
        """
        port_range = self.validate_enum(port_range, PortRange)
        if port_range == PortRange.ALL:
            return self.random.randint(1, 65535)
        elif port_range == PortRange.EPHEMERAL:
            return self.random.randint(49152, 65535)
        elif port_range == PortRange.REGISTERED:
            return self.random.randint(1024, 49151)
        else:  # PortRange.WELL_KNOWN
            return self.random.randint(1, 1023)

    def path(self, *args: t.Any, **kwargs: t.Any) -> str:
        """Generates a random path.

        :param args: Arguments to pass to :meth:`slug`.
        :param kwargs: Keyword arguments to pass to :meth:`slug`.
        :return: Path.
        """
        return f"/{self.slug(*args, **kwargs)}"

    def slug(self, parts_count: int | None=None) -> str:
        """Generates a random slug of given parts count.

        :param parts_count: Slug's parts count.
        :return: Slug.
        """
        if parts_count is None:
            parts_count = self.random.randint(1, 5)
        
        words = self._text.words(quantity=parts_count)
        return '-'.join(word.lower() for word in words)

    def public_dns(self) -> str:
        """Generates a random public DNS.

        :Example:
            1.1.1.1
        """
        return self.random.choice(PUBLIC_DNS)

    def http_response_headers(self) -> dict[str, t.Any]:
        """Generates a random HTTP response headers.

        The following headers are included:

        - Allow
        - Age
        - Server
        - Content-Type
        - X-Request-ID
        - Content-Language
        - Content-Location
        - Set-Cookie
        - Upgrade-Insecure-Requests
        - X-Content-Type-Options
        - X-XSS-Protection
        - Connection
        - X-Frame-Options
        - Content-Encoding
        - Cross-Origin-Opener-Policy
        - Cross-Origin-Resource-Policy
        - Strict-Transport-Security

        :return: Response headers as dict.
        """
        headers = {
            'Allow': ', '.join(self.random.sample(HTTP_METHODS, k=self.random.randint(1, len(HTTP_METHODS)))),
            'Age': str(self.random.randint(1, 1000)),
            'Server': self.random.choice(HTTP_SERVERS),
            'Content-Type': self.content_type(),
            'X-Request-ID': self._code.pin(mask='##################'),
            'Content-Language': self._code.locale_code(),
            'Content-Location': self.path(),
            'Set-Cookie': f'session_id={self._code.pin(mask="##########")}; Secure; HttpOnly',
            'Upgrade-Insecure-Requests': '1',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Connection': self.random.choice(['keep-alive', 'close']),
            'X-Frame-Options': self.random.choice(['DENY', 'SAMEORIGIN']),
            'Content-Encoding': self.random.choice(CONTENT_ENCODING_DIRECTIVES),
            'Cross-Origin-Opener-Policy': self.random.choice(CORS_OPENER_POLICIES),
            'Cross-Origin-Resource-Policy': self.random.choice(CORS_RESOURCE_POLICIES),
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload'
        }
        return headers

    def http_request_headers(self) -> dict[str, t.Any]:
        """Generates a random HTTP request headers.

        The following headers are included:

        - Referer
        - Authorization
        - Cookie
        - User-Agent
        - X-CSRF-Token
        - Content-Type
        - Content-Length
        - Connection
        - Cache-Control
        - Accept
        - Host
        - Accept-Language

        :return: Request headers as dict.
        """
        headers = {
            'Referer': self.url(),
            'Authorization': f'Bearer {b64encode(self._text.word().encode()).decode()}',
            'Cookie': f'session_id={self._code.pin(mask="##########")}',
            'User-Agent': self.user_agent(),
            'X-CSRF-Token': self._code.pin(mask='################'),
            'Content-Type': self.content_type(),
            'Content-Length': str(self.random.randint(100, 10000)),
            'Connection': self.random.choice(['keep-alive', 'close']),
            'Cache-Control': self.random.choice(['no-cache', 'max-age=0', 'max-age=3600']),
            'Accept': '*/*',
            'Host': self.hostname(),
            'Accept-Language': f'{self._code.locale_code()},en-US;q=0.9,en;q=0.8'
        }
        return headers
