"""Jogo do tipo Orbito-n
Fundamentos Programação
Projeto 2
2024/2025 P1
Tiago Andrês 113875"""

# ------ TAD posição (1,5) --------

"""
# Construtor:
- cria_posicao(col, lin): str x int -> posicao

# Seletores:
- obtem_pos_col(p): posicao -> str
- obtem_pos_lin(p): posicao -> int

# Reconhecedor:
- eh_posicao(arg): universal -> booleano

# Teste:
- posicoes_iguais(p1, p2): posicao x posicao -> booleano

# Transformador:
- posicao_para_str(p): posicao -> str
- str_para_posicao(s): str -> posicao
"""


# construtor

def cria_posicao(col, lin):
    """ str x int -> posicao
    cria uma posição com base nos inputs do utilizador
    coluna - string entre 'a' e 'j'
    linha - inteiro entre 1 e 10"""
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = (range(1, 11))
    if not (type(col) == str and col in colunas and type(lin) == int and lin in linhas):
        raise ValueError("cria_posicao: argumentos invalidos")
    return (col, lin)

# seletores


def obtem_pos_col(p):
    """ posicao -> str
    devolve a coluna onde a posição está inserida"""
    return p[0]


def obtem_pos_lin(p):
    """ posicao -> int
    devolve a linha onde a posição está inserida"""
    return p[1]

# reconhecedor


def eh_posicao(arg):
    """ universal -> booleano
    verifica se o argumento recebido é uma posição do tabuleiro"""
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = (range(1, 11))
    if not (type(arg) == tuple and len(arg) == 2 and type(arg[0]) == str and arg[0] in colunas and type(arg[1]) == int and arg[1] in linhas):
        return False
    return True

# teste


def posicoes_iguais(p1, p2):
    """ universal x universal -> booleano
    verificar se os argumentos são posições do tabuleiro e se são iguais"""
    if not (eh_posicao(p1) and eh_posicao(p2) and p1 == p2):
        return False
    return True

# transformador


def posicao_para_str(p):
    """ posicao -> str
    pegar numa posição e escrever em formato string"""
    return obtem_pos_col(p) + str(obtem_pos_lin(p))


def str_para_posicao(s):
    """ str -> posicao
    pegar numa str e escrever em formato posicao"""
    return cria_posicao(s[0], int(s[1:]))

# --alto nivel--


def eh_posicao_valida(p, n):
    """ posicao x inteiro -> booleano
    ver se a posição dada é valida no tabuleiro com n orbitais, 2 <= n <= 5
    numero de linhas/colunas é dado por 2*n"""
    if not (eh_posicao(p) and type(n) == int and 2 <= n <= 5):
        return False
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = tuple(range(1, 11))
    colunas_n = colunas[:2*n]
    linhas_n = linhas[:2*n]
    if not (obtem_pos_col(p) in colunas_n and obtem_pos_lin(p) in linhas_n):
        return False
    return True


