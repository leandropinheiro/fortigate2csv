#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from fortigate2csv import *

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Webfilter Content para CSV')
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
    
    line_out = '"EDIT";"NAME";"ENTRIES"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    inedit = False
    pattern = False
    status = False
    lang = False
    action = False

    while line:
        cli = line.lstrip(' ')
        command = cli.split()    

        if command[0] == 'config': 
            if not inedit: config(cli, 'config webfilter content')

        elif command[0] == 'end': 
            if not inedit:
                write(Output, buffer_out, True)
            else:
                inedit = False
        elif command[0] == 'next':
            if not inedit:
                line_out = obj_edit
                line_out = line_out + ';' + obj_name
                line_out = line_out + ';"' + obj_entries.rstrip(' \n') + '"'
                buffer_out.append(line_out)
                inedit = False
            else:
                if not pattern: obj_entries += 'Pattern Type: WILDCARD\n'
                if not status: obj_entries += 'Status: DISABLE\n'
                if not lang: obj_entries += 'Language: WESTERN\n'
                if not action: obj_entries += 'Action: BLOCK\n'

        elif command[0] == 'edit':
            if not inedit:
                pattern = False
                status = False
                lang = False
                action = False
                obj_name = ''
                obj_entries = ''
                obj_edit = edit(command, True)
            if inedit:
                pattern = False
                status = False
                lang = False
                action = False
                if not obj_entries == '': obj_entries += '\n'
                obj_entries += 'Edit: ' + edit(command, quote=False) + '\n'
            inedit = True
            
        elif command[0] == 'set':

            if command[1] == 'name': obj_name = set(command, quote=True)

            if command[1] == 'pattern-type':
                obj_entries += set(command, 'Pattern Type:', newline=True, case='upper')
                pattern = True

            if command[1] == 'status':
                obj_entries += set(command, 'Status:', newline=True, case='upper')
                status = True

            if command[1] == 'lang':
                obj_entries += set(command, 'Laguage:', newline=True, case='upper')
                lang = True
            
            if command[1] == 'action':
                obj_entries += set(command, 'Action:', newline=True, case='upper')
                action = True
            
        line = In.readline() # Le a proxima linha