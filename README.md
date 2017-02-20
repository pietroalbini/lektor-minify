## lektor-minify-assets

This package allows you to minify the static assets of your [Lektor][lektor]
website directly from the build process, without any additional tool.

Internally it uses the [rcssmin][rcssmin] and [rjsmin][rjsmin] libraries, and
it's released under the MIT license.

### Installation

If you want to use lektor-minify-assets in your project, you can to execute
the following command in your Lektor project folder:

```
$ lektor plugins add lektor-minify-assets
```

If you don't feel comfortable with this, you can add this by hand in your
`.lektorproject` file instead:

```
[packages]
lektor-minify-assets = "1.0"
```

### Usage

If you want to make a build with minified assets, you need to provide the
`minify-assets` flag to the `build` (or `server`) command:

```
$ lektor build -f minify-assets
$ lektor server -f minify-assets
```

If you need to minify just the CSS or JS files though, you can use either the
`minify-css` or `minify-js` flags instead.

[lektor]: https://www.getlektor.com/
[rcssmin]: http://opensource.perlig.de/rcssmin/
[rjsmin]: http://opensource.perlig.de/rjsmin/
