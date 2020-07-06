#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from fortigate2csv import *

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Firewall Policy para CSV')
parser.add_argument('File', metavar='In_File', type=str, help='Arquivo com os comandos exportados do Fortigate')
parser.add_argument('-o', metavar='Out_File', dest='Output', help='Define o file name de saída, padrão [In_File].csv')

args = parser.parse_args()

Input = args.File

if str(args.Output) == 'None':
    Output = Path(str(Input)).stem + ".csv"

else:
    Output = args.Output

print("Argumentos:", vars(args))

print("Arquivo de Configuração:", Input)
print("Arquivo de Saída:", Output, "\n")

# Abrir Aquivo

print("Processando:", Input, "\n")

with open(Input) as In:
    line = In.readline() # Le a primeira linha
    
    line_out = '"EDIT";"CONFIG"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    while line:
        cli = line.lstrip(' ')
        command = cli.split()
        
        if command[0] == 'config': config(cli, 'config firewall vip')

        elif command[0] == 'end': write(Output, buffer_out, True)

        elif command[0] == 'next':
            line_out = '"' + obj_edit +'"'
            line_out = line_out + ';"' + obj_config.rstrip(' \n') + '"'
            buffer_out.append(line_out)

        elif command[0] == 'edit':
            obj_edit = edit(command)
            obj_config = ''

        elif command[0] == 'set':

            if command[1] == 'src-filter': obj_config += set(command, 'Source IP Filter:', False, True, 22, True)
            
            if command[1] == 'service': obj_config += set(command, 'Service:', False, True, 22, True)
            
            if command[1] == 'extip': obj_config += set(command, 'External IP:', newline=True)

            if command[1] == 'extintf': obj_config += set(command, 'External Iface:', case='upper', newline=True)
            
            if command[1] == 'portforward': obj_config += set(command, 'Port Forward:', case='upper', newline=True)
            
            if command[1] == 'mappedip': obj_config += set(command, 'Mapped IP:', newline=True)
            
            if command[1] == 'mappedport': obj_config += set(command, 'Mapped Port:', newline=True)
            
        line = In.readline() # Le a proxima linha