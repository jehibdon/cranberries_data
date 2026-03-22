This Python based tool automates the quantification of root surface area coverage from digital images. It uses grayscale thresholding to isolate root structures and calculates the percentage of the image covered by roots.

Before running the script, you need to install Python and the following libraries. Open your terminal and run:
pip install Pillow numpy matplotlib

To ensure the script runs correctly, organize your files like this:
--> roots.py: The main script
--> /Images: A folder containing all your .png root photos.
--> /Output: A folder where the script will save your pixelated images and graphs.

1. Place all your root images in the Images folder. Ensure they are in the .png format.
2. Run the script.
3. View results.
   --> Graphs and tables: These will pop on your screen as the script runs.
   --> Processed Images: Check the output folder for the pixelated images.
   --> Data Export: A file named "pixel_counts.csv" will be created in your main folder. You can open this in Excel or Google Sheets.

This tool follows a 4 step image process:
1. Greyscale conversion: Converts color images to an 8-bit brightness scale
2. Binary Thresholding: Uses a threshold of 115 to separate roots (white) from the background (black).
3. Pixel counting: Sums the white pixels to calculate the Root Surface Area Coverage using this formula:
   D = (white pixels/total pixels) * 100
4. Downsampling: Creates a pixelated version of the binary mask to help identify high growth areas.
