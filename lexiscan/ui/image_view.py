"""Widget for displaying ARASAAC pictograms."""

import threading
import urllib.request

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import GdkPixbuf, Gio, GLib, Gtk

from lexiscan.utils.i18n import _


class ImageView(Gtk.Box):
    """Displays pictogram images from ARASAAC."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        self._title = Gtk.Label(label=_("Image support (ARASAAC)"))
        self._title.add_css_class("heading")
        self._title.set_halign(Gtk.Align.START)
        self.append(self._title)

        self._flow = Gtk.FlowBox()
        self._flow.set_max_children_per_line(4)
        self._flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self._flow.set_homogeneous(True)
        self.append(self._flow)

        self.set_visible(False)

    def update(self, images):
        """Update view with image results."""
        # Clear existing
        while child := self._flow.get_first_child():
            self._flow.remove(child)

        if not images:
            self.set_visible(False)
            return

        self.set_visible(True)
        for img in images[:4]:
            self._load_image_async(img)

    def _load_image_async(self, image_result):
        """Load an image asynchronously."""
        # Placeholder with spinner
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        spinner = Gtk.Spinner()
        spinner.set_size_request(96, 96)
        spinner.start()
        box.append(spinner)

        desc_label = Gtk.Label(label=image_result.description)
        desc_label.add_css_class("caption")
        desc_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        box.append(desc_label)
        self._flow.append(box)

        # Load in background
        thread = threading.Thread(
            target=self._fetch_image,
            args=(image_result.image_url, box, spinner),
            daemon=True,
        )
        thread.start()

    def _fetch_image(self, url, box, spinner):
        """Fetch image data in background thread."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()

            GLib.idle_add(self._set_image, data, box, spinner)
        except Exception:
            GLib.idle_add(self._set_error, box, spinner)

    def _set_image(self, data, box, spinner):
        """Set the loaded image on the main thread."""
        try:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(data)
            loader.close()
            pixbuf = loader.get_pixbuf()

            if pixbuf:
                # Scale to 96x96
                pixbuf = pixbuf.scale_simple(96, 96, GdkPixbuf.InterpType.BILINEAR)
                texture = __import__("gi.repository.Gdk", fromlist=["Gdk"]).Gdk.Texture.new_for_pixbuf(pixbuf)
                picture = Gtk.Picture.new_for_paintable(texture)
                picture.set_size_request(96, 96)

                box.remove(spinner)
                # Insert picture before the label
                box.prepend(picture)
        except Exception:
            self._set_error(box, spinner)
        return False

    def _set_error(self, box, spinner):
        """Show error placeholder."""
        spinner.stop()
        box.remove(spinner)
        icon = Gtk.Image.new_from_icon_name("image-missing-symbolic")
        icon.set_pixel_size(48)
        box.prepend(icon)
        return False
