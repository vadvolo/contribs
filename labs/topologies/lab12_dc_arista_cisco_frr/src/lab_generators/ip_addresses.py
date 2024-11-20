from ipaddress import IPv4Address, IPv4Network

from annet.generators import PartialGenerator
from annet.storage import Device

from .helpers.router import bgp_mesh


class IpAddresses(PartialGenerator):
    """Partial generator class of IPv4 and IPv6 addresses on interfaces"""

    TAGS = ["l3", "iface"]

    def acl_cisco(self, _: Device):
        """ACL for Cisco devices"""

        return """
        interface
            ip address
            ipv6 address
        """

    def run_cisco(self, device: Device):
        """Generator for Cisco devices"""

        # enrich interfaces by mesh
        bgp_mesh(device)
        for interface in device.interfaces:
            if interface.ip_addresses:
                # structure of ip addresses looks like:
                #  ip_addresses=[
                #       IpAddress(family=IpFamily(value=4,label='IPv4'),address='10.0.0.1/32'),
                #       IpAddress(family=IpFamily(value=6,label='IPv6'),address='2001:db8::1/128')
                #  ],
                with self.block(f"interface {interface.name}"):
                    for ip_address in interface.ip_addresses:
                        if ip_address.family.value == 4:
                            ip_addr: str = str(IPv4Address(ip_address.address.split("/")[0]))
                            ip_mask: str = str(IPv4Network(ip_address.address, strict=False).netmask)
                            yield "ip address", ip_addr, ip_mask

    def acl_arista(self, _: Device):
        """ACL for Arista devices"""
        return """
        interface
            ip address
            ipv6 address
        """

    def run_arista(self, device: Device):
        """Generator for Arista devices"""

        # enrich interfaces by mesh
        bgp_mesh(device)
        for interface in device.interfaces:
            if interface.ip_addresses:
                # structure of ip addresses looks like:
                #  ip_addresses=[
                #       IpAddress(family=IpFamily(value=4,label='IPv4'),address='10.0.0.1/32'),
                #       IpAddress(family=IpFamily(value=6,label='IPv6'),address='2001:db8::1/128')
                #  ],
                with self.block(f"interface {interface.name}"):
                    ip_addr_set: set[tuple[str, int]] = set()
                    for ip_address in interface.ip_addresses:
                        if ip_address.family.value == 4:
                            yield "ip address", ip_address.address
