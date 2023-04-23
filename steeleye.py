import zipfile
import xml.etree.ElementTree as ET
import csv
import urllib.request

# Download the zip file
url = 'http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip'
file_type = 'DLTINS'
with urllib.request.urlopen(url) as f:
    with zipfile.ZipFile(f) as z:
        # Extract the XML file
        xml_filename = None
        for name in z.namelist():
            if name.endswith('.xml'):
                with z.open(name) as xml_file:
                    xml_filename = name
                    break
        if not xml_filename:
            raise ValueError('No XML file found in zip')

        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract the data
        data = []
        for elt in root.findall('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}FinInstrmGnlAttrbts'):
            id = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}Id')
            full_name = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}FullNm')
            classification_type = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}ClssfctnTp')
            commodity_derivative_indicator = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}CmmdtyDerivInd')
            national_currency = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}NtnlCcy')
            issuer = elt.findtext('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}Issr')
            data.append([id, full_name, classification_type, commodity_derivative_indicator, national_currency, issuer])

        # Write the data to a CSV file
        csv_filename = 'output.csv'
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp', 'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr'])
            writer.writerows(data)

print(f"CSV file '{csv_filename}' saved successfully")
