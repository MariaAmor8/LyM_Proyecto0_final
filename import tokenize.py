import tokenize
def Tokenizar(archivo):
    tokensList = []
    with tokenize.open(archivo) as f:
        tokens = tokenize.generate_tokens(f.readline)
        for token in tokens:
            if token[0] != 61 and token[0] != 4:
                diccToken = {'type':token[0],'value':token[1].lower()}
                tokensList.append(diccToken)
    print(tokensList)
    return tokensList

def analizeDefVar(tokensList,DiccVar):
    if tokensList[1]['type'] == 1 and tokensList[2]['type'] == 2:
        DiccVar['lstVarGlobales'].append(tokensList[1]['value'])
        tokensList.pop(0)
        tokensList.pop(0)
        tokensList.pop(0) 
    else:
        tokensList = False
    return tokensList

def analizeName(tokensList,DiccVar):
    if tokensList[1]['value'] == '=' and tokensList[2]['type'] == 2:
        DiccVar['lstVarGlobales'].append( tokensList[0]['value'])
        tokensList.pop(0)
        tokensList.pop(0)
        tokensList.pop(0)
    else: 
        tokensList = False
    return tokensList

def analizeBlock(tokensList,DiccVar,boolProc,nombre):
    if tokensList[0]['value'] == '{':
        tokensList.pop(0)
        s = True
        try:
            while tokensList[0]['type'] == 1 and s:
                tokensList = analizeStr(tokensList[0],tokensList,DiccVar,boolProc,nombre)
                    
                if tokensList[0]['value'] == ';' and tokensList[1]['type'] == 1:
                    tokensList.pop(0)
                elif tokensList[0]['value'] != ';' and tokensList[0]['type'] == 1 and tokensList[1]['value'] != '}':
                    s = False
            if tokensList[0]['value'] != '}':
                tokensList = False
            else:
                tokensList.pop(0)
        except:
            tokensList = False
    return tokensList

def analizeDefProc(tokensList,DiccVar,boolProc):
    if tokensList[1]['type'] == 1 and tokensList[2]['value'] == '(':
            nombre = tokensList[1]['value']
            DiccVar['varPorBloque'][nombre] = []
            tokensList.pop(0)
            tokensList.pop(0)
            tokensList.pop(0)
            if tokensList[0]['value'] == ')':
                tokensList.pop(0)
                
            elif tokensList[0]['type'] == 1 and tokensList[1]['value'] == ',':
                while tokensList[1]['value'] == ',' and tokensList[0]['type'] == 1 and tokensList[2]['type'] == 1:
                    DiccVar['varPorBloque'][nombre].append(tokensList[0]['value'])
                    tokensList.pop(0)
                    tokensList.pop(0)
                DiccVar['varPorBloque'][nombre].append(tokensList[0]['value'])
                tokensList.pop(0)
                tokensList.pop(0)
                boolProc = True
            elif tokensList[0]['type'] == 1 and tokensList[1]['value'] == ')':
                DiccVar['varPorBloque'][nombre].append(tokensList[0]['value'])
                tokensList.pop(0)
                tokensList.pop(0)
                boolProc = True
            else:
                tokensList = False
    else:
        tokensList = False
    return tokensList,boolProc,nombre

def analizeDefProcP2(tokensList,DiccVar,boolProc,nombre):
    if tokensList[0]['value'] == '{':
        tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
    else:
        tokensList = False
    return tokensList

def analizeCommandValue(tokensList,DiccVar,boolProc,nombre):
    if tokensList[1]['value'] == '(' and tokensList[3]['value'] == ')':
        if boolProc and tokensList[2]['value'] in DiccVar['varPorBloque'][nombre] or tokensList[2]['type'] == 2 or tokensList[2]['value'] in DiccVar['lstVarGlobales']:
            tokensList.pop(0)
            tokensList.pop(0)
            tokensList.pop(0)
            tokensList.pop(0)
        elif not boolProc and tokensList[2]['value'] in DiccVar['lstVarGlobales'] or tokensList[2]['type'] == 2:
            tokensList.pop(0)
            tokensList.pop(0)
            tokensList.pop(0)
            tokensList.pop(0)
        else:
            tokensList = False
    else:
        tokensList = False
    return tokensList

def analizeNop(tokensList):
    if tokensList[1]['value'] == '(' and tokensList[2]['value'] == ')':
        tokensList.pop(0)
        tokensList.pop(0)
        tokensList.pop(0)
    else:
        tokensList = False
    return tokensList

