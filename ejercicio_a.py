from ncclient import manager
from lxml import etree

router_ip = "192.168.5.129"
port = 830
username = "cisco"
password = "cisco123!"

loopback_config = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>6</name>
                <ip>
                    <address>
                        <primary>
                            <address>10.10.1.6</address>
                            <mask>255.255.0.0</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

route_config = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
            <route>
                <ip-route-interface-forwarding-list>
                    <prefix>0.0.0.0</prefix>
                    <mask>0.0.0.0</mask>
                    <fwd-list>
                        <fwd>Loopback6</fwd>
                    </fwd-list>
                </ip-route-interface-forwarding-list>
            </route>
        </ip>
    </native>
</config>
"""

def configure_router():
    with manager.connect(
        host=router_ip,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False,
    ) as m:
        m.edit_config(target="running", config=loopback_config)
        print("Interfaz Loopback6 configurada correctamente.")
        m.edit_config(target="running", config=route_config)
        print("Ruta predeterminada configurada correctamente.")
        get_routes(m)
def get_routes(m):
    routes_filter = """
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <ip>
                <route>
                    <ip-route-interface-forwarding-list>
                        <prefix>0.0.0.0</prefix>
                        <mask>0.0.0.0</mask>
                    </ip-route-interface-forwarding-list>
                </route>
            </ip>
        </native>
    </filter>
    """
    response = m.get(filter=("subtree", routes_filter))
    routes_xml = etree.tostring(response.data, pretty_print=True).decode()
    print("\nTabla de rutas actual:")
    print(routes_xml)

if __name__ == "__main__":
    configure_router()