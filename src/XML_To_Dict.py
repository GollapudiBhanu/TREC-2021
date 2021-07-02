import json
from bs4 import BeautifulSoup
import xmltodict
import os


class Conversion:
    def __init__(self, source_dir, dest_dir):
        self.dest_dir = dest_dir  # /home/iialab/Bhanu/PythonFiles/Sample_Trec_2016
        self.source_dir = source_dir  # /home/iialab/Bhanu/PythonFiles/sample_Trec_2016_output
        self.convert_nxml_to_xml()

    '''
        
    '''
    def convert_nxml_to_xml(self):
        src_dir = os.listdir(self.source_dir)
        for dir in src_dir:
            sub_dir = os.listdir(self.source_dir + '/' + dir)
            for sdir in sub_dir:
                xml_files = os.listdir(self.source_dir + '/' + dir + '/' + sdir)
                if not os.path.exists(self.dest_dir + '/' + dir + '/' + sdir):
                    os.makedirs(self.dest_dir + '/' + dir + '/' + sdir)
                for xml in xml_files:
                    self.convertXML(self.source_dir + '/' + dir + '/' + sdir + '/' + xml,
                                    self.dest_dir + '/' + dir + '/' + sdir + '/' + xml)

    def convertXML(self, xml_file, output_file):
        with open(xml_file, 'r') as file:
            data = file.read()
        bs_data = BeautifulSoup(data, "xml")
        bData = bs_data.prettify()
        with open(output_file, 'w') as out_file:
            out_file.write(bData)

    # Need top move basic preprocessing

    def xmlToDict(self, out_file):
        with open(out_file, 'r') as file:
            data_dict = xmltodict.parse(file.read())
            file.close()
        for key, value in data_dict.items():
            data_dict[key]: value
        json_data = json.dumps(data_dict)
        with open("/home/iialab/Bhanu/PythonFiles/sample_Trec_2016_output/2.json", 'w') as outfile:
            outfile.write(json_data)


_ = Conversion('/home/iialab/Bhanu/PythonFiles/Sample_Trec_2016',
                            '/home/iialab/Bhanu/PythonFiles/sample_Trec_2016_output')
print("Conversion is done")
