import os

LABELS_DIR = "Database1"
IMAGES_DIR = "Database1"


valid_label_basenames = set()

for filename in os.listdir(LABELS_DIR):
    if not filename.endswith(".txt"):
        continue

    label_path = os.path.join(LABELS_DIR, filename)

    with open(label_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    # Delete empty label files
    if not lines:
        os.remove(label_path)
        print(f"Deleted empty label: {filename}")
        continue

    # Force class ID = 2
    new_lines = []
    for line in lines:
        parts = line.split()
        parts[0] = "2"
        new_lines.append(" ".join(parts))

    with open(label_path, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    # Track valid label base names
    base_name = os.path.splitext(filename)[0]
    valid_label_basenames.add(base_name)

# --- STEP 2: Remove images without matching labels ---
for filename in os.listdir(IMAGES_DIR):
    if not filename.lower().endswith(".jpeg"):
        continue

    base_name = os.path.splitext(filename)[0]

    if base_name not in valid_label_basenames:
        image_path = os.path.join(IMAGES_DIR, filename)
        os.remove(image_path)
        print(f"Deleted image without label: {filename}")

print("Cleanup complete.")