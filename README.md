# lektor-minify

This plugin allows you to minify the build artifacts of your [Lektor][lektor]
project during the build process, without any additional tool. It currently
supports minifying HTML, CSS and JS files.

The plugin only minifies the files changed during the last build, avoiding
slowing down the build if your project consists of a lot of files. Internally
it uses the [django_htmlmin][htmlmin], [rcssmin][rcssmin] and [rjsmin][rjsmin]
libraries, and it's released under the MIT license.

## Installation

If you want to use lektor-minify in your project, you can to execute the
following command in your Lektor project folder:

```
$ lektor plugins add lektor-minify
```

After you did that, it's good to clear the build cache: the plugin only
minifies changed files, so clearing the cache ensures all the assets are
minified:

```
$ lektor clean --yes
```

## Usage

This plugin isn't enabled by default: you need to provide the `minify` flag to
the `build` (or `server`) command if you want to minify the build artifacts:

```
$ lektor build -f minify
$ lektor server -f minify
```

If you need to minify only some kind of artifacts, you can tell which ones you
want to minify by providing their kinds as a comma-separated list in the flag:

```
$ lektor build -f minify:html
$ lektor build -f minify:html,css,js
```

Keep in mind only artifacts built with the flag will be minified: if you
execute other builds without the flag there might be some unminified files!

## Testing

Some basic tests are available for the project. If you want to run them clone
the repository, install Lektor and run:

```
tests/test.sh
```

[lektor]: https://www.getlektor.com/
[rcssmin]: http://opensource.perlig.de/rcssmin/
[rjsmin]: http://opensource.perlig.de/rjsmin/
[htmlmin]: https://github.com/cobrateam/django-htmlmin