def obtem_posicoes_adjacentes(p, n, d):
    """ posicao x inteiro x booleano -> tuplo
    posicoes adjacentes - posicoes juntas (em qualquer direcao)
    posicoes ortogonais - posicoes juntas verticalmente ou horizontalmente
    se d = True, retornar adjacentes
    se d = False, retornar ortognais
    as posicoes do tuplo vêm ordenadas em sentido horario, começando pela posição em cima de p"""
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = tuple(range(1, 11))
    colunas_n, linhas_n = colunas[:2*n], linhas[:2*n]
    c_pos, l_pos = obtem_pos_col(p), obtem_pos_lin(p)
    ortogonais, adjacentes = (), ()
    coluna_numeros = coluna_para_numeros(p)
    if l_pos - 1 > 0:  # superior
        pos = cria_posicao(c_pos, l_pos - 1)
        ortogonais += (pos,)
        adjacentes += (pos,)
    # superior direita (diagonal)
    if l_pos - 1 > 0 and coluna_numeros + 1 < len(colunas_n):
        adjacentes += (cria_posicao(colunas_n[coluna_numeros + 1], l_pos - 1),)
    if coluna_numeros + 1 < len(colunas_n):   # horizontal direita
        pos = cria_posicao(colunas_n[coluna_numeros + 1], l_pos)
        ortogonais += (pos,)
        adjacentes += (pos,)
    # inferior direita (diagonal)
    if l_pos + 1 <= linhas_n[-1] and coluna_numeros + 1 < len(colunas_n):
        adjacentes += (cria_posicao(colunas_n[coluna_numeros + 1], l_pos + 1),)
    if l_pos + 1 <= linhas_n[-1]:  # inferior
        pos = cria_posicao(c_pos, l_pos + 1)
        ortogonais += (pos,)
        adjacentes += (pos,)
    # inferior esquerda (diagonal)
    if l_pos + 1 <= linhas_n[-1] and coluna_numeros - 1 >= 0:
        adjacentes += (cria_posicao(colunas_n[coluna_numeros - 1], l_pos + 1),)
    if coluna_numeros - 1 >= 0:   # horizontal esquerda
        pos = cria_posicao(colunas_n[coluna_numeros - 1], l_pos)
        ortogonais += (pos,)
        adjacentes += (pos,)
    # superior esquerda (diagonal)
    if l_pos - 1 > 0 and coluna_numeros - 1 >= 0:
        adjacentes += (cria_posicao(colunas_n[coluna_numeros - 1], l_pos - 1),)
    if d:
        return adjacentes
    return ortogonais


def ordena_posicoes(t, n):
    """ tuplo x inteiro -> tuplo
    ordena as posições do tabuleiro de acordo com a sua leitura.
    De dentro para fora, da esquerda para a direita e de cima para baixo"""
    def ordenacao(p):
        # ordenar por orbita de dentro para fora
        sort_1 = obtem_orbita_posicao(p, n)
        sort_2 = obtem_pos_lin(p)   # ordenar por linha
        sort_3 = coluna_para_numeros(p) + 1  # ordenar por coluna
        return (sort_1, sort_2, sort_3)
    return tuple(sorted(t, key=ordenacao))


def coluna_para_numeros(p):  # auxiliar
    """posicao -> int
    transforma a coluna em numeros"""
    return ord(obtem_pos_col(p)) - ord('a')


def numeros_para_coluna(n):  # auxiliar
    """int -> str
    transforma numeros em colunas"""
    return chr(n + ord('a'))

# -------- TAD pedra (1,5) --------

"""
# Construtores
- cria_pedra_branca(): -> pedra
- cria_pedra_preta(): -> pedra
- cria_pedra_neutra(): -> pedra

# Reconhecedor:
- eh_pedra(arg): universal -> booleano
- eh_pedra_branca(p): pedra -> booleano
- eh_pedra_preta(p): pedra -> booleano

# Testes:
- pedras_iguais(p1, p2): pedra x pedra -> booleano

# Transformador:
- pedra_para_str(p): pedra -> str
"""


# construtores

def cria_pedra_branca():
    """ -> pedra
    devolve uma pedra pertencente ao jogador branco"""
    return -1


def cria_pedra_preta():
    """ -> pedra
    devolve uma pedra pertencente ao jogador preto"""
    return 1


def cria_pedra_neutra():
    """ -> pedra
    devolve uma pedra neutra"""
    return 0

# reconhecedor


def eh_pedra(arg):
    """ universal -> booleano
    verifica se é uma pedra"""
    return type(arg) == int


def eh_pedra_branca(p):
    """ pedra -> booleano
    devolve True se for uma pedra branca e falso se nao for"""
    return p == -1


def eh_pedra_preta(p):
    """ pedra -> booleano
    devolve True se for uma pedra preta e falso se nao for"""
    return p == 1

# testes


def pedras_iguais(p1, p2):
    """pedra x pedra -> booleano
    devolve True se as duas pedras forem pedras e iguais"""
    return (eh_pedra(p1) and eh_pedra(p2) and p1 == p2)

# transformador


def pedra_para_str(p):
    """ pedra -> str
    preta = 'X'
    neutra = ' '
    branca = 'O' """
    if eh_pedra_branca(p):
        return 'O'
    elif eh_pedra_preta(p):
        return 'X'
    else:
        return ' '

# --alto nivel--


