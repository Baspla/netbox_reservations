from extras.plugins import PluginConfig


class NetBoxReservationsConfig(PluginConfig):
    name = 'netbox_reservations'
    verbose_name = 'NetBox Reservations'
    description = 'Manage reservations in NetBox'
    version = '0.1'
    base_url = 'reservations'


config = NetBoxReservationsConfig
