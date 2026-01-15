##############
### ORBITA ###
##############

GLB_MAX_ORBITS = 5
GLB_MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*GLB_MAX_ORBITS]
GLB_MAX_NUMBERS = tuple(range(1,2*GLB_MAX_ORBITS + 1))

## Some AUX functionality

def create_pos2orbit_table(orbits):
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    p2o = {}
    for o in range(1,orbits+1):
        mid = len(LETTERS)//2
        for col in LETTERS[mid-o:mid+o]:
            for lin in NUMBERS[mid-o:mid+o]:
                pos = (cria_posicao(col,lin))
                if pos not in p2o:
                    p2o[pos] = o
    return p2o

def create_nextpos_table(orbits): 
    nextpos_anti, nextpos_hora = {}, {}
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    
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

### TAD posicao (imutável)
def cria_posicao(cad, num):
    ORBITS = GLB_MAX_ORBITS
    LETTERS = GLB_MAX_LETTERS[:2*ORBITS]
    NUMBERS = GLB_MAX_NUMBERS[:2*ORBITS]
    
    if type(cad) == str and len(cad) == 1 and cad in LETTERS and type(num) == int and num in NUMBERS:
        return cad,num 
    raise ValueError("cria_posicao: argumentos invalidos")

def obtem_pos_col(pos):
    return pos[0]

def obtem_pos_lin(pos):
    return pos[1]

def eh_posicao(val):
    ORBITS = GLB_MAX_ORBITS
    LETTERS = GLB_MAX_LETTERS[:2*ORBITS]
    NUMBERS = GLB_MAX_NUMBERS[:2*ORBITS]
    
    return type(val) == tuple and len(val) == 2 and \
        type(val[0]) == str and len(val[0]) == 1 and val[0] in LETTERS and \
            type(val[1]) == int and val[1] in NUMBERS

def posicoes_iguais(p1, p2):
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2 

def posicao_para_str(pos):
    return f'{pos[0]}{pos[1]}'

def str_para_posicao(cad):
    return cad[0],int(cad[1:])

# FANs
def obtem_posicoes_adjacentes(pos, orbits, diag): 
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    if diag: # inclui tbm diagonais
        deltas = ((-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1),(0,-1), (-1,-1)) 
    else:
        deltas = ((-1,0), (0,1), (1,0), (0,-1)) 
    return tuple(cria_posicao(LETTERS[LETTERS.index(obtem_pos_col(pos)) + h], obtem_pos_lin(pos)+v) 
                 for v, h in  deltas if ((obtem_pos_lin(pos)+v) in NUMBERS and 0 <= LETTERS.index(obtem_pos_col(pos)) + h < len(LETTERS)))


def ordena_posicoes(tuplo, orbits): 
    POS_2_ORBIT = create_pos2orbit_table(orbits)
    return tuple(sorted(tuplo, key=lambda x:(POS_2_ORBIT[x], obtem_pos_lin(x), obtem_pos_col(x))))

        
def eh_posicao_valida(pos, orbits):
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    return eh_posicao(pos) and obtem_pos_col(pos) in LETTERS and obtem_pos_lin(pos) in NUMBERS

# TAD Pedra
def cria_pedra_branca():
    return -1

def cria_pedra_preta():
    return 1 

def cria_pedra_neutra():
    return 0 

def eh_pedra(arg):
    return type(arg) == int and arg in (1,-1,0)

def eh_pedra_branca(arg):
    return eh_pedra(arg) and arg == -1
                
def eh_pedra_preta(arg):
    return eh_pedra(arg) and arg == 1

def pedras_iguais(p1, p2):
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2 

def pedra_para_str(p):
    return 'X' if eh_pedra_preta(p) else ('O' if eh_pedra_branca(p) else ' ') 

#FANs
def eh_pedra_jogador(p):
    return eh_pedra(p) and (eh_pedra_branca(p) or eh_pedra_preta(p))

def pedra_para_int(p):
    pedras = {pedra_para_str(cria_pedra_preta()):1, 
         pedra_para_str(cria_pedra_branca()):-1,
         pedra_para_str(cria_pedra_neutra()):0}
    
    return pedras[pedra_para_str(p)]

### TAD tabuleiro

def cria_tabuleiro_vazio(orbits):
    if not (type(orbits) == int and 1 < orbits <= GLB_MAX_ORBITS):
        raise ValueError('cria_tabuleiro_vazio: argumento invalido')
     
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    return dict((posicao_para_str(cria_posicao(col, lin)), cria_pedra_neutra()) for col in LETTERS for lin in NUMBERS)

