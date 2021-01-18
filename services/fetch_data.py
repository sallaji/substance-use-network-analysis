#!/usr/bin/env python3

import requests
import pandas as pd
import os.path
from services.logger import *


class FetchData(object):
    """
    Service class for performing CRUD database operations
    """

    def __init__(self):
        pass

    def fetch_db_and_write_tsv_file(self, rewrite=False, filepath=None):
        """
        Downloads the database and writes it locally as a zip tsv file
        :param rewrite: rewrite the existing zip file
        :param filepath:
        """
        try:
            if filepath is None:
                raise FileNotFoundError('You must specify a filepath before doing this operation')
            if not os.path.isfile(filepath) or rewrite is True:
                if rewrite is False:
                    print("A local copy of the database was not found in the 'data' folder")

                DATABASE = "https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2019" \
                           "/NSDUH-2019-datasets/NSDUH-2019-DS0001/NSDUH-2019-DS0001-bundles-with-study-info" \
                           "/NSDUH-2019-DS0001-bndl-data-tsv.zip"
                print("Fetching database from NSDUH server...\n Database-Url: {}\n".format(DATABASE))
                data = requests.get(DATABASE)
                with open(filepath, 'wb') as fid:
                    fid.write(data.content)
                    print("A copy of the database has been successfully created at {}".format(filepath))
            else:
                print("A local copy of the database already exists. If you want to rewrite the existing file call "
                      "'rewrite=True' in the 'write_tsv_zip_file' function")
        except FileNotFoundError:
            print('Cannot read file with filepath=None')
            raise