def eh_pedra_jogador(p):
    """ pedra -> booleano
    verifica se a pedra é de algum jogador"""
    return (eh_pedra_branca(p) or eh_pedra_preta(p))


def pedra_para_int(p):
    """ pedra -> int
    devolve o valor da pedra
    branca = -1
    preta = 1
    neutra = 0 """
    if eh_pedra_branca(p):
        return -1
    elif eh_pedra_preta(p):
        return 1
    else:
        return 0

# -------- TAD tabuleiro (4,0) --------


"""
# Construtor:
- cria_tabuleiro_vazio(n): int -> tabuleiro
- cria_tabuleiro(n, tp, tb): int x tuplo x tuplo -> tabuleiro
- cria_copia_tabuleiro(t): tabuleiro -> tabuleiro

# Seletores:
- obtem_numero_orbitas(t): tabuleiro -> int
- obtem_pedra(t, p): tabuleiro x pedra -> pedra
- obtem_linha_horizontal(t, p): tabuleiro x posicao -> tuplo
- obtem_linha_vertical(t, p): tabuleiro x posicao -> tuplo
- obtem_linhas_diagonais(t, p):tabuleiro x posicao -> tuplo
- obtem_posicoes_pedra(t, j): tabuleiro x pedra -> tuplo

# Modificadores:
- coloca_pedra(t, p, j): tabuleiro x posicao x pedra -> tabuleiro
- remove_pedra(t, p): tabuleiro x posicao -> tabuleiro

# Reconhecedor:
- eh_tabuleiro(arg): universal -> booleano

# Teste:
- tabuleiros_iguais(t1, t2): tabuleiro x tabuleiro -> booleano

# Transformador:
- tabuleiro_para_str(t): tabuleiro -> str
"""


# construtor

def cria_tabuleiro_vazio(n):
    """int -> tabuleiro
    cria um tabuleiro vazio com n órbitas"""
    if not (type(n) == int and n in (2, 3, 4, 5)):
        raise ValueError('cria_tabuleiro_vazio: argumento invalido')
    t = []
    for i in range(2 * n):  # numero de linhas
        linha = [cria_pedra_neutra() for j in range(2 * n)]  # linha nula
        t.append(linha)
    return t


def cria_tabuleiro(n, tp, tb):
    """int x tuplo x tuplo -> tabuleiro
    cria um tabuleiro com as peças de ambos os jogadores"""
    if not (type(n) == int and n in (2, 3, 4, 5) and type(tp) == tuple and type(tb) == tuple):
        raise ValueError('cria_tabuleiro: argumentos invalidos')
    b = list(set(tb))
    p = list(set(tp))
    if len(b) != len(tb) or len(p) != len(tp):
        raise ValueError('cria_tabuleiro: argumentos invalidos')
    i, j = 0, 0
    t = cria_tabuleiro_vazio(n)
    while i < len(b):
        if not (eh_posicao(b[i]) and eh_posicao_valida(b[i], n) and b[i] not in p):
            raise ValueError('cria_tabuleiro: argumentos invalidos')
        t = coloca_pedra(t, b[i], cria_pedra_branca())
        i += 1
    while j < len(p):
        if not (eh_posicao(p[j]) and eh_posicao_valida(p[j], n) and p[j] not in b):
            raise ValueError('cria_tabuleiro: argumentos invalidos')
        t = coloca_pedra(t, p[j], cria_pedra_preta())
        j += 1
    return t


def cria_copia_tabuleiro(t):
    """tabuleiro -> tabuleiro
    devolve uma copia do tabuleiro"""
    return t[:]

# seletores


def obtem_numero_orbitas(t):
    """tabuleiro -> int
    obtem o número de orbitas do tabuleiro"""
    return len(t) // 2


def obtem_pedra(t, p):
    """tabuleiro x pedra -> pedra
    devolve a pedra na posicao p"""
    return t[obtem_pos_lin(p) - 1][coluna_para_numeros(p)]


def obtem_linha_horizontal(t, p):
    """tabuleiro x posicao -> tuplo
    devolve um tuplo de tuplos de dois elementos (posicao, valor) da linha horizontal daquela posicao"""
    coluna = 2 * obtem_numero_orbitas(t)
    l_pos = obtem_pos_lin(p)
    linha = ()
    i = 0
    while i < coluna:
        linha += ((cria_posicao(numeros_para_coluna(i), l_pos),
                  t[l_pos - 1][i]),)
        i += 1
    return linha


