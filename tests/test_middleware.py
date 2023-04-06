from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.test import RequestFactory, TestCase, override_settings

from cidr import middleware


class TestMiddleware(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def _get_middleware(self):
        return middleware.CIDRMiddleware(get_response=lambda *args, **kwargs: None)


class TestGoodCIDRMiddleware(TestMiddleware):
    @override_settings(CIDR_ALLOWED_HOSTS=["172.16.0.0/16"])
    def test_allowed_cidr_subnet(self):
        middleware = self._get_middleware()

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4:1234"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="172.15.255.255"))

        middleware(self.request_factory.get("/", HTTP_HOST="172.16.0.0"))
        middleware(self.request_factory.get("/", HTTP_HOST="172.16.0.255:80"))
        middleware(self.request_factory.get("/", HTTP_HOST="172.16.255.255"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="172.17.0.0"))

    @override_settings(ALLOWED_HOSTS=["domain.com"])
    def test_allowing_only_particular_domain(self):
        middleware = self._get_middleware()

        middleware(self.request_factory.get("/", HTTP_HOST="domain.com"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="example.com"))

    @override_settings(CIDR_ALLOWED_HOSTS=["1.2.3.4/32"])
    def test_allowing_particular_ip(self):
        middleware = self._get_middleware()

        middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.5"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="example.com"))

    @override_settings(CIDR_ALLOWED_HOSTS=["0.0.0.0/0"])
    def test_allow_all_via_cidr(self):
        middleware = self._get_middleware()

        middleware(self.request_factory.get("/", HTTP_HOST="1.1.1.1"))
        middleware(self.request_factory.get("/", HTTP_HOST="3.4.5.6"))
        middleware(self.request_factory.get("/", HTTP_HOST="254.254.254.254"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="example.com"))

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_allow_all_via_asterisk(self):
        middleware = self._get_middleware()

        middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4"))
        middleware(self.request_factory.get("/", HTTP_HOST="example.com"))

    @override_settings(
        ALLOWED_HOSTS=["domain.com", "example.com"],
        CIDR_ALLOWED_HOSTS=["10.0.0.0/8", "172.16.32.0/24"],
    )
    def test_mixed_configuration(self):
        middleware = self._get_middleware()

        middleware(self.request_factory.get("/", HTTP_HOST="domain.com"))
        middleware(self.request_factory.get("/", HTTP_HOST="example.com"))
        middleware(self.request_factory.get("/", HTTP_HOST="10.0.0.1"))
        middleware(self.request_factory.get("/", HTTP_HOST="172.16.32.100"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="other.com"))

        with self.assertRaises(DisallowedHost):
            middleware(self.request_factory.get("/", HTTP_HOST="1.2.3.4"))


class TestBadCIDRMiddleware(TestMiddleware):
    @override_settings(ALLOWED_HOSTS=["*"], CIDR_ALLOWED_HOSTS=["0.0.0.0/0"])
    def test_wrong_configuration_using_both_allowed_hosts(self):
        with self.assertRaises(MiddlewareNotUsed):
            self._get_middleware()

    @override_settings(CIDR_ALLOWED_HOSTS=["1.2.3.4/-1"])
    def test_wrong_mask(self):
        with self.assertRaises(ValueError):
            self._get_middleware()

    @override_settings(CIDR_ALLOWED_HOSTS=["1,2,3.4/32"])
    def test_wrong_ip(self):
        with self.assertRaises(ValueError):
            self._get_middleware()
