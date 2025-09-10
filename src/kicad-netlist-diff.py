#!/usr/bin/env python3
"""
KiCAD-netlist-diff

This script compares two KiCAD netlist XML files and outputs the differences
to a CSV file. The CSV file is named after the first netlist file with
"-diff.csv" appended to its name.

Example usage:
    ./KiCAD-netlist-diff netlist1.xml netlist2.xml
"""

import sys
import os
import csv
import xml.etree.ElementTree as ET


def parse_netlist(file_path):
    """
    Parse a KiCAD netlist XML file and convert it into a Python dictionary.

    The dictionary has the following structure:
        {
            "R1": {
                "value": "10k",
                "footprint": "Resistor_SMD:R_0805",
                "datasheet": "http://example.com/ds.pdf",
                "CustomField1": "SomeValue",
                ...
            },
            "C3": {
                "value": "100nF",
                "footprint": "Capacitor_SMD:C_0603",
                ...
            },
            ...
        }

    Parameters
    ----------
    file_path : str
        Path to the KiCAD netlist XML file.

    Returns
    -------
    dict
        Dictionary mapping component references (e.g., R1, C3, U2) to
        dictionaries of their properties and field values.
    """

    # Parse the XML file using ElementTree
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Dictionary that will hold all components keyed by their reference
    comps = {}

    # Find all <comp> elements inside the <components> section
    for comp in root.findall(".//components/comp"):
        ref = comp.get("ref")  # Component reference, e.g., "R1", "U3"

        # Each component can have a number of subfields
        fields = {}

        # Extract the value field (e.g., "10k", "LM324", etc.)
        value = comp.findtext("value")
        if value:
            fields["value"] = value

        # Extract the footprint field (e.g., "Resistor_SMD:R_0805")
        footprint = comp.findtext("footprint")
        if footprint:
            fields["footprint"] = footprint

        # Extract the datasheet link if it exists
        datasheet = comp.findtext("datasheet")
        if datasheet:
            fields["datasheet"] = datasheet

        # Extract any custom fields defined in the schematic
        # These appear inside <fields><field name="...">...</field></fields>
        for f in comp.findall("fields/field"):
            fields[f.get("name")] = f.text or ""

        # Store the dictionary of fields under the component's reference
        comps[ref] = fields

    return comps


def compare_netlists(netlist1, netlist2):
    """
    Compare two parsed netlists (as dictionaries) and return a list of differences.

    The differences are expressed as rows in the form:
        [Reference, Field, Value_in_Netlist1, Value_in_Netlist2]

    Types of differences handled:
    - Component missing in one netlist
    - Field missing or different between netlists

    Parameters
    ----------
    netlist1 : dict
        Parsed netlist dictionary from the first file.
    netlist2 : dict
        Parsed netlist dictionary from the second file.

    Returns
    -------
    list of list
        Each inner list represents a difference with 4 elements:
        [reference, field, value_in_netlist1, value_in_netlist2]
    """

    diffs = []

    # Collect all unique component references across both netlists
    all_refs = set(netlist1.keys()) | set(netlist2.keys())

    # Loop through each component reference in sorted order (for consistent output)
    for ref in sorted(all_refs):
        if ref not in netlist1:
            # Component exists only in netlist2
            diffs.append([ref, "Missing in first netlist", "", str(netlist2[ref])])
        elif ref not in netlist2:
            # Component exists only in netlist1
            diffs.append([ref, "Missing in second netlist", str(netlist1[ref]), ""])
        else:
            # Component exists in both netlists, so compare their fields
            fields1 = netlist1[ref]
            fields2 = netlist2[ref]

            # Union of all fields used by this component across both netlists
            all_fields = set(fields1.keys()) | set(fields2.keys())

            for field in all_fields:
                v1 = fields1.get(field, "")  # Default to empty string if missing
                v2 = fields2.get(field, "")

                if v1 != v2:
                    # Record the mismatch
                    diffs.append([ref, field, v1, v2])

    return diffs


def main():
    """
    Main entry point of the script.

    - Reads two command-line arguments (the netlist file paths).
    - Parses both netlists into dictionaries.
    - Compares them to find differences.
    - Writes differences into a CSV file.
    """

    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: KiCAD-netlist-diff <netlist1.xml> <netlist2.xml>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    # Parse both netlist files
    netlist1 = parse_netlist(file1)
    netlist2 = parse_netlist(file2)

    # Compare the two netlists
    diffs = compare_netlists(netlist1, netlist2)

    # Construct output filename: same as first file but with "-diff.csv" appended
    out_file = os.path.splitext(file1)[0] + "-diff.csv"

    # Open CSV file for writing
    with open(out_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(["Reference", "Field", "Netlist1", "Netlist2"])

        # Write each difference as a row
        for diff in diffs:
            writer.writerow(diff)

    print(f"Comparison complete. Differences written to {out_file}")


# Entry point guard
if __name__ == "__main__":
    main()