def obtem_linha_vertical(t, p):
    """tabuleiro x posicao -> tuplo
    devolve um tuplo de tuplos de dois elementos (posicao, valor) da linha vertical daquela posicao"""
    linha = 2 * obtem_numero_orbitas(t)
    c_pos = obtem_pos_col(p)
    coluna = ()
    i = 0
    while i < linha:
        coluna += ((cria_posicao(c_pos, i + 1), t[i][coluna_para_numeros(p)]),)
        i += 1
    return coluna


def obtem_linhas_diagonais(t, p):
    """tabuleiro x posicao -> tuplo
    devolve um tuplo de tuplos de dois elementos (posicao, valor) das diagonais daquela posicao"""
    l_pos = obtem_pos_lin(p)
    n = obtem_numero_orbitas(t)
    linha = 2 * n
    coluna = 2 * n
    n_col = coluna_para_numeros(p)

    def diagonal(t, l_pos, n_col, linha, coluna):
        """tabuleiro x int x int x int x int -> tuplo
        devolve um tuplo de tuplos de dois elementos (posicao, valor) da diagonal da posicao"""
        diagonal = ()
        while l_pos > 1 and n_col > 0:  # procurar primeiro elemento diagonal
            l_pos -= 1
            n_col -= 1
        while l_pos <= linha and n_col < coluna:
            if 1 <= l_pos <= linha and 0 <= n_col < coluna:
                diagonal += ((cria_posicao(numeros_para_coluna(n_col),
                             l_pos), t[l_pos-1][n_col]),)
            l_pos += 1
            n_col += 1
        return diagonal

    def antidiagonal(t, l_pos, n_col, linha, coluna):
        """tabuleiro x int x int x int x int -> tuplo
        devolve um tuplo de tuplos de dois elementos (posicao, valor) da antidiagonal da posicao"""
        antidiagonal = ()
        # procurar primeiro elemento antidiagonal
        while l_pos < linha and n_col > 0:
            l_pos += 1
            n_col -= 1
        while l_pos > 0 and n_col < coluna:
            if 1 <= l_pos <= linha and 0 <= n_col < coluna:
                antidiagonal += ((cria_posicao(numeros_para_coluna(n_col),
                                 l_pos), t[l_pos-1][n_col]),)
            l_pos -= 1
            n_col += 1
        return antidiagonal
    return (diagonal(t, l_pos, n_col, linha, coluna), antidiagonal(t, l_pos, n_col, linha, coluna))


def obtem_posicoes_pedra(t, j):
    """tabuleiro x pedra -> tuplo
    devolve um tuplo com as posicoes ocupadas por pedras j (brancas, pretas ou neutras)"""
    coluna = len(t[0])
    linha = len(t)
    n = obtem_numero_orbitas(t)
    l = 0
    posicoes = ()
    while l < linha:
        c = 0
        while c < coluna:
            if t[l][c] == j:
                posicoes += (cria_posicao(numeros_para_coluna(c), l + 1),)
            c += 1
        l += 1
    posicoes_ordenadas = ordena_posicoes(posicoes, n)
    return posicoes_ordenadas

# modificadores


def coloca_pedra(t, p, j):
    """tabuleiro x posicao x pedra -> tabuleiro
    coloca a pedra j na posicao p"""
    t[obtem_pos_lin(p) - 1][coluna_para_numeros(p)] = j
    return t


def remove_pedra(t, p):
    """tabuleiro x posicao -> tabuleiro
    remove a pedra na posicao p"""
    t[obtem_pos_lin(p) - 1][coluna_para_numeros(p)] = cria_pedra_neutra()
    return t

# reconhecedor


def eh_tabuleiro(arg):
    """universal -> booleano
    verifica se é um tabuleiro"""
    if not (type(arg) == list and len(arg) > 0 and len(arg) % 2 == 0 and len(arg) == len(arg[0])):
        return False
    for i in arg:
        if not len(i) == len(arg[0]):
            return False
        for j in i:
            if not eh_pedra(j):
                return False
    return True

