'''
2019-trec-precision-medicine"

To run the script
           $python3 [filename] [source data collection folder path]

for example:
         $python3 /home/iialab/Bhanu/Indexing2019.py /home/iialab/Bhanu/2019_clinical_trials_new.0
'''

import json
from datetime import datetime
from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import os
import re
import sys
from pathlib import Path
import collections

'''
If arguments count is lessthan 2, it throwes error.
'''


class Indexing:

    def __init__(self):
        self.es = Elasticsearch()
        self.source_dir = '/home/junhua/trec/FinalCode/TREC_2019_Basic_preprocessing'

    '''
    Set the default values for keys in the dict
    '''

    def setDefaultValuesForDict(self, data):
        print("set defau;lt values")
        data.setdefault("download_date", None)
        data.setdefault("url", None)
        data.setdefault("link_text", None)
        data.setdefault("org_study_id", None)
        data.setdefault("secondary_id", None)
        data.setdefault("nct_id", None)
        data.setdefault("brief_title", None)
        data.setdefault("official_title", None)
        data.setdefault("source", None)
        data.setdefault("brief_summary_text_block", None)
        data.setdefault("detailed_description_text_block", None)
        data.setdefault("start_date", None)
        data.setdefault("primary_completion_date", None)
        data.setdefault("study_type", None)
        data.setdefault("primary_purpose", None)
        data.setdefault("condition", None)
        data.setdefault("intervention_type", None)
        data.setdefault("intervention_name", None)
        data.setdefault("gender", None)
        data.setdefault("minimum_age", None)
        data.setdefault("maximum_age", None)
        data.setdefault("last_name", None)
        data.setdefault("affiliation", None)
        data.setdefault("country", None)
        data.setdefault("verification_date", None)
        data.setdefault("study_first_submitted", None)
        data.setdefault("study_first_submitted_qc", None)
        data.setdefault("last_update_posted", None)
        data.setdefault("keyword", None)
        data.setdefault("mesh_term", None)
        data.setdefault("intervention_browse_0_mesh_term", None)
        data.setdefault("intervention_browse_1_mesh_term", None)

    '''
        Prepares a dictionary with the vakues fromthe file
    '''

    def prepareDict(self, data):
        print("preparee dict")
        doc = {
            'download_date': self.getValue(data, "required_header", 0),
            'url': self.getValue(data, "required_header", 2),
            'link_text': self.getValue(data, "required_header", 1),
            'org_study_id': self.getValue(data, "id_info", 0),
            'secondary_id': self.getValue(data, "id_info", 1),
            'nct_id': self.getValue(data, "id_info", 4),
            'brief_title': data['brief_title'],
            'official_title': data['official_title'],
            'source': data['source'],
            'brief_summary_text_block': self.getValue(data, "brief_summary", 0),
            'detailed_description_text_block': self.getValue(data, "detailed_description", 0),
            'start_date': data['start_date'],
            'primary_completion_date': data['primary_completion_date'],
            'study_type': data['study_type'],
            'primary_purpose': self.getValue(data, "study_design_info", 0),
            'condition': data['condition'],
            'intervention_type': self.getValue(data, "intervention", 0),
            'intervention_name': self.getValue(data, "intervention", 1),
            'gender': self.getValue(data, "eligibility", 1),
            'minimum_age': self.getValue(data, "eligibility", 2),
            'maximum_age': self.getValue(data, "eligibility", 3),
            'last_name': self.getValue(data, "overall_official", 0),
            'affiliation': self.getValue(data, "overall_official", 2),
            'country': self.getValue(data, "location_countries", 0),
            'verification_date': data['verification_date'],
            'study_first_submitted': data['study_first_submitted'],
            'study_first_submitted_qc': data['study_first_submitted_qc'],
            'last_update_posted': data['last_update_posted'],
            'keyword': data['keyword'],
            'mesh_term': self.getValue(data, "condition_browse", 0),
            'intervention_browse_0_mesh_term': self.getValue(data, "intervention_browse", 0),
            'intervention_browse_1_mesh_term': self.getValue(data, "intervention_browse", 1)
        }
        return doc

    '''
        It returns the value for the provided key in the dict, if there is no key 
        presented in the dictionary it returns None Object.
    '''

    def getValue(self, data, key, index):
        dict = data.get(key, index)
        if dict:
            try:
                for value in dict[index].values():
                    return value
            except:
                return None
        else:
            return None

    '''
        1. list out all sub-directories and get folder by folder and get all xml files.
        2. Using elastic search indexing method it provides the index for the file with name '2019-trec-precision-medicine'
    '''

    def loadJsonDict(self):
        print("Load json dict")
        sub_dirs = os.listdir(self.source_dir)
        index_value = 0
        for folder in sub_dirs:
            sub_dirs = os.listdir(self.source_dir + '/' + folder + '/')
            for childDir in sub_dirs:
                jsonFiles = os.listdir(self.source_dir + '/' + folder + '/' + childDir)
                for fileIndex, file in enumerate(jsonFiles):
                    index_value += 1
                    dict = self.loadJson(self.source_dir + '/' + folder + '/' + childDir + '/' + file)
                    self.indexing(dict, index_value)

    def loadJson(self, sourceFile):
        print("loadJson")
        jsonFile = open(sourceFile)
        data = {}
        data = json.load(jsonFile)
        self.setDefaultValuesForDict(data)
        return data

    def indexing(self, data, index_value):
        print("Indexing")
        doc = self.prepareDict(data)
        res = Elasticsearch().index(index="2019-trec-precision-medicine", id=int(index_value), body=doc)
        print("####################################")
        print(index_value)
        print(res['result'])
        print("####################################")


