# ELK Dashboard

[![CircleCI](https://circleci.com/gh/f213/elk-dashboard.svg?style=svg&circle-token=2ce041d53271e60d7afa4efc393f981684951089)](https://circleci.com/gh/f213/elk-dashboard) [![codecov](https://codecov.io/gh/f213/elk-dashboard/branch/master/graph/badge.svg?token=qDGzPnPA1v)](https://codecov.io/gh/f213/elk-dashboard)

## Configuration

Configuration is stored in `elk/.env`, for examples see `elk/.env.circle`, used during CI.

## Installing on a local machine

This project requires python3.7 <!-- TODO: use poetry/docker to avoid versioning errors, doesn't work with versions above 3.7 --> (i don't test it on python2). For frontend building you need to install Node.JS. I run tests on OS X and Linux (Circle CI), so the project should work on both systems.

```sh
pip install -r requirements.txt
npm install -g gulp bower
npm install
bower install
./build/download_geoip_db.sh
cp elk/.env.circle elk/.env
./manage.py loaddata crm lessons products teachers
```

<!-- FIXME: download_geoip_db.sh not working anymore, cz website returns 404 -->

<!-- FIXME: Probably we should add this to the script above, need to check if issue reproduced on other stuff members envs-->
In case of errors while installing libs with pip, see:
- [Error in anyjson setup command: use_2to3 is invalid](https://stackoverflow.com/questions/72414481/error-in-anyjson-setup-command-use-2to3-is-invalid)
- [libxml install error using pip](https://stackoverflow.com/questions/5178416/libxml-install-error-using-pip)

For always-actual bootstrap process please consider CI configuration.

Running a development host:

```sh
gulp&
./manage.py runserver
```

Production version is built via CircleCI — [![CircleCI](https://circleci.com/gh/f213/elk-dashboard.svg?style=svg&circle-token=2ce041d53271e60d7afa4efc393f981684951089)](https://circleci.com/gh/f213/elk-dashboard).

## Frontend

### CoffeeScript
All frontend programming should be done in [CoffeeScript](http://coffeescript.org). You can learn it in 3 hours, and it will save you nearly 30% of code by removing JS boilerplate. The price is a slightly bigger cognitive load, but the absence of the boilerplate worth it.

### Stylus
All CSS is written in Stylus. You event don't need to learn it — just omit everything boilerplate-like: `{`, `}` and `;`

### Global namespace
CoffeeScript has a built-in protector from polluting global namespace — it wraps every file like this:
```javascript
(function(){
    # your code here
})()
```
So you can't pollute global namespace even if you want it.
When you really need to publish something globally, you can use the `Project` object. It's ok to store Models, Controllers and Helpers there, like this:
```coffeescript
# model.coffee
class Model extends MicroEvent
    constructor (@a, @b, @c) ->
        # your wonerful code here

Project.Models.YourModel = Model

# later, in controller.coffee

class Controller
    constructor (@a, @b, @c ) ->
        @model = new Project.Models.YourModel @a, @b, @c
```

If you need a specific to an element peace of code, you should write a [simple jquery plugin](https://learn.jquery.com/plugins/basic-plugin-creation/).

### Local assets
By default all vendor assets, located it `build/js-vendor-filters.json` and `build/css-vendor-files.json` are cross-site. If you need a heavy library, you can include it with templatetags `css` and `js`, like this:
```django
{% block css %}
<link rel="stylesheet" href="{% static 'vendor/fullcalendar/dist/fullcalendar.min.css' %}">
{% endblock %}

{% block js %}
<script type="text/javascript" src="{% static 'vendor/fullcalendar/dist/fullcalendar.min.js' %}"></script>
{% endblock %}
```

## Coding style

Please use [flake8](https://pypi.python.org/pypi/flake8) for checking your python code. Imports should be sorted by [isort](https://github.com/timothycrosley/isort). For Stylus and CoffeeScript use stylint and coffeelint respectively (pre-configured in Gulp).

Configure your IDE with respect to [`.editorconfig`](http://editorconfig.org).

All comments and commit messages should be written in English.

Every model and model method should have a docstring.

All your code should be covered by tests.
