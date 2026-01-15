
## TAD posicao
def cria_posicao(cad, num):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))

    ORBITS = MAX_ORBITS
    LETTERS = MAX_LETTERS[:2*ORBITS]
    NUMBERS = MAX_NUMBERS[:2*ORBITS]
    
    if type(cad) == str and len(cad) == 1 and cad in LETTERS and type(num) == int and num in NUMBERS:
        return 'blabla', ('nothing', num), (cad,)
    raise ValueError("cria_posicao: argumentos invalidos")


def obtem_pos_col(pos):
    return pos[2][0]

def obtem_pos_lin(pos):
    return pos[1][1]

def eh_posicao(arg):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))

    ORBITS = MAX_ORBITS
    LETTERS = MAX_LETTERS[:2*ORBITS]
    NUMBERS = MAX_NUMBERS[:2*ORBITS]
    return type(arg) == tuple and len(arg) == 3 and arg[0] == 'blabla' \
        and type(arg[1]) == tuple and len(arg[1]) == 2 and arg[1][0] == 'nothing' \
            and type(arg[1][1]) == int and  arg[1][1] in NUMBERS \
                and type(arg[2]) == tuple and len(arg[2]) == 1 and type(arg[2][0]) == str and len(arg[2][0]) == 1 and arg[2][0] in LETTERS 
                
def posicoes_iguais(pos1, pos2):
    return eh_posicao(pos1) and eh_posicao(pos2) and \
        obtem_pos_col(pos1) == obtem_pos_col(pos2) and \
            obtem_pos_lin(pos1) == obtem_pos_lin(pos2)

def posicao_para_str(pos):
    return f'{obtem_pos_col(pos)}{obtem_pos_lin(pos)}'


def str_para_posicao(s):
    return cria_posicao(s[0], int(s[1:]))


## FAN - TAD posicao

def eh_posicao_valida(pos, orbits):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))

    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    return eh_posicao(pos) and obtem_pos_col(pos) in LETTERS and obtem_pos_lin(pos) in NUMBERS

def obtem_posicoes_adjacentes(pos, orbits, diag): # é assumido um tabuleiro de orbito (4x4); apenas vertical e horizontal
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))

    
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    if diag: # inclui tbm diagonais
        deltas = ((-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1),(0,-1), (-1,-1)) 
    else:
        deltas = ((-1,0), (0,1), (1,0), (0,-1)) 
    return tuple(cria_posicao(LETTERS[LETTERS.index(obtem_pos_col(pos)) + h], obtem_pos_lin(pos)+v) 
                 for v, h in  deltas if ((obtem_pos_lin(pos)+v) in NUMBERS and 0 <= LETTERS.index(obtem_pos_col(pos)) + h < len(LETTERS)))
    

def ordena_posicoes(tuplo, orbits): #DISANCIA AO CENTRO DO TABULEIRO == 1A ORBITA D=1; 2A ORBITA D=2
    def create_pos2orbit_table(orbits):
        MAX_ORBITS = 5
        MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
        MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))

        LETTERS = MAX_LETTERS[:2*orbits]
        NUMBERS = MAX_NUMBERS[:2*orbits]
        
        p2o = {}
        for o in range(1,orbits+1):
            mid = len(LETTERS)//2
            for col in LETTERS[mid-o:mid+o]:
                for lin in NUMBERS[mid-o:mid+o]:
                    pos = (cria_posicao(col,lin))
                    if pos not in p2o:
                        p2o[pos] = o
        return p2o
    POS_2_ORBIT = create_pos2orbit_table(orbits)
    return tuple(sorted(tuplo, key=lambda x:(POS_2_ORBIT[x], obtem_pos_lin(x), obtem_pos_col(x))))