# teste


def tabuleiros_iguais(t1, t2):
    """tabuleiro x tabuleiro -> booleano
    verifica se os tabuleiros são iguais"""
    if not (eh_tabuleiro(t1) and eh_tabuleiro(t2) and len(t1) == len(t2)):
        return False
    for i in range(len(t1)):
        for j in range(len(t1[0])):
            if not pedras_iguais(t1[i][j], t2[i][j]):
                return False
    return True

# transformador


def tabuleiro_para_str(t):
    """tabuleiro -> str
    devolve uma string que representa o tabuleiro"""
    s = '    '  # 4 espaços antes das colunas
    n = obtem_numero_orbitas(t)
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    colunas_n = colunas[:2*n]
    linhas = tuple(range(1, 11))
    linhas_n = linhas[:2*n]
    for letra in range(len(colunas_n)):  # linha superior (colunas)
        if letra != len(colunas_n) - 1:
            s += colunas_n[letra] + '   '  # 3 espaços entre letras
        else:
            s += colunas_n[letra] + '\n'
    for numero in linhas_n:
        if numero < 10:
            s += '0' + str(numero) + ' '  # 1 espaço entre peças da linha
        else:
            s += str(numero) + ' '  # 1 espaço entre peças da linha
        for j in range(len(t[0])):
            s += '[' + pedra_para_str(t[numero - 1][j]) + ']'
            if j != len(t[0]) - 1:
                s += '-'
        if numero != linhas_n[-1]:
            # 4 espaços (2 do numero + 1 separacao linha coluna + 1 dos parenteses)
            s += '\n' + '    ' + '|   ' * (len(linhas_n)-1) + '|\n'
    return s

# --alto nivel--


def move_pedra(t, p1, p2):
    """tabuleiro x posicao x posicao -> tabuleiro
    move a pedra da posicao p1 para a posicao p2 e devolve o tabuleiro"""
    pedra = obtem_pedra(t, p1)
    t = coloca_pedra(t, p2, pedra)
    t = remove_pedra(t, p1)
    return t


def posicoes_tabuleiro(t, n):  # auxiliar posicao seguinte
    """tabuleiro x int -> tuplo"""
    posicoes = {}
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = tuple(range(1, 11))
    colunas_n = colunas[:2*n]
    linhas_n = linhas[:2*n]
    for coluna in colunas_n:
        for linha in linhas_n:
            pos = (cria_posicao(coluna, linha))
            if obtem_orbita_posicao(pos, n) not in posicoes:
                posicoes[obtem_orbita_posicao(pos, n)] = (pos,)
            else:
                posicoes[obtem_orbita_posicao(pos, n)] += (pos,)
    return posicoes


def obtem_posicao_seguinte(t, p, s):
    """tabuleiro x posicao x booleano -> posicao
    devolve a posicao seguinte a p (na mesma órbita) no tabuleiro t
    se s = True, devolve a posicao seguinte no sentido horario
    se s = False, devolve a posicao seguinte no sentido anti-horario"""
    n = obtem_numero_orbitas(t)
    c_pos = obtem_pos_col(p)
    l_pos = obtem_pos_lin(p)
    orb_p = obtem_orbita_posicao(p, n)
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = tuple(range(1, 11))
    colunas_n = colunas[:2*n]
    linhas_n = linhas[:2*n]
    posicoes = posicoes_tabuleiro(t, n)
    # obter apenas as posicoes da mesma orbita de p
    orb = tuple(posicoes[orb_p])
    tamanho_orb = 2*orb_p
    inicio_slice = n - orb_p
    fim_slice = inicio_slice + tamanho_orb
    col_o = colunas_n[inicio_slice:fim_slice]
    lin_o = linhas_n[inicio_slice:fim_slice]
    pos_candidatas = obtem_posicoes_adjacentes(p, n, False)
    if s:
        if c_pos == col_o[0] and l_pos != lin_o[0]:
            return pos_candidatas[0]   # superior
        if c_pos == col_o[-1] and l_pos != lin_o[-1]:
            return cria_posicao(c_pos,l_pos+1)  # inferior
        if l_pos == lin_o[-1] and c_pos != col_o[0]:
            return pos_candidatas[-1] # ultima posicao adjacente (esquerda)
        if l_pos == lin_o[0] and c_pos != col_o[-1]:
            return cria_posicao(chr(ord(c_pos)+1),l_pos)
    else:
        if c_pos == col_o[0] and l_pos != lin_o[-1]:
            return cria_posicao(c_pos,l_pos + 1)   # inferior
        if c_pos == col_o[-1] and l_pos != lin_o[0]:
            return pos_candidatas[0]  # primeira posicao adjacente (superior)
        if l_pos == lin_o[-1] and c_pos != col_o[-1]:
            return pos_candidatas[1] # segunda posicao adjacente (direita)
        if l_pos == lin_o[0] and c_pos != col_o[0]:
            return pos_candidatas[-1] # ultima posicao adjacente (esquerda)