def analizeJump(tokensList,DiccVar,boolProc,nombre):
    if tokensList[1]['value'] == '(' and tokensList[5]['value'] == ')' and tokensList[3]['value'] == ',':
        if boolProc == True:
            if tokensList[2]['value'] in DiccVar['varPorBloque'][nombre] or tokensList[2]['type'] == 2 or tokensList[2]['value'] in DiccVar['lstVarGlobales'] and tokensList[4]['value'] in DiccVar['varPorBloque'][nombre] or tokensList[4]['type'] == 2 or tokensList[4]['value'] in DiccVar['lstVarGlobales']:
                del tokensList[0:6]
            else:
                tokensList = False
        else:
            if tokensList[2]['value'] in DiccVar['lstVarGlobales'] or tokensList[2]['type'] == 2:
                if tokensList[4]['value'] in DiccVar['lstVarGlobales'] or tokensList[4]['type'] == 2:
                    del tokensList[0:6]
                else:
                    tokensList = False
            else:
                tokensList = False
    else:
        tokensList = False
    return tokensList

def analizeWalkLeapVD(tokensList,DiccVar,boolProc,nombre):
    directions = ['front', 'right', 'left', 'back']
    points = ['north', 'south', 'west', 'east']
    if tokensList[1]['value'] == '(' and tokensList[5]['value'] == ')' and tokensList[3]['value'] == ',':
        if boolProc == True:
            if tokensList[2]['value'] in DiccVar['varPorBloque'][nombre] or tokensList[2]['type'] == 2 or tokensList[2]['value'] in DiccVar['lstVarGlobales'] and tokensList[4]['value'] in directions or tokensList[4]['value'] in points:
                del tokensList[0:6]
            else:
                tokensList = False
        else:
            if tokensList[2]['value'] in DiccVar['lstVarGlobales'] or tokensList[2]['type'] == 2:
                if tokensList[4]['value'] in directions or tokensList[4]['value'] in points:
                    del tokensList[0:6]
                else:
                    tokensList = False
            else:
                tokensList = False
    else:
        tokensList = False
    return tokensList

def analizeTurn(tokensList):
    directions = ['around', 'right', 'left']
    if tokensList[1]['value'] == '(' and tokensList[3]['value'] == ')' and tokensList[2]['value'] in directions:
        del tokensList[0:4]
    else:
        tokensList = False
    return tokensList

def analizeTurnTo(tokensList):
    points = ['north', 'south', 'west', 'east']
    if tokensList[1]['value'] == '(' and tokensList[3]['value'] == ')' and tokensList[2]['value'] in points:
        del tokensList[0:4]
    else:
        tokensList = False
    return tokensList

def analizeCan(tokensList,DiccVar,boolProc,nombre):
    if tokensList[1]['value'] == '(' and tokensList[2]['type'] == 1:
        tokensList.pop(0)
        tokensList.pop(0)
        tokensList = analizeStr(tokensList[0],tokensList,DiccVar,boolProc,nombre)
        if tokensList != False and tokensList[0]['value'] == ')':
            tokensList.pop(0)
    else:
        tokensList = False
    return tokensList

def analizeNot(tokensList,DiccVar,boolProc,nombre):
    if tokensList[1]['value'] == ':' and tokensList[2]['value'] == 'facing' or tokensList[2]['value'] == 'can':
        tokensList.pop(0)
        tokensList.pop(0)
        tokensList= analizeStr(tokensList[0],tokensList,DiccVar,boolProc,nombre)
    else:
        tokensList = False
    return tokensList

def analizeConditional(tokensList,DiccVar,boolProc,nombre):
    if tokensList[1]['value'] == 'facing' or tokensList[1]['value'] == 'can' or tokensList[1]['value'] == 'nop':
        tokensList.pop(0)
        tokensList= analizeStr(tokensList[0],tokensList,DiccVar,boolProc,nombre)
        if tokensList != False:
            tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
            if tokensList != False and tokensList[0]['value'] == 'else' and tokensList[1]['value'] == '{':
                tokensList.pop(0)
                tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
            else:
                tokensList = False
        else:
            tokensList = False
    return tokensList

def analizeLoop(tokensList,DiccVar,boolProc,nombre):
    tokensList.pop(0)
    if tokensList[0]['value'] == 'can':
        tokensList = analizeCan(tokensList,DiccVar,boolProc,nombre)
    elif tokensList[0]['value'] == 'facing':
        tokensList = analizeTurnTo(tokensList,DiccVar,boolProc,nombre)
    elif tokensList[0]['value'] == 'not':
        tokensList = analizeNot(tokensList,DiccVar,boolProc,nombre)
        if tokensList != False and tokensList[0]["value"] == '{':
            tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
        else:
            tokensList = False
    else:
        tokensList = False
    return tokensList

