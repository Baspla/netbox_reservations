# Netbox Ressource Management - Documentation

## Introduction

This plugin provides a simple way to manage resources in Netbox.
Any entry in recorded in Netbox can be reserved for a specific time period.
This can be used to manage what teams are working on what devices, or to prevent
double or idle bookings of a rack.

## User Guide

This part of the documentation is intended for users of the plugin.

### Concepts

This section aims to explain the concepts of the plugin.

#### Reservations

A reservation is a time period for which a set of resources is reserved.
All reservations are associated with a tenant and a contact person.
The reservation can be in one of the following states:
- `Draft`: The reservation is not yet confirmed.
- `Planned`: The reservation is confirmed but not yet started.
- `Active`: The reservation is currently active.
- `Overdue`: The reservation is overdue.

The start and end date of the reservation can be changed at any time.
Changes to the dates will be validated against other reservations to make sure that no conflicts occur.
If a reservation is set to `Is Draft` it only changes the status to `Planned`, no other changes occur.
Claims, related to the reservation, can be added to the reservation after it has been created.

#### Claims

Claims are used to specify which resources are reserved for a specific reservation.
To reduce the complexity of the plugin, claims are not directly associated with every ressource.
Instead, claims are associated with tags. Almost every ressource in Netbox has a tag field.
This way a claim can be used to link a reservation to a specific set of resources.

Here is a visual representation of the concept:

```
+-----------------+     +-----------------+     +-----------------+     +-----------------+
|                 | 1:n |                 | n:1 |                 | n:n |                 |
|   Reservation   | --- |      Claim      | --- |       Tag       | --- |    Ressource    |
|                 |     |                 |     |                 |     |                 |
+-----------------+     +-----------------+     +-----------------+     +-----------------+
```

### Usage

This section describes how to use the plugin.

#### Creating a new Reservation

To create a new reservation, click on the `Reservations` entry in the `Reservations` tab in the navigation bar.
This will open the list of all reservations. Click on the `+ Add` button in the top right corner to create a new reservation.

To create a new reservation, you need to specify the following information:

- **Name**: The name of the reservation. This is a required field.
- Description: A description of the reservation. This is an optional field.
- **Contact**: The contact person for the reservation. This is a required field.
- **Tenant**: The tenant for the reservation. This is a required field.
- **Start Date**: The start date of the reservation. This is a required field.
- **End Date**: The end date of the reservation. This is a required field.
- Is Draft: If this is checked, the reservation status will be set to `Draft`. This is an optional field.
- Tags: A list of tags for the reservation. This is an optional field.

⚠️ Important! The tags field is not the same as a claim and just a way to tag this entry!


#### Creating a new Claim

To create a new claim you have several options
1. Click on the `Claims` entry in the `Reservations` tab in the navigation bar.
This will open the list of all claims. Click on the `+ Add` button in the top right corner to create a new claim.
2. Open the detail view of a reservation and click on the `+ Add Claim` button in the `Claims` section.

To create a new claim, you need to specify the following information:

- **Reservation**: The reservation for the claim. This is a required field.
- **Tag**: The tag for the claim. This is a required field.
- **Restriction**: The restriction for the claim. Either `exclusive` or `shared`. This is a required field.
- Description: A description of the claim. This is an optional field.
- Tags: A list of tags for the claim. This is an optional field.

⚠️ Important! The Tags field is not the same as the required tag field and just a way to tag this entry!

## Admin Guide

This part of the documentation is intended for administrators of the netbox instance.

#### Requirements

The plugin requires no additional software to be installed except for the netbox instance itself.

- Python 3.6 or higher
- Netbox 2.6 or higher

### Installation

To install the plugin, follow the instructions in the [Netbox documentation](https://netbox.readthedocs.io/en/stable/plugins/).
Here is a quick summary:

#### Clone the repository

Clone or copy the repository into the `plugins` directory of your Netbox installation

#### Enable the plugin

In `configuration.py`, add the plugin's name to the `PLUGINS` list:

```python
PLUGINS = [
    'plugin_name',
]
```

#### Run database migrations
If the plugin introduces new database models, run the provided schema migrations:

```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
```

#### Restart WSGI Service
Restart the WSGI service to load the new plugin:

```bash
 sudo systemctl restart netbox
```


### Configuration

The plugin does not require any configuration and currently does not provide any configuration options.

### Permissions

The plugin introduces the following permissions:

#### Reservation

- `netbox_reservations.view_reservation`
- `netbox_reservations.add_reservation`
- `netbox_reservations.change_reservation`
- `netbox_reservations.delete_reservation`

#### Claim

- `netbox_reservations.view_claim`
- `netbox_reservations.add_claim`
- `netbox_reservations.change_claim`
- `netbox_reservations.delete_claim`

## Troubleshooting & FAQ

Here are some common issues and how to solve them.

### I get an error when trying to create/view/edit/delete a reservation/claim

This is most likely due to missing permissions. Make sure that the user has the correct permissions.
