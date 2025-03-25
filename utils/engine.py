import os
import pandas as pd



class StringThreat():
    def __init__(self):
        self.ini = True


    def get_name(self, file_path):
        'Get file name, without the path.'
        last = file_path.rsplit('\\', 1)[-1]
        return last
    
class Counter(StringThreat):
    def __init__(self, dir):
        self.dir = dir
        self.rows = {}
        self.list_names = []
        self.list_rows = []
    
    def get_rows(self):
        'Get number of rows, file name and add to a dict.'
        for root, _, files in os.walk(self.dir):
            self.count_files(root, files)
        self.rows['file'] = self.list_names
        self.rows['rows'] = self.list_rows
    
    def count_files(self, root, files):
        'Count number of files in a dir.'
        for file in files:
           if file.endswith(".sql"):
               file_path = os.path.join(root, file)
               self.open_file(file_path)

    def open_file(self, file_path):
        'Open the file and count the number of rows.'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Arquivo: {file_path} - Linhas: {len(lines)}")
                path = self.get_name(file_path)
                self.list_names.append(path)
                self.list_rows.append(len(lines))
        except Exception as e:
                print(f"Error to read file {file_path}: {e}")

class Extract(Counter):
    def __init__(self, dir, name):
        super().__init__(dir)
        self.name = name
    
    def extract(self):
        'Call the engine process and extract the data into an Excel file.'
        self.get_rows()
        df = pd.DataFrame(self.rows)
        df.to_excel(f'{self.name}.xlsx', index=False)
        