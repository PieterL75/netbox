# Authentication

## Local Authentication

Local user accounts and groups can be created in NetBox under the "Authentication" section in the "Admin" menu. This section is available only to users with the "staff" permission enabled.

At a minimum, each user account must have a username and password set. User accounts may also denote a first name, last name, and email address. [Permissions](../permissions.md) may also be assigned to individual users and/or groups as needed.

## Remote Authentication

NetBox may be configured to provide user authenticate via a remote backend in addition to local authentication. This is done by setting the `REMOTE_AUTH_BACKEND` configuration parameter to a suitable backend class. NetBox provides several options for remote authentication.

### LDAP Authentication

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.LDAPBackend'
```

NetBox includes an authentication backend which supports LDAP. See the [LDAP installation docs](../../installation/6-ldap.md) for more detail about this backend.

### HTTP Header Authentication

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.RemoteUserBackend'
```

Another option for remote authentication in NetBox is to enable HTTP header-based user assignment. The front end HTTP server (e.g. nginx or Apache) performs client authentication as a process external to NetBox, and passes information about the authenticated user via HTTP headers. By default, the user is assigned via the `REMOTE_USER` header, but this can be customized via the `REMOTE_AUTH_HEADER` configuration parameter.

Optionally, user profile information can be supplied by `REMOTE_USER_FIRST_NAME`, `REMOTE_USER_LAST_NAME` and `REMOTE_USER_EMAIL` headers. These are saved to the user's profile during the authentication process. These headers can be customized like the `REMOTE_USER` header.

!!! warning Verify Header Compatibility
    Some WSGI servers may drop headers which contain unsupported characters. For instance, gunicorn v22.0 and later silently drops HTTP headers containing underscores. This behavior can be disabled by changing gunicorn's [`header_map`](https://docs.gunicorn.org/en/stable/settings.html#header-map) setting to `dangerous`.

### Single Sign-On (SSO)

```python
REMOTE_AUTH_BACKEND = 'social_core.backends.google.GoogleOAuth2'
```

NetBox supports single sign-on authentication via the [python-social-auth](https://github.com/python-social-auth) library. To enable SSO, specify the path to the desired authentication backend within the `social_core` Python package. Please see the complete list of [supported authentication backends](https://github.com/python-social-auth/social-core/tree/master/social_core/backends) for the available options.

Most remote authentication backends require some additional configuration through settings prefixed with `SOCIAL_AUTH_`. These will be automatically imported from NetBox's `configuration.py` file. Additionally, the [authentication pipeline](https://python-social-auth.readthedocs.io/en/latest/pipeline.html) can be customized via the `SOCIAL_AUTH_PIPELINE` parameter. (NetBox's default pipeline is defined in `netbox/settings.py` for your reference.)

#### Configuring the SSO module's appearance

The way a remote authentication backend is displayed to the user on the login
page may be adjusted via the `SOCIAL_AUTH_BACKEND_ATTRS` parameter, defaulting
to an empty dictionary. This dictionary maps a `social_core` module's name (ie.
`REMOTE_AUTH_BACKEND.name`) to a couple of parameters, `(display_name, icon)`.

The `display_name` is the name displayed to the user on the login page. The
icon may either be the URL of an icon; refer to a [Material Design
Icons](https://github.com/google/material-design-icons) icon's name; or be
`None` for no icon.

For instance, the OIDC backend may be customized with

```python
SOCIAL_AUTH_BACKEND_ATTRS = {
    'oidc': ("My awesome SSO", "login"),
}
```
