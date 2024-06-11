import os
import argparse
import PyPDF2
from tabulate import tabulate

argParser = argparse.ArgumentParser()

argParser.add_argument('-d', '--directory', required=True)
argParser.add_argument('-r', '--recursive', required=False, action="store_true")
argParser.add_argument('-D', '--Descending', required=False, action="store_true")
argParser.add_argument('-m', '--minimum_pages', required=False, type = int)
argParser.add_argument('-M', '--maximum_pages', required=False, type = int)
argParser.add_argument('-l', '--limit', required=False, type = int, help="Limit number of results to show, the default value is 20.")

args = argParser.parse_args()

targetDir = args.directory
min_pages = args.minimum_pages or 0
max_pages = args.maximum_pages or float('inf')
limit_res = args.limit or 20

def get_pdf_files(directory):
    pdf_files = []

    if args.recursive:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, filename))
        return pdf_files
    
    else:
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                pdf_files.append(os.path.join(directory, filename))
        return pdf_files

def get_num_pages(pdf_file):
    with open(pdf_file, 'rb') as file:
        #print("Reading "+ pdf_file)
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            #print(len(pdf_reader.pages))
            return len(pdf_reader.pages)
        except:
            #print("Fallo al leer")
            return 0
        

# Obtiene la lista de archivos PDF
pdf_files = get_pdf_files(targetDir)

# Crea una lista de tuplas con el nombre del archivo y el número de páginas
pdf_info = [(
    os.path.basename(os.path.dirname(file)),
    os.path.basename(file),
    get_num_pages(file)
) for file in pdf_files if (get_num_pages(file) >= min_pages) and ( get_num_pages(file) <= max_pages) ]

# Ordena la lista por número de páginas
pdf_info.sort(key=lambda x: x[2], reverse=args.Descending)
pdf_info = pdf_info[:limit_res]

# Muestra la información en una tabla
headers = ['Parent', 'Nombre del Archivo', 'Número de Páginas']
print(tabulate(pdf_info, headers=headers, tablefmt='grid'))