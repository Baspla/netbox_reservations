from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


reservation_buttons = [
    PluginMenuButton(
        link='plugins:netbox_reservations:reservation_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["netbox_reservations.add_claim"]
    )
]

claim_buttons = [
    PluginMenuButton(
        link='plugins:netbox_reservations:claim_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["netbox_reservations.add_reservation"]
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_reservations:reservation_list',
        link_text='Reservations',
        buttons=reservation_buttons,
        permissions=["netbox_reservations.view_reservation"]
    ),
    PluginMenuItem(
        link='plugins:netbox_reservations:claim_list',
        link_text='Claims',
        buttons=claim_buttons,
        permissions=["netbox_reservations.view_claim"]
    ),
)
