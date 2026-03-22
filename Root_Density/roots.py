
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Automatically get all PNG files in the Images folder
image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]

pixel_size = 4
threshold = 115
pixel_counts = []

for roots in image_files:
    img_path = os.path.join(IMAGE_DIR, roots)
    img = Image.open(img_path)

    # Convert to grayscale and binary
    gray = img.convert("L")
    arr = np.array(gray)
    binary = arr > threshold

    # Count pixels
    num_white = np.sum(binary)
    num_black = binary.size - num_white
    percent_white = (num_white / binary.size) * 100

    # Store data for later
    pixel_counts.append({
        "image": roots,
        "white_pixels": num_white,
        "black_pixels": num_black,
        "percent_white": percent_white
    })

    # Create pixelated version for display
    binary_img = Image.fromarray(binary.astype(np.uint8) * 255)
    small_binary = binary_img.resize(
        (binary_img.width // pixel_size, binary_img.height // pixel_size),
        resample=Image.BILINEAR
    )
    pixelated_binary = small_binary.resize(binary_img.size, resample=Image.NEAREST)
    
    # Save the processed image
    pixelated_binary.save(os.path.join(OUTPUT_DIR, f"pixelated_{roots}"))

    # Display processing comparison for each image
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.title(f"Original Binary: {roots}")
    plt.imshow(binary_img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Pixelated Effect")
    plt.imshow(pixelated_binary, cmap="gray")
    plt.show()

# Table
table_rows = []
for entry in pixel_counts:
    table_rows.append([
        entry['image'], 
        f"{entry['white_pixels']:,}",
        f"{entry['black_pixels']:,}", 
        f"{entry['percent_white']:.2f}%"
    ])

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')
ax.set_title("Analysis Summary Table", fontsize=16, pad=20)

columns = ("Image Name", "White Pixels", "Black Pixels", "Coverage %")
the_table = ax.table(cellText=table_rows, 
                      colLabels=columns, 
                      loc='center', 
                      cellLoc='center',
                      colColours=["#f2f2f2"] * 4)

the_table.auto_set_font_size(False)
the_table.set_fontsize(11)
the_table.scale(1.2, 2.5)

plt.show()

# Graph
images = [entry['image'] for entry in pixel_counts]
percentages = [entry['percent_white'] for entry in pixel_counts]

plt.figure(figsize=(10, 6))

bars = plt.bar(images, percentages, color='#2c3e50', alpha=0.85, edgecolor='black', linewidth=1)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.1f}%', 
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.ylabel("Root Surface Area Coverage (%)", fontsize=12, fontweight='bold')
plt.xlabel("Images", fontsize=12, fontweight='bold')
plt.title("Quantitative Comparison of Root Density", fontsize=14, pad=20)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.xticks(rotation=25, ha='right')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "Root_Analysis_Graph.png"), dpi=300)
plt.show()


csv_path = os.path.join(BASE_DIR, "pixel_counts.csv")
with open(csv_path, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["image", "white_pixels", "black_pixels", "percent_white"])
    writer.writeheader()
    writer.writerows(pixel_counts)

print(f"\nAll set! CSV saved to: {csv_path}")