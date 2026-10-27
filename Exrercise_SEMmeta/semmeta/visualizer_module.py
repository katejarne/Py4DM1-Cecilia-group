# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import modules for file system operations (os), JSON parsing (json), 
# and regular expressions -- regex (re)
import os, json, re

# Import PIL for image loading and matplotlib for visualization
from PIL import Image
import matplotlib.pyplot as plt


# Class for visualizing SEM images alongside selected metadata
class SEMVisualizer:
    def __init__(self, json_path, image_path):
        # Store the path to the cleaned metadata JSON file
        self.json_path = json_path
        
        # Store the path to the SEM image file
        self.image_path = image_path
        
        # Define the list of metadata variables to extract and display
        self.variables = [
            "AP_WD",
            "AP_BEAM_TIME",
            "AP_IMAGE_PIXEL_SIZE",
            "AP_HOLDER_HEIGHT",
            "AP_BEAM_CURRENT",
            "AP_HOLDER_DIAMETER"]        
        
        # Initialize an empty dictionary to hold loaded metadata
        self.metadata = {}

    # Load metadata from JSON file into self.metadata
    def load_metadata(self):
        """
        Reads the cleaned JSON file (self.json_path) into self.metadata.
        """

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        # TODO (Task 3): implement this method
        # raise NotImplementedError("load_metadata is not implemented yet")


    def clean_value(self, raw_value, variable_name=None):
        """
        Splits a cleaned metadata value into its number and unit.

        The value must be a (signed) number, optionally in scientific
        notation, followed by a unit. Otherwise ("N/A", "N/A") is returned.

        Examples:
            "3.18 mm"         ->  ("3.18", "mm")
            "-13 pA"          ->  ("-13", "pA")
            "2.34e-006 mbar"  ->  ("2.34e-006", "mbar")
            "InLens" or None  ->  ("N/A", "N/A")

        Returns:
            (value, unit) as strings, or ("N/A", "N/A") if no
            number followed by a unit is found
        """

        # Ensure the input is a string before applying regex
        if not isinstance(raw_value, str):
            return ("N/A", "N/A")

        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', raw_value.strip())

        # If a match is found, return the value and the unit
        if match:
            value, unit = match.groups()
            return (value, unit)

        # Return fallback values (Not Available) if no match is found
        return ("N/A", "N/A")

    def extract_variables(self):
        """
        Extracts selected metadata variables and formats
        them into (name, value, unit) tuples for display.        
        Missing variables give (name, "N/A", "N/A").
        Return the list of formatted metadata rows
        """
        rows = []
        for name in self.variables:
            if name in self.metadata:
                value, unit = self.clean_value(self.metadata[name], variable_name=name)
            else:
                value, unit = ("N/A", "N/A")
            rows.append((name, value, unit))
        return rows
        # TODO (Task 3): implement this method
        # raise NotImplementedError("extract_variables is not implemented yet")



    def show_image_with_table(self):
        """
        Displays the SEM image alongside a formatted metadata
        table and saves the combined output as a figure.

        1. Loads the metadata.
        2. Builds a figure with two vertically stacked panels:
           the grayscale SEM image (top) and a table with the
           column labels "Variable", "Value", "Unit" (bottom).
        3. Creates the folder ./output if needed.
        4. Saves the figure as ./output/<image name without extension>.png
        5. Displays the figure, then closes it.
        """
    def show_image_with_table(self):
        """
        Displays the SEM image alongside a formatted metadata
        table and saves the combined output as a figure.
        """
        # 1. Load metadata
        self.load_metadata()

        # 2. Extract variables and prepare rows for the table
        extracted = self.extract_variables()
        rows = [[name, value, unit] for name, value, unit in extracted]

        # 3. Create figure with two vertically stacked panels
        fig, (ax_img, ax_table) = plt.subplots(2, 1, figsize=(8, 8))

        # 4. Top panel: grayscale image
        img = plt.imread(self.image_path)
        ax_img.imshow(img, cmap="gray")
        ax_img.axis("off")

        # 5. Bottom panel: metadata table
        ax_table.table(
            cellText=rows,
            colLabels=["Variable", "Value", "Unit"],
            loc="center"
        )
        ax_table.axis("off")

        # 6. Save and close
        os.makedirs("./output", exist_ok=True)
        stem = os.path.splitext(os.path.basename(self.image_path))[0]
        fig.savefig(f"./output/{stem}.png", bbox_inches="tight")
        #plt.show()
        plt.close(fig)
        # TODO (Task 3): implement this method
        # raise NotImplementedError("show_image_with_table is not implemented yet")
        

 