def cria_tabuleiro(orbits, pretas, brancas):
    if not ((type(orbits) == int and 1 < orbits <= GLB_MAX_ORBITS) and \
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
    return dict(((key,tab[key]) for key in tab))

def obtem_numero_orbitas(tab):
    return size2orbit(len(tab))
    
def size2orbit(size):
    d = dict(((2*o)**2,o) for o in range(2,GLB_MAX_ORBITS+1))
    return d[size] if size in d else 0

def obtem_pedra(tab, pos):
    return tab[posicao_para_str(pos)]

def aux_pos2vals(tab, tuplo):
    return tuple((pos, tab[posicao_para_str(pos)]) for pos in tuplo) 

def obtem_linha_horizontal(tab, pos): # devolve tuplo de tuplos em que cada tuplo é formado por uma par posicao, valor
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*ORBITS]
    NUMBERS = GLB_MAX_NUMBERS[:2*ORBITS]
    return aux_pos2vals(tab, (cria_posicao(col, obtem_pos_lin(pos)) for col in LETTERS))

def obtem_linha_vertical(tab, pos):
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*ORBITS]
    NUMBERS = GLB_MAX_NUMBERS[:2*ORBITS]
    return aux_pos2vals(tab, (cria_posicao(obtem_pos_col(pos), lin) for lin in NUMBERS))

def obtem_linhas_diagonais(tab, pos):
    ORBITS = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*ORBITS]
    NUMBERS = GLB_MAX_NUMBERS[:2*ORBITS]
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
    for pos in tab:
        if pedras_iguais(obtem_pedra(tab, str_para_posicao(pos)), pedra):
            res += (str_para_posicao(pos),)
    
    return ordena_posicoes(res, obtem_numero_orbitas(tab))        
    
def coloca_pedra(tab, pos , pedra):
    tab[posicao_para_str(pos)] = pedra 
    return tab 

def remove_pedra(tab, pos):
    tab[posicao_para_str(pos)] = cria_pedra_neutra() 
    return tab 

def eh_tabuleiro(arg):
    def check_cadeia_pos(cad):
        return type(cad) == str and len(cad) in (2,3) and \
            cad[0] in GLB_MAX_LETTERS and cad[1:].isdigit() and int(cad[1:]) in GLB_MAX_NUMBERS
            
    if isinstance(arg, dict):
        orbits = size2orbit(len(arg))
        return orbits in tuple(range(2,GLB_MAX_ORBITS+1))  and len(set(arg.keys())) == len(arg) and\
            all(check_cadeia_pos(pos)  for pos in arg) and \
            all(eh_posicao_valida(str_para_posicao(pos), orbits) for pos in arg) and  \
                all(eh_pedra(arg[pos]) for pos in arg)
    return False
        
def tabuleiros_iguais(tab1, tab2): # nao sei se está completo
    return eh_tabuleiro(tab1) and eh_tabuleiro(tab2) and len(tab1) == len(tab2) and \
        all(pos in tab2 for pos in tab1) and all(pedras_iguais(tab1[pos],tab2[pos]) for pos in tab1)
    
def tabuleiro_para_str(tab):
    orbits = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
        
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
    NEXT_POS_H, NEXT_POS_A = create_nextpos_table(obtem_numero_orbitas(tab))
    return NEXT_POS_H[pos] if horario else NEXT_POS_A[pos]
        
def roda_tabuleiro(tab):
    orbits = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
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
                return True  
    return False

### FANs finais
def eh_vencedor(tab, jogador):
    orbits = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    # nao preciso em todas basta com a primeira linha e a primeira coluna
    all_pos = tuple(cria_posicao('a', lin) for lin in NUMBERS) + \
        tuple(cria_posicao(col, 1) for col in LETTERS)
    
    return any(verifica_linha_pedras(tab, pos, jogador,2*orbits) for pos in all_pos)
             

def eh_fim_jogo(tab):
    orbits = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]
    
    all_pos = tuple(cria_posicao(col, lin) for lin in NUMBERS for col in LETTERS)
    return all((eh_pedra_jogador(obtem_pedra(tab, pos)) for pos in all_pos)) or \
        (eh_vencedor(tab, cria_pedra_branca()) or eh_vencedor(tab, cria_pedra_preta()))

def escolhe_movimento_manual(tab):
    orbits = obtem_numero_orbitas(tab)
    LETTERS = GLB_MAX_LETTERS[:2*orbits]
    NUMBERS = GLB_MAX_NUMBERS[:2*orbits]

    while True:
        # Repetir pergunta até escolher uma posicao valida 
        cad = input('Escolha uma posicao livre:')
        if len(cad) >= 2 and cad[0] in LETTERS and cad[1:].isdigit() and int(cad[1:]) in NUMBERS:
            pos = cria_posicao(cad[0], int(cad[1:]))
            
            if not eh_pedra_jogador(obtem_pedra(tab, pos)):
                return pos 

