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
    
    line_out = '"EDIT";"OPTIONS";"ENTRIES";"COMMENT"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")
    
    inedit = False
    action = False
    log = False

    while line:
        cli = line.lstrip(' ')
        command = cli.split()    

        if command[0] == 'config': 
            if not inedit: config(cli, 'config application list')

        elif command[0] == 'end': 
            if not inedit:
                write(Output, buffer_out, True)
            else:
                inedit = False
        elif command[0] == 'next':
            if not inedit:
                line_out = obj_edit
                line_out = line_out + ';"' + obj_options.rstrip(' \n') + '"'
                line_out = line_out + ';"' + obj_entries.rstrip(' \n') + '"'
                line_out = line_out + ';"' + obj_comment.rstrip(' \n') + '"'
                buffer_out.append(line_out)
                inedit = False
            else:
                if not action: obj_entries += 'Action: BLOCK\n'
                if not log: obj_entries += 'Log: ENABLED\n'

        elif command[0] == 'edit':
            if not inedit:
                action = False
                log = False
                obj_comment = '-'
                obj_options = ''
                obj_entries = ''
                obj_edit = edit(command, True)
            if inedit:
                action = False
                log = False
                obj_entries += '\nEdit: ' + edit(command, quote=True) + '\n'
            inedit = True
            
        elif command[0] == 'set':

            if command[1] == 'deep-app-inspection': obj_options += set(command, 'Deep App Inspect:', newline=True, case='upper')

            if command[1] == 'other-application-log:': obj_options += set(command, 'Other App Log', newline=True, case='upper')

            if command[1] == 'unknown-application-action': obj_options += set(command, 'Other App Action:', newline=True)
            
            if command[1] == 'options': obj_options += set(command, 'Other Options:', tab=False, tab_len=15, newline=True, case='upper')

            if command[1] == 'application': obj_entries += set(command, 'Applications:', newline=True)
            
            if command[1] == 'action':
                obj_entries += set(command, 'Action:', newline=True, case='upper')
                action = True
            
            if command[1] == 'log':
                obj_entries += set(command, 'Log:', newline=True, case='upper')
                log = True
            
            if command[1] == 'category': obj_entries += set(command, 'Category:', tab=False, tab_len=5, newline=True)
            
            if command[1] == 'comment': obj_comment = set(command)

        line = In.readline() # Le a proxima linha