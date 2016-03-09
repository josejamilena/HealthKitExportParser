#!/usr/bin/env python
"""
A quick script for tidying up data from the HealthKit export file.

To get an export file:
 1) Open the Health app on iOS
 2) Under "Health Data", select "All"
 3) Use the share button to get a copy of your data in XML format

This script allows you to get data for one particular value, and turn it into
a slightly more human-readable form.

Use `get_available_types()` to get a list of all the `type` keys used in the
XML data. Find the one you want, and then pass that into
`get_values_for_type()`. I'm assuming that the data is an integer; if that's
not correct, change lines 48 and 55.

The `main()` function has an example for getting step count data.
"""

from collections import defaultdict
from xml.etree import ElementTree as ET

from dateutil import parser

import itertools

def get_available_types(filepath):
    """
    Returns a list of all the types of data in the HealthKit export file.
    """
    types = set()
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in root:
        types.add(child.attrib.get("type", ""))
    types.remove("")
    return types


def get_values_for_type(filepath, type_name):
    """
    Given a path to an XML file, return a list of date/value pairs for all the
    data points of a given type.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()

    #values = defaultdict(int)
    values = defaultdict(str)

    for child in root:
        # if child.tag in ["ExportDate", "Me"]:
        #     continue
        # if child.attrib["type"] == type_name:
        #     date = parser.parse(child.attrib['startDate']).date()
        #     try:
        #         #values[date] += int(float(child.attrib['value']))
        #         values[date] += float(child.attrib['value'])
        #     except:
        #         values[date] += child.attrib['value']
        s = child
        year = s.attrib['ExportDate'].value[:4]
        month = s.attrib['ExportDate'].value[4:6]
        date = s.attrib['ExportDate'].value[6:8]
        hour = s.attrib['ExportDate'].value[8:10]
        minute = s.attrib['ExportDate'].value[10:12]
        try:
            #try to parse the consolidated values
			print "%s,%s,%s,%s,%s,%d,%d,%d,%d" % (year, month, date, hour, minute,   float(s.attrib['min'].value)*60, float(s.attrib['max'].value)*60, float(s.attrib['average'].value)*60, float(s.attrib['recordCount'].value))
        except:
            #try to parse the non-consolidated ones
            print "%s,%s,%s,%s,%s,%d,%d,%d,%d,+" % (year, month, date, hour, minute, float(s.attrib['value'].value)*60, float(s.attrib['value'].value)*60, float(s.attrib['value'].value)*60, 1)
    #return values
    return s


def main():
    lista = get_available_types("export.xml")
    print lista
    #step_data = get_values_for_type("export.xml",
    #                                "HKQuantityTypeIdentifierStepCount")
    for nodo in lista:
        step_data = get_values_for_type("export.xml",nodo)
        with open("stepdata.txt", "w") as f:
            for date, step_count in step_data.iteritems():
                f.write("%s %s\n" % (date, step_count))


if __name__ == '__main__':
    main()
