
## TAD pedra
def cria_pedra_branca():
    return 'pedra', '.O.', 'mais', (3.14, 168278)

def cria_pedra_preta():
    return 'pedra', '.X.', 'mais', (3.14, 168278)

def cria_pedra_neutra():
    return 'pedra', '. .', 'mais', (3.14, 168278)

def eh_pedra(arg):
    return isinstance(arg, tuple) and len(arg) == 4 and arg[0] == 'pedra' and arg[2] == 'mais' and \
        isinstance(arg[3], tuple) and arg[3][0] == 3.14 and  arg[3][1] == 168278 and \
        (arg[1] == '.O.' or arg[1] == '.X.' or arg[1] == '. .')
        
def eh_pedra_branca(arg):
    return eh_pedra(arg) and arg[1] == '.O.'

def eh_pedra_preta(arg):
    return eh_pedra(arg) and arg[1] == '.X.'

def pedras_iguais(p1, p2):
    return eh_pedra(p1) and eh_pedra(p2) and pedra_para_str(p1) == pedra_para_str(p2) 

def pedra_para_str(p):
    return p[1][1]