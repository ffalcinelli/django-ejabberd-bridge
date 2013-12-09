# django_ejabberd_bridge [![Build Status](https://travis-ci.org/ffalcinelli/django-ejabberd-bridge.png)](https://travis-ci.org/ffalcinelli/django-ejabberd-bridge) [![Coverage Status](https://coveralls.io/repos/ffalcinelli/django-ejabberd-bridge/badge.png)](https://coveralls.io/r/ffalcinelli/django-ejabberd-bridge) 

It's a django app to integrate [ejabberd](http://www.ejabberd.im/) XMPP server with [Django](https://www.djangoproject.com/)

Right now it just allows the ejabberd service to perform authentication against Django's authentication middleware. This part is based on the guidelines provided by Alexey Shchepin <alexey@sevcom.net> on the eJabberd developer's guide.

## Quick Start


Install django_ejabberd_bridge with the following

```
$ python setup.py install
```

TODO: add quick starts here...


## Install and startup eJabberd

On a debian/ubuntu linux you can use

```
$ apt-get -y install ejabberd
$ service ejabberd restart
```

whereas on OSX using [homebrew](http://brew.sh/)

```
$ brew install ejabberd
$ ejabberdctl restart
```

### Setup Admin User

* Change "password" to your own value:

```
$ ejabberdctl register admin localhost password
```

* Give Admin Privileges. By default, hostname used by eJabberd is 'localhost', which can be modified from config file.
For our example we will call our admin user "admin@localhost" and modify the following lines in `/etc/ejabberd/ejabberd.cfg` (`/usr/local/etc/ejabberd/ejabberd.cfg` if you're using homebrew):


```
%% Admin user
{acl, admin, {user, "admin", "localhost"}}.

%% Hostname
{hosts, ["localhost"]}.
```

### Configure external authentication

On eJabberd you can configure several authentication methods. For our integration purpose we must select "external" and provide the path to our script. 

```
%%
%% Authentication using external script
%% Make sure the script is executable by ejabberd.
%%
{auth_method, external}.
{extauth_program, "/path/to/authentication/script"}.
```

Since a virtualenv is commonly used while dealing with python projects, we could write a script that enables the virtualenv and calls the django command to perform authentication, e.g. we could use an authentication script like these:

```
#!/bin/bash
source <virtualenv_path>/bin/activate
python <django_project_path>/manage.py ejabberd_auth $@
```

### Restart eJabberd

If a service is provided you can use

```
$ service ejabberd restart
```
Or if available

```
$ ejabberdctl restart
```

Now, you can access ejabberd admin page at the url
 
http://localhost:5280/admin

# TODO

1. Simplify configuration by providing the script
2. Write down a page specifically for eJabberd

# License

LGPLv3

Copyright (c) 2013 Fabio Falcinelli <fabio.falcinelli@gmail.com>

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU Lesser General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU Lesser General Public License for more details.
>
> You should have received a copy of the GNU Lesser General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.