def roda_tabuleiro(t):
    """tabuleiro -> tabuleiro
    Modifica destrutivamente o tabuleiro t, rotacionando todas as pedras uma posição na órbita no sentido anti-horário."""
    # Lista para armazenar as mudanças de posição para aplicar depois
    rotacoes = []
    # Obter todas as posições das pedras brancas e pretas e calcular suas novas posições
    for pedra in [cria_pedra_branca(), cria_pedra_preta()]:
        posicoes = obtem_posicoes_pedra(t, pedra)  # obter todas as posições ocupadas
        for posicao in posicoes:
            nova_posicao = obtem_posicao_seguinte(t, posicao, False)
            rotacoes.append((nova_posicao, pedra))  # anotar as novas posições (apos rotacao)
    # remover as pedras todas
    for posicao in obtem_posicoes_pedra(t, cria_pedra_branca()) + obtem_posicoes_pedra(t, cria_pedra_preta()):
        remove_pedra(t, posicao)
    # colocar as pedras na posicao apos a rotacao
    for posicao, pedra in rotacoes:
        coloca_pedra(t, posicao, pedra)
    return t


def verifica_linha_pedras(t, p, j, k):
    """tabuleiro x posicao x pedra x int -> booleano
    verifica se existe uma sequencia de k pedras j em qualquer direcao"""
    direcoes = (obtem_linha_horizontal(t, p), obtem_linha_vertical(
        t, p), obtem_linhas_diagonais(t, p)[0], obtem_linhas_diagonais(t, p)[1])
    if obtem_pedra(t,p) != j:
        return False
    for linha in direcoes:
        seguidas = 0
        for posicao_valor in linha:
            pos = posicao_valor[0]
            if obtem_pedra(t, pos) == j:
                seguidas += 1
                if seguidas == k:
                    return True
            else:
                seguidas = 0   # contagem volta a zero
    return False

# ----- Funções adicionais (5,0) -----


def obtem_orbita_posicao(p, n):  # auxiliar
    """posicao x int -> int
    obtem a orbita da posicao, sendo 0 a mais interior"""
    col = coluna_para_numeros(p)
    lin = obtem_pos_lin(p) - 1  # comeca no 0
    # contagem de fora para dentro
    orb_inv = min(col, lin, (2*n-1)-col, (2*n-1)-lin)  # ver o minimo de coluna e linha a contar de cada "lado" do tabuleiro
    return abs(orb_inv - n)  # inverter a contagem


def troca_jogador(jog):  # auxiliar
    """ pedra -> pedra
    alterna o jogador"""
    return cria_pedra_branca() if jog == cria_pedra_preta() else cria_pedra_preta()


def eh_vencedor(t, j):  # 2.2.1 0.5
    """tabuleiro x pedra -> booleano
    verifica se existe uma linha completa de pedras do jogador"""
    n = obtem_numero_orbitas(t)
    k = n * 2
    # verificar as posicoes de todas as orbitas
    for pos in posicoes_tabuleiro(t, n).values():
        for p in pos:
            if verifica_linha_pedras(t, p, j, k):
                return True
    return False


