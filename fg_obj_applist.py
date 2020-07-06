#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from fortigate2csv import *

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Application List Group para CSV')
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
    
    line_out = '"EDIT";"MEMBERS"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    while line:
        cli = line.lstrip(' ')
        command = cli.split()
        inedit = False

        if command[0] == 'config': 
            config(cli, 'config application list')

        elif command[0] == 'end': write(Output, buffer_out, True)

        elif command[0] == 'next':
            line_out = obj_edit
            line_out = line_out + ';"' + obj_member.rstrip('\n') + '"'
            buffer_out.append(line_out)
            inedit = False

        elif command[0] == 'edit':
            print(command)
            obj_edit = edit(command, True)
            obj_membe''
            inedit = True

        elif command[0] == 'set':

            if command[1] == 'member': obj_member= set(command, newline=True)
             
        line = In.readline() # Le a proxima linha