def analizeRepeatTimes(tokensList,DiccVar,boolProc,nombre):
    if boolProc == True:
        if tokensList[1]['value'] in DiccVar['varPorBloque'][nombre] or tokensList[1]['type'] == 2 or tokensList[1]['value'] in DiccVar['lstVarGlobales'] and tokensList[2]['value'] == 'times' and tokensList[2]['value'] == '{':
            del tokensList[0:3]
            tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
        else:
            tokensList = False
    else: 
        if tokensList[1]['value'] in DiccVar['lstVarGlobales'] or tokensList[1]['type'] == 2 and tokensList[2]['value'] == 'times' and tokensList[3]['value'] == '{':
            del tokensList[0:3]
            tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
    return tokensList

def analizeFuncion(tokensList,DiccVar,boolProc,nombre):
    ret = ''
    param = len(DiccVar['varPorBloque'][tokensList[0]['value']])
    cantReal = 0
    if tokensList[0]['type'] == 1 and tokensList[1]['value'] == '(' and tokensList[2]['type'] == 1 or tokensList[2]['type'] == 2:
        tokensList.pop(0)
        tokensList.pop(0)
        
        while tokensList[1]['value'] == ',' and tokensList[0]['type'] == 2 or tokensList[0]['type'] == 1 and tokensList[2]['type'] == 1 or tokensList[2]['type'] == 1 or tokensList[0]['value'] in DiccVar['lstVarGlobales'] or tokensList[2]['value'] in DiccVar['lstVarGlobales']:
            tokensList.pop(0)
            tokensList.pop(0)
            cantReal += 1
            
        if tokensList[1]['value'] == ')':
            print('yuyuy')
            tokensList.pop(0)
            tokensList.pop(0)
            cantReal += 1
        print(cantReal)
        print(param)
        if cantReal == param:
            ret = tokensList
        
        else:
            ret = False
            
    elif tokensList[0]['type'] == 1 and tokensList[1]['value'] == '(' and tokensList[2]['value'] == ')' and cantReal == 0:
        del tokensList[0:3]
        ret= tokensList
    
    else:
        ret = False
    return ret


#analize string -> analiza comandos básicos

def analizeStr(token,tokensList,DiccVar,boolProc,nombre):
    try:
        if token['value'] == "defvar":
            tokensList = analizeDefVar(tokensList,DiccVar)
        
        elif token['type'] == 1 and tokensList[1]['value'] == '=':
            tokensList = analizeName(tokensList,DiccVar)
            
        elif token['value'] == "defproc":
            tokensList,boolProc,nombre = analizeDefProc(tokensList,DiccVar,boolProc)
            if tokensList != False:
                tokensList = analizeDefProcP2(tokensList,DiccVar,boolProc,nombre)
                
        elif token['value'] == "{":
            tokensList = analizeBlock(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] == 'drop' or token['value'] == 'get'or token['value'] == 'grab' or token['value'] == 'letgo':
            tokensList = analizeCommandValue(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] == 'jump':
            tokensList = analizeJump(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] == 'walk' or token['value'] == 'leap':
            if tokensList[1]['value'] == '(' and tokensList[3]['value'] == ')':
                tokensList = analizeCommandValue(tokensList,DiccVar,boolProc,nombre) 
            elif tokensList[1]['value'] == '(' and tokensList[5]['value'] == ')':
                tokensList = analizeWalkLeapVD(tokensList,DiccVar,boolProc,nombre)
            else:
                tokensList = False
                
        elif token['value'] == 'turn':
            tokensList = analizeTurn(tokensList)
        
        elif token['value'] == 'turnto' or token['value'] == 'facing':
            tokensList = analizeTurnTo(tokensList)
        
        elif token['value'] == 'can':
            tokensList = analizeCan(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] == 'nop':
            tokensList = analizeNop(tokensList)
            
        elif token['value'] == 'if':
            tokensList = analizeConditional(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] == 'while':
            tokensList= analizeLoop(tokensList,DiccVar,boolProc,nombre)
           
        elif token['value'] == 'repeat':
            tokensList= analizeRepeatTimes(tokensList,DiccVar,boolProc,nombre)
            
        elif token['value'] in DiccVar['varPorBloque'].keys():
            tokensList = analizeFuncion(tokensList,DiccVar,boolProc,nombre)
            
        elif token['type'] == 0:
            return tokensList
            
        else:
            tokensList = False
    except:
        tokensList = False
    return tokensList

def read(token,tokensList,DiccVar):
    iProcc = 0
    if token["type"] == 1 or token["type"] == 54:
        tokensList = analizeStr(token,tokensList,DiccVar,False,"")
    else:
        tokensList = False
        
    return tokensList

def ejecutar():
    lista = Tokenizar('hello.txt')
    DiccVar = {'lstVarGlobales':[],'varPorBloque':{}}
    while lista:
        lista = read(lista[0],lista,DiccVar)
        try:
            if lista[0]['type'] == 0 or lista == []:
                lista = False
                rta = True
        except:
            rta = False
    print("lista de variables -> " + str(DiccVar))
    print(rta)
     
ejecutar()