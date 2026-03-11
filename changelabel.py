import os

LABELS_DIR = "datasets/drone/test/labels"
IMAGES_DIR = "datasets/drone/test/images"


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
        class_id = int(parts[0])
        if parts[0] == "0":
            print(label_path)

        new_lines.append(" ".join(parts))

    with open(label_path, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    # Track valid label base names
    base_name = os.path.splitext(filename)[0]
    valid_label_basenames.add(base_name)



print("Cleanup complete.")