def facil(tab, jog):
    new_tab = cria_copia_tabuleiro(tab)
    orbits = obtem_numero_orbitas(new_tab)
        
    # Roto uma copia do tabuleiro
    roda_tabuleiro(new_tab)

    #Procuro todas as posiçoes livres adjacentes a uma pedra propria
    proprias = obtem_posicoes_pedra(new_tab, jog)
    livres = set()
    for pos in proprias:
        this_livres = set(adj for adj in obtem_posicoes_adjacentes(pos, orbits,True) 
            if not eh_pedra_jogador(obtem_pedra(new_tab, adj)))
        livres = livres.union(this_livres)
    
    # Procuro para todas elas a posicao anterior
    anterior = ()
    if livres: # se existe pelo menos uma posicao
        for pos in livres:
            previous = obtem_posicao_seguinte(new_tab, pos, True)
            # if not eh_pedra_jogador(obtem_pedra(tab, previous)): # not sure this verification makes sense, 
            anterior += (previous,)
                
    return ordena_posicoes(anterior, orbits)    

def normal(tab, jog):
    new_tab = cria_copia_tabuleiro(tab)
    orbits = obtem_numero_orbitas(tab)
    res = {}
    
    for pedra in (jog, cambio_turno(jog)):
        # Roto a copia do tabuleiro uma vez em cada ciclo
        roda_tabuleiro(new_tab)
        livres =  obtem_posicoes_pedra(new_tab, cria_pedra_neutra())
    
        #Procuro L no tabuleiro rotado para pedras pedra
        for k in range(orbits*2, 0, -1):
            candidates = ()
            for pos in livres:
                sim_tab = cria_copia_tabuleiro(new_tab)
                coloca_pedra(sim_tab, pos, pedra)
                if verifica_linha_pedras(sim_tab, pos, pedra, k):
                    candidates += (pos,)
            if candidates:
                break
        res[pedra] = (k, candidates)
    
    if res[jog][0] >= res[cambio_turno(jog)][0]: # uma rotação
        candidates = tuple(obtem_posicao_seguinte(tab, pos, True) for pos in res[jog][1])
    else: # duas rotacoes
        candidates = tuple(obtem_posicao_seguinte(tab, obtem_posicao_seguinte(tab, pos, True), True) for pos in res[cambio_turno(jog)][1])       
    
    return ordena_posicoes(candidates, orbits)
    
def escolhe_movimento_auto(tab, pedra, lvl):
    mode = {'facil': facil,
            'normal': normal}
    
    candidates = mode[lvl](tab, pedra)    
    if not candidates:
        candidates = obtem_posicoes_pedra(tab, cria_pedra_neutra())
    
    return candidates[0]
 
cambio_turno = lambda jog: (cria_pedra_preta() if pedras_iguais(jog, cria_pedra_branca()) else cria_pedra_branca())
  
def orbito(orbits, mode, jogador):  
    def print_winner(jogador):
        def get_winner(tab):
            # Há dois ganhadores --> é considerado empate
            if eh_vencedor(tab, cria_pedra_branca()) and eh_vencedor(tab, cria_pedra_preta()):
                return cria_pedra_neutra()
            elif eh_vencedor(tab, cria_pedra_branca()):
                return cria_pedra_branca()
            elif eh_vencedor(tab, cria_pedra_preta()):
                return cria_pedra_preta()
            else:
                return cria_pedra_neutra()
        
        winner = get_winner(tab)
        if pedras_iguais(winner, cria_pedra_neutra()):
            print("EMPATE")
        elif mode == '2jogadores':
            print(f"VITORIA DO JOGADOR '{pedra_para_str(winner)}'")
        elif pedras_iguais(winner, jogador):
            print("VITORIA")
        else:
            print("DERROTA")
                    
        return pedra_para_int(winner)
    
    if not (type(orbits) == int and 2 <= orbits <= 5 and 
        type(mode) == str and mode in ('facil', 'normal', '2jogadores') and 
        type(jogador) == str and jogador in ('X', 'O')):
            raise ValueError("orbito: argumentos invalidos")

    jogador = cria_pedra_preta() if jogador == 'X' else cria_pedra_branca()
    
    print(f"Bem-vindo ao ORBITO-{orbits}.")
    if mode == '2jogadores':
        print(f"Jogo para dois jogadores.")
    else:
        print(f"Jogo contra o computador ({mode}).")
        print(f"O jogador joga com '{pedra_para_str(jogador)}'.")
        
    tab = cria_tabuleiro_vazio(orbits)
    
    turno = cria_pedra_preta()
    
    while not eh_fim_jogo(tab):
        print(tabuleiro_para_str(tab))
        if mode == '2jogadores':
            print(f"Turno do jogador '{pedra_para_str(turno)}'.")
            jogada = escolhe_movimento_manual(tab)
        elif pedras_iguais(turno, jogador):
            print("Turno do jogador.")
            jogada = escolhe_movimento_manual(tab)
        else:
            print(f"Turno do computador ({mode}):")
            jogada = escolhe_movimento_auto(tab, turno, mode)
             
        # Coloca a pedra
        coloca_pedra(tab, jogada, turno)
        roda_tabuleiro(tab)

        turno = cambio_turno(turno)
    
    print(tabuleiro_para_str(tab))
    return print_winner(jogador)
    