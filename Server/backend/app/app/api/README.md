# REST Api Design

## Security

The API is divided into a user, gateway and admin api.
This distinction enables to ensure that the administration endpoints with access to all data always require the
administration priveledges.
It is still important to ensure only the data of the user is accessable by the crud operation.
The gateway api is accessable only by the gateway with the gateway access token.

## Parameter

### POST

The IDs of **POST** requests should be included in the json data.
This has the advantage that only one place has to be manipulated on client.
Furthermore only one passing of parameter gives clarity and avoids situations where parameters dont match.

### GET

**GET** requests have the parameters in the path to avoid unessesary payload.

