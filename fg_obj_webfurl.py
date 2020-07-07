#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from fortigate2csv import *

parser = argparse.ArgumentParser(description='Transforma CLI FortiGate IPv4 Object Webfilter Urlfilter para CSV')
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
    onearmips = False
    ipaddrblock = False
    url = False
    tipo = False
    action = False
    status = False
    exempt = False
    webproxyprofile = False
    referrerhost = False

    while line:
        cli = line.lstrip(' ')
        command = cli.split()    

        if command[0] == 'config': 
            if not inedit: config(cli, 'config webfilter urlfilter')

        elif command[0] == 'end': 
            if not inedit:
                write(Output, buffer_out, True)
            else:
                inedit = False
        elif command[0] == 'next':
            if not inedit:
                line_out = obj_edit
                line_out = line_out + ';"' + obj_options.rstrip('\n') + '"'
                line_out = line_out + ';"' + obj_entries.rstrip(' \n') + '"'
                buffer_out.append(line_out)
                inedit = False
            else:
                if not onearmips: obj_options += 'One-arm IPS URL Filter: DISABLED\n'
                if not ipaddrblock: obj_options += 'IP Addr Block: DISABLED\n'
                if not url: obj_entries += 'URL: NONE\n'
                if not tipo: obj_entries += 'Type: SIMPLE\n'
                if not action: obj_entries += 'Action: EXEMPT\n'
                if not status: obj_entries += 'Status: ENABLE\n'
                if not exempt: obj_entries += 'Exempt: ' + 'av web-content activex-java-cookie dlp fortiguard range-block all\n'.upper() 
                if not webproxyprofile: obj_entries += 'Web Proxy Profile: -\n'
                if not referrerhost: obj_entries += 'Referrer Host: -\n'

        elif command[0] == 'edit':
            if not inedit:
                inedit = False
                onearmips = False
                ipaddrblock = False
                url = False
                tipo = False
                action = False
                status = False
                exempt = False
                webproxyprofile = False
                referrerhost = False
                obj_options = ''
                obj_entries = ''
                obj_edit = edit(command, True)
            if inedit:
                inedit = False
                onearmips = False
                ipaddrblock = False
                url = False
                tipo = False
                action = False
                status = False
                exempt = False
                webproxyprofile = False
                referrerhost = False
                if not obj_entries == '': obj_entries += '\n'
                obj_entries += 'Edit: ' + edit(command, quote=False) + '\n'
            inedit = True
            
        elif command[0] == 'set':

            if command[1] == 'name': obj_options += set(command, 'Name:', newline=True)

            if command[1] == 'one-arm-ips-urlfilter':
                obj_options += set(command, 'One-arm IPS URL Filter:', newline=True, case='upper')
                onearmips = True
            
            if command[1] == 'ip-addr-block':
                obj_options += set(command, 'IP Addr Block:', newline=True, case='upper')
                ipaddrblock = True
                      
            if command[1] == 'url':
                obj_entries += set(command, 'URL:', newline=True)
                url = True

            if command[1] == 'type':
                obj_entries += set(command, 'Type:', newline=True, case='upper')
                tipo = True

            if command[1] == 'action':
                obj_entries += set(command, 'Action:', newline=True, case='upper')
                action = True
            
            if command[1] == 'status':
                obj_entries += set(command, 'Status:', newline=True, case='upper')
                status = True
            
            if command[1] == 'exempt':
                obj_entries += set(command, 'Exempt:', newline=True, case='upper')
                exempt = True
            
            if command[1] == 'web-proxy-profile':
                obj_entries += set(command, 'Web Proxy Profile:', newline=True, case='upper')
                webproxyprofile = True
            
            if command[1] == 'referrer-host':
                obj_entries += set(command, 'Referrer Host:', newline=True, case='upper')
                referrerhost = True
            
        line = In.readline() # Le a proxima linha