def eh_fim_jogo(t):  # 2.2.2 0.5
    """tabuleiro -> booleano
    verifica se o jogo terminou"""
    n = obtem_numero_orbitas(t)
    k = n * 2
    colunas = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    linhas = tuple(range(1, 11))
    colunas_n = colunas[:2*n]
    linhas_n = linhas[:2*n]
    for l in linhas_n:
        for c in colunas_n:
            pos = cria_posicao(c, l)
            if verifica_linha_pedras(t, pos, cria_pedra_branca(), k) or verifica_linha_pedras(t, pos, cria_pedra_preta(), k):
                return True
    return False


def escolhe_movimento_manual(t):  # 2.2.3 1.0
    """tabuleiro -> posicao
    pede ao utilizador para escolher uma posicao livre"""
    pos = 0  # valor para alterar depois
    while not (eh_posicao(pos) and eh_posicao_valida(pos, obtem_numero_orbitas(t)) and obtem_pedra(t, pos) == cria_pedra_neutra()):
        input_pos = input('Escolha uma posicao livre:')
        if len (input_pos) >= 2 and input_pos[0].isalpha() and input_pos[1:].isdigit():
            pos = str_para_posicao(input_pos)
    return pos


def escolhe_movimento_auto(t, j, lvl):  # 2.2.4 1.5
    """tabuleiro x pedra x str-> posicao
    escolhe uma posicao livre com base na dificuldade escolhida"""
    while not eh_fim_jogo(t):
        if lvl == 'facil':
            return dif_facil(t, j)
        elif lvl == 'normal':
            return dif_normal(t, j)
        else:
            return jogadores_2(t, j)


def dif_facil(t, j):  # auxiliar escolhe_movimento_auto
    """tabuleiro x pedra -> posicao
    se depois de colocar a pedra e rodar o tabuleiro, existir uma posicao livre que fique adjacente a uma posição própria, jogar nessa posicao
    caso contrario, jogar na primeira posicao livre de acordo com a leitura do tabuleiro"""
    n = obtem_numero_orbitas(t)
    roda_t = roda_tabuleiro(t)
    pos_jog = obtem_posicoes_pedra(roda_t, j)
    pos_livres = set(obtem_posicoes_pedra(roda_t, cria_pedra_neutra()))
    pos_adj = set()  # evitar repeticao porque a mesma posicao pode ser adjacente a varias
    for jog in pos_jog:
        pos_adj.update(obtem_posicoes_adjacentes(jog, n, True))  # usar update para adicionar elementos do tuplo
    res = pos_adj.intersection(pos_livres)
    if res:
        jogada = ordena_posicoes(tuple(res), n)[0]
        return obtem_posicao_seguinte(roda_t, jogada, True)
    primeira_livre = list(pos_livres)[0]
    return obtem_posicao_seguinte(t, primeira_livre, True)


def dif_normal(t, j):  # auxiliar escolhe_movimento_auto
    """tabuleiro x pedra -> posicao
    encontrar o maior L < k para que ao fim do turno consiga fazer L pedras seguidas a contar com essa posicao
    ou conseguir que o adversário faça L pedras seguidas, após duas rotcações
    se existir uma posicao que satisfaça a primeira condição, jogar nessa posicao
    se não, jogar uma posicao que impeça o outro jogador de fazer L pedras consecutivas"""
    t = roda_tabuleiro(t)
    roda_2 = roda_tabuleiro(t) 
    n = obtem_numero_orbitas(t)
    L = n * 2
    pos_livres = obtem_posicoes_pedra(t, cria_pedra_neutra())
    pos_livres_ordenadas = ordena_posicoes(pos_livres, n)
    while L > 0:
        jog = j
        for pos in pos_livres_ordenadas:
            t_ofensivo = cria_copia_tabuleiro(t)
            coloca_pedra(t_ofensivo, pos, jog)
            if verifica_linha_pedras(t_ofensivo, pos, jog, L):
                return obtem_posicao_seguinte(t,pos,True)
        jog = troca_jogador(j)
        for pos in pos_livres_ordenadas:
            t_defensivo = cria_copia_tabuleiro(roda_2)
            coloca_pedra(t_defensivo, pos, jog)
            if verifica_linha_pedras(t_defensivo, pos, jog, L):
                return obtem_posicao_seguinte(t,obtem_posicao_seguinte(t,pos,True),True)
        L -= 1
    return pos_livres[0]


