# KiCAD-netlist-diff

## Overview

`KiCAD-netlist-diff` is a Python command-line tool that compares two **KiCAD netlist XML files** and records any differences in a CSV file.  
This script is useful when working on collaborative hardware design projects or when maintaining version-controlled schematic changes, as it helps you quickly identify discrepancies between two schematic netlists.

The differences can include:
- Components present in one netlist but missing in the other.
- Field value mismatches (e.g., value, footprint, datasheet, or custom fields).

The output CSV file is automatically named after the **first input netlist** with `-diff.csv` appended.

---

## Features

- Parses KiCAD netlist files in XML format.
- Compares **components and their fields**:
  - Reference (e.g., R1, C3, U5).
  - Standard fields (`value`, `footprint`, `datasheet`).
  - Custom fields defined in the schematic.
- Detects:
  - Missing components.
  - Field mismatches (different values between netlists).
- Outputs results to a clean, structured CSV file.

---

## Requirements

- Python **3.6+**
- Standard library modules only (`sys`, `os`, `csv`, `xml.etree.ElementTree`).

No external dependencies are required.

---

## Installation

1. Save the script as `KiCAD-netlist-diff` (or `KiCAD-netlist-diff.py` if preferred).
2. Make it executable (Linux/macOS):
   ```bash
   chmod +x KiCAD-netlist-diff
   ```
   ## Usage

   ### Command Syntax
   KiCAD-netlist-diff <netlist1.xml> <netlist2.xml>

       <netlist1.xml> : First KiCAD netlist file (used as the baseline).
       <netlist2.xml> : Second KiCAD netlist file (compared against the first).
       Output will be written to <netlist1>-diff.csv.

   ### Example

   Suppose you have two netlists:

   design_revA.xml  
   design_revB.xml  

   Run the comparison:

   ./KiCAD-netlist-diff design_revA.xml design_revB.xml

   The script will:

   - Parse both netlists.  
   - Compare components and fields.  
   - Create an output file:  

   design_revA-diff.csv  

   ### Sample Output (CSV)

   The generated CSV will have the following columns:

   Reference | Field | Netlist1 | Netlist2  
   --------- | ----- | -------- | --------  
   R1 | value | 10k | 4.7k  
   C3 | Missing in second netlist | {'value': '100nF', 'footprint': 'C_0603'} |  
   U2 | footprint | Package_SO:SOIC-8 | Package_SO:SOIC-14  

   ### Notes

   - The script focuses on component-level differences (values, footprints, fields).  
   - It does not currently compare the <nets> connectivity section.  
   - If you need net-level comparison, that could be added as a future enhancement.  

   ### License

   This script is provided under the GPL V3 License
   Feel free to use, modify, and distribute it as needed.
