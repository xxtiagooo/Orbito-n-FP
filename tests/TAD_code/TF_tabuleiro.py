from random import randint
### TAD tabuleiro

def cria_tabuleiro_vazio(orbits):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    if not (type(orbits) == int and 1 < orbits <= MAX_ORBITS):
        raise ValueError('cria_tabuleiro_vazio: argumento invalido')
     
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    return  [randint(0, 10**6), (orbits, dict((posicao_para_str(cria_posicao(col, lin)), cria_pedra_neutra()) for col in LETTERS for lin in NUMBERS))]


def cria_tabuleiro(orbits, pretas, brancas):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    if not ((type(orbits) == int and 1 < orbits <= MAX_ORBITS) and \
         (isinstance(pretas, tuple) and isinstance(brancas, tuple)) and \
            all(eh_posicao(pos) and eh_posicao_valida(pos, orbits) for pos in pretas + brancas) and \
                len(set(pretas)) == len(pretas) and len(set(brancas)) == len(set(brancas)) and \
                    len(set(pretas + brancas)) == len(pretas + brancas)):
        raise ValueError('cria_tabuleiro: argumentos invalidos')

    tab = cria_tabuleiro_vazio(orbits)
    # coloca pretas
    for pos in pretas:
        coloca_pedra(tab, pos, cria_pedra_preta())
        # coloca pretas
    for pos in brancas:
        coloca_pedra(tab, pos, cria_pedra_branca())
    return tab 

def cria_copia_tabuleiro(tab):
    orbits, tab = tab[1]
    # return dict(((key,tab[key]) for key in tab))
    return  [randint(0, 10**6), (orbits, dict(((key,tab[key]) for key in tab)))]

def obtem_numero_orbitas(tab):
    return tab[1][0]

    
def obtem_pedra(tab, pos):
    tab = tab[1][1]
    return tab[posicao_para_str(pos)]


def obtem_linha_horizontal(tab, pos): # devolve tuplo de tuplos em que cada tuplo é formado por uma par posicao, valor
    def aux_pos2vals(tab, tuplo):
        return tuple((pos, obtem_pedra(tab, pos)) for pos in tuplo) 

    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*ORBITS]
    NUMBERS = MAX_NUMBERS[:2*ORBITS]
    return aux_pos2vals(tab, (cria_posicao(col, obtem_pos_lin(pos)) for col in LETTERS))

def obtem_linha_vertical(tab, pos):
    def aux_pos2vals(tab, tuplo):
        return tuple((pos, obtem_pedra(tab, pos)) for pos in tuplo) 

    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*ORBITS]
    NUMBERS = MAX_NUMBERS[:2*ORBITS]
    return aux_pos2vals(tab, (cria_posicao(obtem_pos_col(pos), lin) for lin in NUMBERS))

def obtem_linhas_diagonais(tab, pos):
    def aux_pos2vals(tab, tuplo):
        return tuple((pos, obtem_pedra(tab, pos)) for pos in tuplo) 

    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*ORBITS]
    NUMBERS = MAX_NUMBERS[:2*ORBITS]
    lado = 2*ORBITS
    
    diagonal = ()
    i ,j = NUMBERS.index(obtem_pos_lin(pos)), LETTERS.index(obtem_pos_col(pos))
    i, j = i-min(i,j), j-min(i,j)
    for d in range(lado):
        if 0 <= i+d < lado and 0 <= j+d < lado: # eh uma posicao Ok
            diagonal += (cria_posicao(LETTERS[j+d], NUMBERS[i+d]),)
                 
    anti_diagonal = ()
    i ,j = NUMBERS.index(obtem_pos_lin(pos)), LETTERS.index(obtem_pos_col(pos))
    i, j = i+min(lado-i-1,j), j-min(lado-i-1,j)
    for d in range(lado):
        if 0 <= i-d < lado and 0 <= j+d < lado: # eh uma posicao Ok
            anti_diagonal += (cria_posicao(LETTERS[j+d], NUMBERS[i-d]),)

    return aux_pos2vals(tab, diagonal), aux_pos2vals(tab, anti_diagonal)

def obtem_posicoes_pedra(tab, pedra):
    res = ()
    for pos in tab[1][1]:
        if pedras_iguais(obtem_pedra(tab, str_para_posicao(pos)), pedra):
            res += (str_para_posicao(pos),)
    
    return ordena_posicoes(res, obtem_numero_orbitas(tab))      
    
def coloca_pedra(tab, pos , pedra):
    tab[1][1][posicao_para_str(pos)] = pedra 
    return tab 

def remove_pedra(tab, pos):
    tab[1][1][posicao_para_str(pos)] = cria_pedra_neutra() 
    return tab 


