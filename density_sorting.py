"""Design density analyzer.

This module defines two classes, `Design` and `Library`, used to store and sort
design layout data. Input coordinates are provided in micrometers (µm), but
density is computed as polygon count per square millimeter (polygons/mm²),
requiring a unit conversion.

The program:
1. Reads a data file containing design parameters.
2. Creates `Design` instances for each row.
3. Stores them inside a `Library` instance.
4. Prints designs sorted by density from high to low.

Data file format (seven columns):
    name  lower_left_x  lower_left_y  upper_right_x  upper_right_y  poly_count  md5sum
"""

from typing import List


class Design:
    """Represents a design block with geometry and polygon statistics.

    Attributes:
        name (str): Design identifier.
        lx (float): Lower-left x coordinate in micrometers (µm).
        ly (float): Lower-left y coordinate in micrometers (µm).
        ux (float): Upper-right x coordinate in micrometers (µm).
        uy (float): Upper-right y coordinate in micrometers (µm).
        poly_count (int): Number of polygons in the design.
        md5sum (str): Precomputed MD5 checksum provided in the input file.
        area_mm2 (float): Area of the design in mm².
        density (float): Polygon density (polygons per mm²).
    """

    def __init__(self, name: str, lx: float, ly: float, ux: float, uy: float,
                 poly_count: int, md5sum: str):
        """Initializes a Design instance.

        Args:
            name: Design name.
            lx: Lower-left x in µm.
            ly: Lower-left y in µm.
            ux: Upper-right x in µm.
            uy: Upper-right y in µm.
            poly_count: Number of polygons.
            md5sum: MD5 checksum string.
        """
        self.name = name
        self.lx = float(lx)
        self.ly = float(ly)
        self.ux = float(ux)
        self.uy = float(uy)
        self.poly_count = int(poly_count)
        self.md5sum = md5sum

        self.area_mm2 = self._compute_area_mm2()
        self.density = self._compute_density()

    def _compute_area_mm2(self) -> float:
        """Computes the design area in mm².

        Input coordinates are µm, so:
        1 mm = 1000 µm → 1 mm² = 1,000,000 µm²

        Returns:
            Area in square millimeters.
        """
        area_um2 = (self.ux - self.lx) * (self.uy - self.ly)
        return area_um2 / 1_000_000.0

    def _compute_density(self) -> float:
        """Computes polygon density as polygons per mm².

        Returns:
            Density value. If area is zero, returns 0.
        """
        if self.area_mm2 == 0:
            return 0.0
        return self.poly_count / self.area_mm2


class Library:
    """Stores and manages a collection of Design objects."""

    def __init__(self):
        """Initializes an empty design library."""
        self.designs: List[Design] = []

    def add_design(self, design: Design) -> None:
        """Adds a Design instance to the library.

        Args:
            design: A Design object.
        """
        self.designs.append(design)

    def print_by_density(self) -> None:
        """Prints all stored designs sorted from highest to lowest density."""
        sorted_designs = sorted(self.designs, key=lambda d: d.density, reverse=True)

        print("Designs sorted by density (high → low):")
        for d in sorted_designs:
            print(
                f"{d.name:10s} density={d.density:10.6f} poly/mm²   "
                f"area={d.area_mm2:12.2f} mm²   polys={d.poly_count:6d}"
            )


def main() -> None:
    """Main program entry point.

    Reads data from 'testdata.txt', constructs objects, sorts, and prints output.
    """
    library = Library()
    filename = "testdata.txt"

    with open(filename, "r", encoding="utf-8") as file:
        file.readline()  # Skip header line

        for line in file:
            parts = line.strip().split()
            if len(parts) != 7:
                continue  # Skip malformed lines

            name, lx, ly, ux, uy, poly_count, md5sum = parts
            library.add_design(Design(name, lx, ly, ux, uy, poly_count, md5sum))

    library.print_by_density()


if __name__ == "__main__":
    main()
