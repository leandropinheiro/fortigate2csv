#!/usr/bin/env python3

def config(cli: list, str_config: str):
    str_config_file = ''.join(cli).rstrip('\n')

    if str_config_file != str_config:
        print('Seu arquivo inicia com: ' + '"' + str_config_file +'"')
        print('Seu arquivo deve iniciar com: ' + '"' + str_config + '"')
        quit()

def edit(cli: list, quote: bool = False):
    str_edit = cli[1]
    
    for x in range(2, len(cli)):
        str_edit = str_edit + ' ' + cli[x]
    
    if quote == False: str_edit = str_edit.replace('"', '')
    
    return str_edit

def set(cli: list, header: str = None, quote: bool = False, tab: bool = False, tab_len: int = 0, newline: bool = False, case: str = None):
    
    str_var = ''
    if quote == True: str_var = '"'
    if header: str_var += header + ' '

    if tab == True and tab_len > 0:
        str_tab = ' ' * tab_len
    else:
        obj_tab = ''
    bol_tab = False

    for x in range(2, len(cli)):
        if cli[x].endswith('"'):
            if len(cli) > 3 and bol_tab == True:
                str_var += str_tab
            if case == 'upper': str_var += cli[x].replace('"', '').upper()
            if case == 'capitalize': str_var += cli[x].replace('"', '').capitalize()
            if case == None: str_var += cli[x].replace('"', '')
            if newline: str_var += '\n'
            if tab == True: bol_tab = True
        else:
            if case == 'upper': str_var += cli[x].replace('"', '').upper()
            if case == 'capitalize': str_var += cli[x].replace('"', '').capitalize()
            if case == None: str_var += cli[x].replace('"', '')
            if not len(cli) <= 3:
                str_var += ' '
            bol_tab = False
    
    str_var

    if newline == True: str_var += '\n'

    return str_var

def write(output_file: str, array: list, debug: bool = False) :
    line = ''
    with open(output_file, 'w') as Out:
        for x in range(len(array)):
            if debug == True: print(array[x])
            line = array[x] + '\n'
            Out.write(line)