def eh_tabuleiro(arg):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    def size2orbit(size):
        d = dict(((2*o)**2,o) for o in range(2,MAX_ORBITS+1))
        return d[size] if size in d else 0
    
    def check_cadeia_pos(cad):
        return type(cad) == str and len(cad) in (2,3) and \
            cad[0] in MAX_LETTERS and cad[1:].isdigit() and int(cad[1:]) in MAX_NUMBERS
            
    if isinstance(arg,list) and len(arg) == 2 and type(arg[0]) == int and \
        type(arg[1]) == tuple and len(arg[1]) == 2 and type(arg[1][0]) == int and \
            arg[1][0] in tuple(range(2,MAX_ORBITS+1)) and type(arg[1][1]) == dict and \
                size2orbit(len(arg[1][1])) == arg[1][0]:
        arg = arg[1][1]
        orbits = size2orbit(len(arg))
        return orbits in tuple(range(2,MAX_ORBITS+1))  and len(set(arg.keys())) == len(arg) and\
            all(check_cadeia_pos(pos)  for pos in arg) and \
                all(eh_posicao_valida(str_para_posicao(pos), orbits) for pos in arg) and  \
                    all(eh_pedra(arg[pos]) for pos in arg)
    return False

        
def tabuleiros_iguais(tab1, tab2): # nao sei se está completo
    return eh_tabuleiro(tab1) and eh_tabuleiro(tab2) and tab1[1][0] == tab2[1][0] and \
        len(tab1[1][1]) == len(tab2[1][1]) and all(pos in tab2[1][1] for pos in tab1[1][1]) and \
            all(pedras_iguais(obtem_pedra(tab1, str_para_posicao(pos)), obtem_pedra(tab2, str_para_posicao(pos))) for pos in tab1[1][1])

def tabuleiro_para_str(tab):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    orbits = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
        
    cad = '    ' + '   '.join(LETTERS) + '\n'
    for lin in NUMBERS:
        cad += (f'{lin:02d} [' +']-['.join(pedra_para_str(obtem_pedra(tab, cria_posicao(col, lin))) for col in LETTERS) + ']\n')
        if lin != NUMBERS[-1]:
            cad += (' ' + '   |'*len(LETTERS) + '\n')
    return cad[:-1] 
    

### FAN tabuleiro

def move_pedra(tab, pos1, pos2):
    pedra = obtem_pedra(tab, pos1)
    remove_pedra(tab, pos1)
    coloca_pedra(tab, pos2, pedra)
    return tab 

def obtem_posicao_seguinte(tab, pos, horario):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    def create_nextpos_table(orbits): 
        nextpos_anti, nextpos_hora = {}, {}
        LETTERS = MAX_LETTERS[:2*orbits]
        NUMBERS = MAX_NUMBERS[:2*orbits]
        
        
        for o in range(1,orbits+1):
            mid = len(LETTERS)//2
            corners = ()
            for l in LETTERS[mid-o:mid+o][:-1]:
                corners += (cria_posicao(l,NUMBERS[mid-o]),)
            for n in NUMBERS[mid-o:mid+o][:-1]:
                corners += (cria_posicao(LETTERS[mid+o-1],n),)
            for l in LETTERS[mid-o:mid+o][:0:-1]:
                corners += (cria_posicao(l,NUMBERS[mid+o-1]),) 
            for n in NUMBERS[mid-o:mid+o][:0:-1]:
                corners += (cria_posicao(LETTERS[mid-o],n),)
            
            for i in range(len(corners)):
                nextpos_anti[corners[i]] = corners[i-1]
                nextpos_hora[corners[i-1]] = corners[i]
            
        return nextpos_hora, nextpos_anti  
    NEXT_POS_H, NEXT_POS_A = create_nextpos_table(obtem_numero_orbitas(tab))
    return NEXT_POS_H[pos] if horario else NEXT_POS_A[pos]
        

def roda_tabuleiro(tab):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    orbits = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    new_tab = cria_tabuleiro_vazio(orbits)
    all_pos = tuple(cria_posicao(col, lin) for lin in NUMBERS for col in LETTERS)
    
    # rotate 
    for pos in all_pos:
        coloca_pedra(new_tab, obtem_posicao_seguinte(new_tab, pos, False), obtem_pedra(tab, pos))
        
    # update the original tab
    for pos in all_pos:
        coloca_pedra(tab, pos, obtem_pedra(new_tab, pos))

    return tab

def verifica_linha_pedras(tab, pos, jog, k):
    def unpack_posicoes(tuplo):
        return tuple(p for p, v in tuplo), tuple(v for p, v in tuplo)
    
    eh_jogador = eh_pedra_preta if eh_pedra_preta(jog) else eh_pedra_branca
    
    for linha in (obtem_linha_horizontal(tab, pos), obtem_linha_vertical(tab, pos)) + obtem_linhas_diagonais(tab, pos):
        positions, pedras = unpack_posicoes(linha)
        idx = positions.index(pos) # indice da posicao
        for i in range(k):
            this_line = pedras[idx-i:idx+k-i]
            if len(this_line) == k and all(eh_jogador(pedra) for pedra in this_line):
            # if len(this_line) == k and all(obtem_valor(tab, other) == jog for other in this_line):
                return True  
    return False