def jogadores_2(t, j):  # auxiliar orbito
    """tabuleiro x pedra -> int
    jogo entre dois jogadores"""
    while not eh_fim_jogo(t):
        pos = escolhe_movimento_manual(t)
        t = coloca_pedra(t, pos, j)
        t = roda_tabuleiro(t)
        j = troca_jogador(j)
    return pos


def vencedor(t):  # auxiliar orbito
    """tabuleiro -> int"""
    n = obtem_numero_orbitas(t)
    for pos in posicoes_tabuleiro(t, n):
        if verifica_linha_pedras(t, pos, cria_pedra_preta(), obtem_numero_orbitas(t) * 2):
            return 1
        elif verifica_linha_pedras(t, pos, cria_pedra_branca(), obtem_numero_orbitas(t) * 2):
            return -1
    return 0


def orbito(n, modo, jog):
    """int x str x str -> int
    o jogo começa sempre com o jogador preto
    devolve um inteiro que representa o vencedor do jogo"""
    if not (type(n) == int and n in (2, 3, 4, 5) and type(modo) == str and modo in ('2jogadores', 'facil', 'normal') and type(jog) == str and jog in ('X', 'O')):
        raise ValueError('orbito: argumentos invalidos')
    t = cria_tabuleiro_vazio(n)
    print(f'Bem-vindo ao ORBITO-{n}.')
    if modo == '2jogadores':
        print('Jogo para dois jogadores')
    elif modo == 'facil':
        print('Jogo contra o computador (facil):')
        print(f'O jogador joga com "{jog}".')
    else:
        print('Jogo contra o computador (normal):')
        print(f'O jogador joga com {jog}.')
    print(tabuleiro_para_str(t))
    jog_atual = cria_pedra_preta() if jog == 'X' else cria_pedra_branca()
    if modo != '2jogadores':  # jogo com o computador
        while not eh_fim_jogo(t):
            if jog_atual == (cria_pedra_preta() if jog == 'X' else cria_pedra_branca()):
                print("Turno do jogador.")
                pos = escolhe_movimento_manual(t)
            else:
                print(f"Turno do computador ({modo})")
                pos = escolhe_movimento_auto(t, jog_atual, modo)
            t = coloca_pedra(t, pos, jog_atual)
            t = roda_tabuleiro(t)
            print(tabuleiro_para_str(t))
            jog_atual = troca_jogador(jog_atual)  # trocar de jogador
        if (not (eh_vencedor(t, cria_pedra_preta()) and eh_vencedor(t, cria_pedra_branca())) and len(obtem_posicoes_pedra(t, cria_pedra_neutra())) == 0) or \
                (eh_vencedor(t, cria_pedra_preta()) and eh_vencedor(t, cria_pedra_branca())):
            print("EMPATE")
            return 0
        elif eh_vencedor(t, cria_pedra_preta() if jog == 'X' else cria_pedra_branca()):
            print('VITORIA')
            return 1 if jog == 'X' else -1
        else:
            print('DERROTA')
            return -1 if jog == 'X' else 1

    else:
        jog_atual = cria_pedra_preta()  # começa o 'X'
        while not eh_fim_jogo(t):
            pos = escolhe_movimento_manual(t)
            t = coloca_pedra(t, pos, jog_atual)
            t = roda_tabuleiro(t)
            print(tabuleiro_para_str(t))
            jog_atual = troca_jogador(jog_atual)
            pos = escolhe_movimento_manual(t)
            t = coloca_pedra(t, pos, jog_atual)
            t = roda_tabuleiro(t)
            print(tabuleiro_para_str(t))

        if (not (eh_vencedor(t, cria_pedra_preta()) and eh_vencedor(t, cria_pedra_branca())) and len(obtem_posicoes_pedra(t, cria_pedra_neutra())) == 0) or \
                (eh_vencedor(t, cria_pedra_preta()) and eh_vencedor(t, cria_pedra_branca())):
            print("EMPATE")
            return 0
        elif eh_vencedor(t, cria_pedra_preta()):
            print('VITORIA DO JOGADOR "X"')
            return 1
        else:
            print('VITORIA DO JOGADOR "O"')
            return -1
