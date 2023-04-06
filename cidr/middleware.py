from django.conf import settings
from django.core.exceptions import DisallowedHost, MiddlewareNotUsed
from django.http.request import validate_host

ORIGINAL_ALLOWED_HOSTS = []


class CIDRMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        if (
            "*" in settings.ALLOWED_HOSTS
            and getattr(settings, "CIDR_ALLOWED_HOSTS", []) != []
        ):
            raise MiddlewareNotUsed("ALLOWED_HOSTS is set to allow all hosts")

        for subnet in getattr(settings, "CIDR_ALLOWED_HOSTS", []):
            if "/" not in subnet:
                raise MiddlewareNotUsed(
                    f"Invalid CIDR subnet {subnet} in CIDR_ALLOWED_HOSTS"
                )
            address, mask = subnet.split("/")

            if not self._is_valid_subnet_mask(mask):
                raise ValueError(f"Invalid subnet mask {mask} in CIDR subnet")

            if not self._is_valid_ipv4_address(address):
                raise ValueError(f"Invalid IP address {address} in CIDR subnet")

        if "*" not in settings.ALLOWED_HOSTS:
            ORIGINAL_ALLOWED_HOSTS.extend(settings.ALLOWED_HOSTS)
            settings.ALLOWED_HOSTS = ["*"]

    def _validate_cidr_subnet(self, host, subnet):
        host_parts = host.split(".")
        subnet_parts = subnet.split("/")
        mask = int(subnet_parts[1])
        host_in_binary = "".join([f"{int(part):08b}" for part in host_parts])
        subnet_in_binary = "".join(
            [f"{int(part):08b}" for part in subnet_parts[0].split(".")]
        )
        return host_in_binary[:mask] == subnet_in_binary[:mask]

    def _is_valid_ipv4_address(self, host):
        parts = host.split(".")

        if len(parts) != 4:
            return False

        return all(
            [part.isdigit() and int(part) >= 0 and int(part) <= 255 for part in parts]
        )

    def _is_valid_subnet_mask(self, mask):
        return mask.isdigit() and int(mask) >= 0 and int(mask) <= 32

    def _validate_cidr_subnets(self, host):
        if not self._is_valid_ipv4_address(host):
            return False

        return any(
            self._validate_cidr_subnet(host, subnet)
            for subnet in getattr(settings, "CIDR_ALLOWED_HOSTS", [])
        )

    def __call__(self, request):
        host = request.get_host()
        address, _ = host.split(":") if ":" in host else (host, None)

        if not validate_host(
            address, ORIGINAL_ALLOWED_HOSTS or settings.ALLOWED_HOSTS
        ) and not self._validate_cidr_subnets(address):
            raise DisallowedHost(
                f"Invalid HTTP_HOST header: {address}. You may need to add {address} to ALLOWED_HOSTS."
            )

        return self.get_response(request)
