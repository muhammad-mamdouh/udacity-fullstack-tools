# BOOKMARK SERVER, or URL-shortening service
similar to `TinyURL.com` or `goo.gl`, but with no persistent storage.

### How it generally works:
This server will accept a URL and a short name, check that the URL actually
works (returns an HTTP 200), it maintains a mapping (dictionary) between
the URL and the short name.

![Bookmark Server](https://user-images.githubusercontent.com/13325802/58197198-0b85c700-7ccc-11e9-9e9a-747801739d1c.png)

    