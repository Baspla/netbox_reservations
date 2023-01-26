from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


workspace_buttons = [
    PluginMenuButton(
        link='plugins:netbox_workspaces:workspace_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_workspaces.add_workspace"],
        color=ButtonColorChoices.GREEN
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_workspaces:workspace_list',
        link_text='Workspaces',
        buttons=workspace_buttons,
        permissions=["netbox_workspaces.view_workspace"]
    ),
)
