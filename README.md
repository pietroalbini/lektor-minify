# lektor-minify-assets

This plugin allows you to minify the static assets of your [Lektor][lektor]
project directly from the build process, without any additional tool.

Internally it uses the [rcssmin][rcssmin] and [rjsmin][rjsmin] libraries, and
it's released under the MIT license.

## Installation

If you want to use lektor-minify-assets in your project, you can to execute
the following command in your Lektor project folder:

```
$ lektor plugins add lektor-minify-assets
```

After you did that, it's good to clear the build cache: the plugin only
minifies changed files, so clearing the cache ensures all the assets are
minified:

```
$ lektor clean --yes
```

## Usage

This plugin isn't enabled by default: you need to provide the `minify-assets`
flag to the `build` (or `server`) command if you want to minify the static
assets:

```
$ lektor build -f minify-assets
$ lektor server -f minify-assets
```

If you need to minify only CSS or JS though, you can either use the
`minify-css` or `minify-js` flags to avoid minifying the other kind of asset.

[lektor]: https://www.getlektor.com/
[rcssmin]: http://opensource.perlig.de/rcssmin/
[rjsmin]: http://opensource.perlig.de/rjsmin/
