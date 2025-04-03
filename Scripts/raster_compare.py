import os
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# Utility Functions
# ========================
def load_raster(file_path):
    with rasterio.open(file_path) as src:
        arr = src.read(1)
        meta = src.meta.copy()
    return arr, meta

def confirm_alignment(meta1, meta2, arr1, arr2):
    if arr1.shape != arr2.shape:
        print("⚠️ Rasters have different shapes — alignment issue!")
        return False
    else:
        print("✅ Rasters are the same shape.")
    if meta1['transform'] != meta2['transform']:
        print("⚠️ Warning: Transforms do not match!")
        return False
    else:
        print("✅ Pixel alignment confirmed.")
    return True

def save_figure(fig, filepath):
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure saved to {filepath}")

# ========================
# Interactive File Selection
# ========================
processed_folder = "Data/Processed"
output_folder = "Output"
os.makedirs(output_folder, exist_ok=True)

# List all .tif files in the processed folder
all_files = [f for f in os.listdir(processed_folder) if f.endswith('.tif')]
print("Available NLCD files in Data/Processed:")
for idx, file in enumerate(all_files):
    print(f"{idx + 1}: {file}")

# Ask user for the reference file (later date)
ref_file = input("Enter the reference (later date) file from the above list (e.g., NLCD_2023.tif): ").strip()
if ref_file not in all_files:
    print("Reference file not found. Exiting.")
    exit()

ref_path = os.path.join(processed_folder, ref_file)
nlcd_ref, meta_ref = load_raster(ref_path)
print(f"Loaded reference file: {ref_file}")

# ========================
# Iterate Through Other Files and Process Each Comparison
# ========================
for file in all_files:
    if file == ref_file:
        continue  # Skip the reference file

    file_path = os.path.join(processed_folder, file)
    nlcd_earlier, meta_earlier = load_raster(file_path)
    print(f"\nProcessing comparison: {file} vs {ref_file}")

    # Confirm alignment between the earlier file and the reference
    if not confirm_alignment(meta_earlier, meta_ref, nlcd_earlier, nlcd_ref):
        print(f"Skipping {file} due to alignment issues.")
        continue

    # ------------------------
    # Step 1: Create Binary Change Mask
    # ------------------------
    change_mask = (nlcd_earlier != nlcd_ref).astype(np.uint8)
    changed_pixels = np.sum(change_mask)
    total_pixels = change_mask.size
    print("Changed pixels:", changed_pixels)
    print("Total pixels:", total_pixels)
    print("Percentage changed: {:.2f}%".format((changed_pixels / total_pixels) * 100))

    # Save the change mask as a GeoTIFF
    output_change_path = os.path.join(output_folder, f"NLCD_change_{file[:-4]}_vs_{ref_file[:-4]}.tif")
    meta_earlier.update({"dtype": "uint8", "count": 1})
    with rasterio.open(output_change_path, "w", **meta_earlier) as dest:
        dest.write(change_mask, 1)
    print(f"Change mask saved to {output_change_path}")

    # ------------------------
    # Step 2: Generate Transition Matrix
    # ------------------------
    classes_earlier = nlcd_earlier.flatten()
    classes_ref = nlcd_ref.flatten()
    df = pd.DataFrame({'Earlier': classes_earlier, 'Reference': classes_ref})
    transition_matrix = pd.crosstab(df['Earlier'], df['Reference'])
    print("Transition Matrix (Pixel Counts):")
    print(transition_matrix)
    # Convert pixel counts to area (acres)
    transition_area = transition_matrix * 0.2224
    print("Transition Matrix (Acres):")
    print(transition_area)

    # ------------------------
    # Step 3: Visualization
    # 3a. Greyscale Change Mask
    # ------------------------
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    cax1 = ax1.imshow(change_mask, cmap='gray', interpolation='none')
    fig1.colorbar(cax1, ax=ax1, label='Change Mask (0 = No Change, 1 = Change)')
    ax1.set_title(f'Change Mask: {file[:-4]} vs {ref_file[:-4]}')
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Row')
    greyscale_path = os.path.join(output_folder, f"change_mask_{file[:-4]}_vs_{ref_file[:-4]}.png")
    save_figure(fig1, greyscale_path)

    # ------------------------
    # 3b. Enhanced Overlay Map: Reference with Highlighted Change Areas
    # ------------------------
    # Create a discrete colormap for the reference NLCD (assuming up to 20 classes)
    cmap_nlcd = plt.get_cmap('tab20', 20)
    fig2, ax2 = plt.subplots(figsize=(12, 10))
    img = ax2.imshow(nlcd_ref, cmap=cmap_nlcd, interpolation='none')
    cbar = fig2.colorbar(img, ax=ax2, ticks=range(20))
    cbar.set_label('Reference NLCD Land Cover Class')
    # Overlay the change mask with increased opacity and a contrasting colormap
    change_overlay = np.ma.masked_where(change_mask == 0, change_mask)
    ax2.imshow(change_overlay, cmap='autumn', alpha=0.8, interpolation='none')
    # Add contour lines for clear boundaries
    ax2.contour(change_mask, levels=[0.5], colors='black', linewidths=1)
    ax2.set_title(f'Reference NLCD with Highlighted Changes ({file[:-4]} vs {ref_file[:-4]})')
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Row')
    overlay_path = os.path.join(output_folder, f"overlay_map_{file[:-4]}_vs_{ref_file[:-4]}.png")
    save_figure(fig2, overlay_path)

print("All comparisons processed and visualizations saved. Script complete.")