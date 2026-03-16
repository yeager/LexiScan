"""Entry point for LexiScan."""

import sys

from lexiscan.utils.i18n import setup_i18n

setup_i18n()

from lexiscan.application import LexiScanApp


def main():
    app = LexiScanApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
