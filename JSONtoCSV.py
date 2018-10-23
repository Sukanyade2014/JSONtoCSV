import ijson
import sys
import csv
import json
import Validator.py

class JSONtoCSV:


    def __init__(self , filename):
        try:
            with open(filename) as f:
                try:
                    self.JSONattributes = {}
                    self.metadata = json.load(f)
                    self.inputfile = self.metadata['FileDetails'][0]['InputFile']
                    self.outputfile = self.metadata['FileDetails'][1]['OutputFile']

                    for i in self.metadata['JSONSchema'] :
                        self.JSONattributes.update(i)
                    #print(self.JSONattributes)

                except:
                    print("Cannot parse the configuration JSON:")
                    exit()
        except:
            print("Configuration file not found")
            exit()


    '''  
    Get the keys:
    '''
    def writeheader(self):
        header = ['EmployeeID']
        with open(self.outputfile, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            try:
                with open(self.inputfile) as f:
                    u = [o for o in (ijson.items(f , '1'))]
                    header.append(list(u[0].keys()))
            except:
                print('Invalid input file format')
                exit()

            writer.writerow(header)

    '''Write values to CSV'''
    def writetocsv (self):
        try:
            with open(self.outputfile, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                with open(self.inputfile) as f:
                    i = 1
                    writetocsv = [i]
                    number_of_attributes = len(self.metadata['JSONSchema'])

                    for prefix, event, value in ijson.parse(f):
                        for j in range(0, number_of_attributes):

                            meta_key = list(self.metadata['JSONSchema'][j].keys())[0]
                            expected_prefix = str(i) + '.' + meta_key
                            if (prefix, event) == (expected_prefix, self.JSONattributes.get(meta_key)):

                                writetocsv.append(value)
                                print(value)
                                if (j == number_of_attributes -1):
                                    writer.writerow(writetocsv)
                                    i = i +1
                                    writetocsv = [i]



            csv_file.close()
        except FileNotFoundError as f:
            print ('Unable to find the file. Please check the path.')
            exit()
        except PermissionError as e:
            print('Unable to write to the CSV file.. Please close the file and try again')
            exit()
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            exit()


if __name__ == "__main__":

    json_data = JSONtoCSV('C:\\Users\\sde11\\Documents\\ProductEngg\\Input.json')
    json_data.writeheader()
    json_data.writetocsv()








