#!/usr/bin/env python3

import argparse
import time
import importlib.util
from pathlib import Path
from fortigate2csv import *
#from netaddr import IPAddress

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
    
    line_out = '"EDIT";"NAME";"POLICY"'
    buffer_out = []
    buffer_out.append(line_out)

    print("buffer:", buffer_out, "\n")

    while line:
        cli = line.lstrip(' ')
        command = cli.split()
        
        if command[0] == 'config': # Verifica se a linha corresponde a CONFIG
            correto = 'Seu arquivo deve iniciar com: "config firewall address"\n'
            errado = 'config'
            if command[1] == 'firewall': # Verifica se a linha corresponde a CONFIG FIREWALL
                errado = 'config firewall'
                if command [2] == 'policy': # Verifica se a linha corresponde a CONFIG FIREWALL POLICY
                    print('!', end='')
                else:
                    print('Arquivo Incorreto!!!\n')
                    for x in range(2, len(command)):
                        errado = errado + ' ' + command[x]
                    print('Seu arquivo inicia com: ' + errado)
                    print(correto)
                    quit()
            else:
                print('Arquivo Incorreto!!!\n')
                for x in range(1, len(command)):
                    errado = errado + ' ' + command[x]
                print('Seu arquivo inicia com: ' + errado)
                print(correto)
                quit()

        elif command[0] == 'end': # Verifica se a linha corresponde a END
            print('                                                   ', end='\r')
            print('*')

        elif command[0] == 'next':  # Verifica se a linha corresponde a NEXT
            print('                                                   ', end='\r')
            
            if obj_name == '':
                obj_name == '"-"'

            line_out = '"' + obj_edit + '"'
            line_out = line_out + ';"' + obj_name.rstrip(' \n') + '"'
            line_out = line_out + ';"' + obj_policy.rstrip(' \n') + '"'

            buffer_out.append(line_out)

        elif command[0] == 'edit':  # Verifica se a linha corresponde a EDIT
            print('^', end='')
            
            obj_edit = edit(command)
            
            #obj_edit = obj_edit.replace('"', '')
            obj_name = ''
            obj_policy = ''

        elif command[0] == 'set':  # Verifica se a linha corresponde a SET
            print('.', end='')

            if command[1] == 'name':
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_name += command[x].replace('"', '') + '\n'
                    else:
                        obj_name += command[x].replace('"', '') + ' '
            
            if command[1] == 'srcintf':
                obj_policy += 'Source Iface: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'dstintf':
                obj_policy += 'Dest Iface: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '
    
            if command[1] == 'srcaddr':
                obj_policy += set(command, 'Source Addr:', False, True, 22)

            if command[1] == 'dstaddr':
                obj_policy += set(command,'Dest Addr:', False, True, 18)

            if command[1] == 'action':
                obj_policy += 'Action: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '
                obj_policy += '\n'

            if command[1] == 'schedule':
                obj_policy += 'Schedule: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '

            if command[1] == 'service':
                obj_policy += 'Service: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'utm-status':
                obj_policy += 'UTM-Status: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '
                obj_policy += '\n'

            if command[1] == 'fixedport':
                obj_policy += 'Fixed Port: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '
                obj_policy += '\n'

            if command[1] == 'groups':
                obj_policy += 'FSSO: ENABLED\n'
                obj_policy += 'Groups: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'fsso':
                obj_policy += 'FSSO: DISABLE\n'

            if command[1] == 'webfilter-profile':
                obj_policy += 'Webfilter Profile: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'application-list':
                obj_policy += 'Application List: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'ssl-ssh-profile':
                obj_policy += 'SSL/SSH Profile: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '') + '\n'
                    else:
                        obj_policy += command[x].replace('"', '') + ' '

            if command[1] == 'nat':
                obj_policy += 'NAT: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '
                obj_policy += '\n'

            if command[1] == 'comments':
                obj_policy += 'Comments: '
                for x in range(2, len(command)):
                    if command[x].endswith('"'):
                        obj_policy += command[x].replace('"', '').upper() + '\n'
                    else:
                        obj_policy += command[x].replace('"', '').upper() + ' '

        line = In.readline() # Le a proxima linha
    
    #with open(Output, 'w') as Out:
    #    for x in range(len(buffer_out)):
    #       print(buffer_out[x])
    #       line = buffer_out[x] + '\n'
    #       Out.write(line)
    write(Output, buffer_out, True)