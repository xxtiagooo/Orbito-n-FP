import pytest
import sys
projet_filename = '/wsl.localhost/Ubuntu/home/tiago/ist/2024-2025/S1/FP/proj 2/FP2425P2.py'
TAD_CODE_PATH = '/wsl.localhost/Ubuntu/home/tiago/ist/2024-2025/S1/FP/proj 2/tests/TAD_code/'
SAMPLE_DIR = '/wsl.localhost/Ubuntu/home/tiago/ist/2024-2025/S1/FP/proj 2/tests/expected'
import FP2425P2 as fp 

class TestPublicPosicao:

    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            i1 = fp.cria_posicao('a', 21)        
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
    
    def test_2(self):
        assert not fp.posicoes_iguais(fp.cria_posicao('a', 2), fp.cria_posicao('b', 3))

    def test_3(self):
        assert fp.posicoes_iguais(fp.cria_posicao('a', 2), fp.str_para_posicao('a2'))

    def test_4(self):
        assert fp.posicao_para_str(fp.cria_posicao('b', 3)) == 'b3'

    def test_5(self):
        i1 = fp.cria_posicao('a', 2)
        assert ('a1', 'b2', 'a3') == tuple(fp.posicao_para_str(i) for i in fp.obtem_posicoes_adjacentes(i1, 2, False))
        
    def test_6(self):
        i1 = fp.cria_posicao('a', 2)
        assert ('a1', 'b1', 'b2', 'b3', 'a3') == tuple(fp.posicao_para_str(i) for i in fp.obtem_posicoes_adjacentes(i1, 2, True))    
        
    def test_7(self):
        tup = (fp.cria_posicao('a',1), fp.cria_posicao('a',3), fp.cria_posicao('b',1), fp.cria_posicao('b',2))
        assert ('b2', 'a1', 'b1', 'a3') == tuple(fp.posicao_para_str(i) for i in fp.ordena_posicoes(tup, 2))
    
    

class TestPublicPedra:

    def test_1(self):
        assert  fp.eh_pedra(fp.cria_pedra_branca())

    def test_2(self):
        assert not fp.pedras_iguais(fp.cria_pedra_branca(), fp.cria_pedra_preta())

    def test_3(self):
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        assert fp.pedra_para_str(b), fp.pedra_para_str(p) == ('O', 'X')
    
    def test_4(self):
        assert not fp.eh_pedra_jogador(fp.cria_pedra_neutra())
        
    def test_5(self):
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        assert fp.pedra_para_int(b), fp.pedra_para_int(p) == (-1, 1)
             
        
        
class TestPublicTabuleiro:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            tab = fp.cria_tabuleiro_vazio(12)
        assert "cria_tabuleiro_vazio: argumento invalido" == str(excinfo.value)

    def test_2(self):
        assert fp.eh_tabuleiro(fp.cria_tabuleiro_vazio(2))
        
    def test_3(self):
        tab = fp.cria_tabuleiro_vazio(2)
        pos = fp.cria_posicao('c',2)
        assert fp.pedra_para_str(fp.obtem_pedra(tab, pos)) == ' '
        
    def test_4(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        hyp = \
"""    a   b   c   d
01 [ ]-[X]-[O]-[ ]
    |   |   |   |
02 [ ]-[ ]-[O]-[O]
    |   |   |   |
03 [X]-[X]-[X]-[O]
    |   |   |   |
04 [X]-[ ]-[ ]-[O]"""

        assert fp.tabuleiro_para_str(tab) == hyp
      
    def test_5(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        pos = fp.cria_posicao('c',3)
        ref =  (('c1', 'O'), ('c2', 'O'), ('c3', 'X'), ('c4', ' '))
        assert tuple((fp.posicao_para_str(p), fp.pedra_para_str(v)) for p, v in fp.obtem_linha_vertical(tab, pos)) == ref

    def test_6(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        diag, anti = fp.obtem_linhas_diagonais(tab, fp.cria_posicao('c',3))
        ref_d = (('a1', ' '), ('b2', ' '), ('c3', 'X'), ('d4', 'O'))
        ref_a = (('b4', ' '), ('c3', 'X'), ('d2', 'O'))
        assert tuple((fp.posicao_para_str(p), fp.pedra_para_str(v)) for p, v in diag) == ref_d and \
            tuple((fp.posicao_para_str(p), fp.pedra_para_str(v)) for p, v in anti) == ref_a


    def test_7(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        _ = fp.roda_tabuleiro(tab)
        assert fp.tabuleiro_para_str(tab) == \
"""    a   b   c   d
01 [X]-[O]-[ ]-[O]
    |   |   |   |
02 [ ]-[O]-[X]-[O]
    |   |   |   |
03 [ ]-[ ]-[X]-[O]
    |   |   |   |
04 [X]-[X]-[ ]-[ ]"""

    def test_8(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        
        assert (not fp.verifica_linha_pedras(tab,fp.cria_posicao('d',1), fp.cria_pedra_branca(), 3)) and \
            fp.verifica_linha_pedras(tab,fp.cria_posicao('d',2), fp.cria_pedra_branca(), 3)
        
    def test_9(self):
        orbits = 2
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        ib = tuple(fp.str_para_posicao(i) for i in ib)
        ip = tuple(fp.str_para_posicao(i) for i in ip)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        
        tab1 = fp.cria_tabuleiro_vazio(2)

        for i in ib: fp.coloca_pedra(tab1, i, b)
        for i in ip: fp.coloca_pedra(tab1, i, p)
        
        tab2 = fp.cria_tabuleiro(2, ip, ib)
        assert fp.tabuleiros_iguais(tab1, tab2)
        
    def test_10(self):
        orbits = 2
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        ib = tuple(fp.str_para_posicao(i) for i in ib)
        ip = tuple(fp.str_para_posicao(i) for i in ip)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        
        tab1 = fp.cria_tabuleiro_vazio(2)

        for i in ib: fp.coloca_pedra(tab1, i, b)
        for i in ip: fp.coloca_pedra(tab1, i, p)
        
        _ = fp.roda_tabuleiro(tab1)
        
        tab2 = fp.cria_tabuleiro(2, ip, ib)
        assert not fp.tabuleiros_iguais(tab1, tab2)
        
    def test_11(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        pos = fp.cria_posicao('c',3)
        ref =  (('a3', 'X'), ('b3', 'X'), ('c3', 'X'), ('d3', 'O'))
        assert tuple((fp.posicao_para_str(p), fp.pedra_para_str(v)) for p, v in fp.obtem_linha_horizontal(tab, pos)) == ref

    def test_12(self):
        tab = fp.cria_tabuleiro_vazio(2)
        b, p = fp.cria_pedra_branca(), fp.cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: fp.coloca_pedra(tab, fp.str_para_posicao(i), b)
        for i in ip: fp.coloca_pedra(tab, fp.str_para_posicao(i), p)
        ref = ('b3', 'c3', 'b1', 'a3', 'a4')
        
        assert tuple(fp.posicao_para_str(pos) for pos in fp.obtem_posicoes_pedra(tab, p)) == ref

        
class TestPublicAdditionalFuns:
    def test_1(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        assert (fp.eh_vencedor(t, fp.cria_pedra_preta()), fp.eh_vencedor(t, fp.cria_pedra_branca())) == (False, False)

    def test_2(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        _ = fp.coloca_pedra(t, fp.cria_posicao('d',1), fp.cria_pedra_branca())    
        assert (fp.eh_vencedor(t, fp.cria_pedra_preta()), fp.eh_vencedor(t, fp.cria_pedra_branca())) == (False, True)
    
    def test_3(self):
        assert not fp.eh_fim_jogo(fp.cria_tabuleiro_vazio(2))
        
    def test_4(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        _ = fp.coloca_pedra(t, fp.cria_posicao('d',1), fp.cria_pedra_branca())    
        assert fp.eh_fim_jogo(t)

    def test_5(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'd1\n')
        ref_text = "Escolha uma posicao livre:"
        ref_move =  'd1'
        assert fp.posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
                
    def test_6(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'c1\nc3\nc4\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'c4'
        assert fp.posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
    def test_7(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        move_p = fp.escolhe_movimento_auto(t, fp.cria_pedra_preta(), 'facil')
        move_b = fp.escolhe_movimento_auto(t, fp.cria_pedra_branca(), 'facil')
        assert fp.posicao_para_str(move_p) == 'b2' and \
            fp.posicao_para_str(move_b) == 'b2' 
        
    
    def test_8(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        move = fp.escolhe_movimento_auto(t, fp.cria_pedra_preta(), 'normal')
        assert fp.posicao_para_str(move) == 'd1'
        
    
    def test_9(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.cria_tabuleiro(2, ip, ib)
        move = fp.escolhe_movimento_auto(t, fp.cria_pedra_branca(), 'normal')
        assert fp.posicao_para_str(move) == 'c4'
        
    def test_10(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.roda_tabuleiro(fp.roda_tabuleiro(fp.cria_tabuleiro(2, ip, ib)))
        move = fp.escolhe_movimento_auto(t, fp.cria_pedra_preta(), 'normal')
        assert fp.posicao_para_str(move) == 'd3'
        
    
    def test_11(self):
        ib = tuple(fp.str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(fp.str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = fp.roda_tabuleiro(fp.roda_tabuleiro(fp.cria_tabuleiro(2, ip, ib)))
        move = fp.escolhe_movimento_auto(t, fp.cria_pedra_branca(), 'normal')
        assert fp.posicao_para_str(move) == 'b1'
        
        
    def test_12(self):
        res, text = orbito_offline(2, 'facil', 'O',  JOGADA_PUBLIC_1)
        assert res == -1 and text == OUTPUT_PUBLIC_1

    def test_13(self):
        res, text = orbito_offline(2, 'normal', 'X', JOGADA_PUBLIC_2)
        assert res ==0 and text == OUTPUT_PUBLIC_2

    def test_14(self):
        res, text = orbito_offline(2, '2jogadores', 'X', JOGADA_PUBLIC_3)
        assert res == 1 and text == OUTPUT_PUBLIC_3


### AUXILIAR CODE NECESSARY TO REPLACE STANDARD INPUT 
class ReplaceStdIn:
    def __init__(self, input_handle):
        self.input = input_handle.split('\n')
        self.line = 0

    def readline(self):
        if len(self.input) == self.line:
            return ''
        result = self.input[self.line]
        self.line += 1
        return result

class ReplaceStdOut:
    def __init__(self):
        self.output = ''

    def write(self, s):
        self.output += s
        return len(s)

    def flush(self):
        return 


def escolhe_movimento_manual_offline(tab, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = fp.escolhe_movimento_manual(tab)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout


def orbito_offline(orbits, lvl, jog, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = fp.orbito(orbits, lvl, jog)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout

JOGADA_PUBLIC_1 = 'd1\nc1\nb1\nb4\n'
OUTPUT_PUBLIC_1 = \
"""Bem-vindo ao ORBITO-2.
Jogo contra o computador (facil).
O jogador joga com 'O'.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[O]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[O]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [O]-[O]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [O]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [O]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[ ]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[X]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[X]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[O]-[O]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[X]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[O]-[O]-[O]
VITORIA
"""

JOGADA_PUBLIC_2 = "c2\na3\nb2\na2\na3\na2\nb1\n"
OUTPUT_PUBLIC_2 = \
"""Bem-vindo ao ORBITO-2.
Jogo contra o computador (normal).
O jogador joga com 'X'.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[ ]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[O]-[X]-[ ]
    |   |   |   |
04 [X]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[X]-[ ]
    |   |   |   |
03 [ ]-[O]-[O]-[ ]
    |   |   |   |
04 [ ]-[X]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[O]-[ ]
    |   |   |   |
04 [ ]-[ ]-[X]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[O]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[X]
Turno do jogador.
Escolha uma posicao livre:Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[X]-[ ]
    |   |   |   |
03 [O]-[O]-[X]-[X]
    |   |   |   |
04 [X]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[X]-[X]
    |   |   |   |
03 [O]-[O]-[O]-[ ]
    |   |   |   |
04 [O]-[X]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[X]
    |   |   |   |
02 [ ]-[X]-[O]-[ ]
    |   |   |   |
03 [X]-[X]-[O]-[ ]
    |   |   |   |
04 [O]-[O]-[X]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[X]-[ ]
    |   |   |   |
02 [O]-[O]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [X]-[O]-[O]-[X]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [X]-[X]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[X]-[ ]
    |   |   |   |
03 [O]-[O]-[X]-[X]
    |   |   |   |
04 [ ]-[X]-[O]-[O]
Turno do computador (normal):
    a   b   c   d
01 [X]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[X]-[X]-[X]
    |   |   |   |
03 [O]-[O]-[O]-[O]
    |   |   |   |
04 [O]-[ ]-[X]-[O]
EMPATE
"""

JOGADA_PUBLIC_3 = "a1\nb2\na4\nc4\na4\nb3\nb4\na3\n"
OUTPUT_PUBLIC_3 = \
"""Bem-vindo ao ORBITO-2.
Jogo para dois jogadores.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [X]-[O]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[O]-[ ]
    |   |   |   |
04 [X]-[X]-[ ]-[ ]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[O]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[X]-[X]-[O]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[O]
    |   |   |   |
04 [ ]-[X]-[X]-[X]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[O]
    |   |   |   |
03 [ ]-[O]-[O]-[X]
    |   |   |   |
04 [ ]-[ ]-[X]-[X]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[O]
    |   |   |   |
02 [ ]-[ ]-[O]-[X]
    |   |   |   |
03 [ ]-[ ]-[O]-[X]
    |   |   |   |
04 [ ]-[ ]-[X]-[X]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[O]-[X]
    |   |   |   |
02 [ ]-[O]-[O]-[X]
    |   |   |   |
03 [ ]-[ ]-[ ]-[X]
    |   |   |   |
04 [O]-[ ]-[ ]-[X]
VITORIA DO JOGADOR 'X'
"""

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:
    exec(open(projet_filename, encoding="utf-8").read(), globals())

    # A test function will be run at this point
    yield
    
    # Code that will run after your test, for example:
    
# TAD POSICAO: 49 tests

class TestPrivatePosicaoCria:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao(200, 10)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
        
    def test_2(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('b', (10,))
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
     
    def test_3(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('D', 5)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
        
    def test_4(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('!', 7)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
     
    def test_5(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('ca', 2)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
     
    def test_6(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('d', '1')
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
        
    def test_7(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('b', -45)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)

    def test_8(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('i', 10.0)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)

    def test_9(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('k', 2)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
       
    def test_10(self):
        with pytest.raises(ValueError) as excinfo:
            cria_posicao('f', 11)
        assert "cria_posicao: argumentos invalidos" == str(excinfo.value)
        
         
    def test_11(self):
        p = cria_posicao('g', 8)
        assert p == p 

    def test_12(self):
        p = cria_posicao('j', 10)
        assert p == p 

    def test_13(self):
        p = cria_posicao('e', 9)
        assert hash(p) == hash(p)

class TestPrivatePosicaoColuna:
    def test_1(self):
        p = cria_posicao('c', 4)
        assert obtem_pos_col(p) == 'c'


class TestPrivatePosicaoLinha:
    def test_1(self):
        p = cria_posicao('g', 9)
        assert obtem_pos_lin(p) == 9


class TestPrivatePosicaoEhPosicao:
    def test_1(self):
        assert not eh_posicao(True)

    def test_2(self):
        assert not eh_posicao(27.5)
    
    def test_3(self):
        assert not eh_posicao(('L', 4))

    def test_4(self):
        assert not eh_posicao(('BO', 25))
    
    def test_5(self):
        assert eh_posicao(cria_posicao('h',1))
 


class TestPrivatePosicaoIguais:

    def test_1(self):
        c = cria_posicao('d', 7)
        assert posicoes_iguais(c, c)

    def test_2(self):
        c1 = cria_posicao('f', 7)
        c2 = cria_posicao('f', 8)
        assert not posicoes_iguais(c1, c2)

    def test_3(self):
        c1 = cria_posicao('c', 9)
        c2 = cria_posicao('d', 9)
        assert not posicoes_iguais(c1, c2)
    

class TestPrivatePosicaoToString:
    def test_1(self):
        c = cria_posicao('e', 4)
        assert posicao_para_str(c) == 'e4' 

    def test_2(self):
        c = cria_posicao('g', 10)
        assert posicao_para_str(c) == 'g10'

class TestPrivatePosicaoStringToPosicao:
    def test_1(self):
        c = cria_posicao('a', 4)
        assert posicoes_iguais(str_para_posicao('a4'), c)

    def test_2(self):
        assert eh_posicao(str_para_posicao('b10'))

    def test_3(self):
        assert posicao_para_str(str_para_posicao('h7')) == 'h7'

class TestPrivatePosicaoEhValida:
    def test_1(self):
        assert not eh_posicao_valida(cria_posicao('f', 6), 2) and eh_posicao_valida(cria_posicao('f', 6), 3)

    def test_2(self):
        assert eh_posicao_valida(cria_posicao('j', 10), 5)  and not eh_posicao_valida(cria_posicao('j', 10), 4)

    def test_3(self):
        assert eh_posicao_valida(cria_posicao('h', 8), 4)  and not eh_posicao_valida(cria_posicao('h', 8), 3)
        
    
    
class TestPrivatePosicaoAdjacentes:
    def test_1(self):
        c = cria_posicao('f', 6)
        p_viz = obtem_posicoes_adjacentes(c, 5, True)
        assert isinstance(p_viz, tuple) and all((eh_posicao(a) for a in p_viz))

    def test_2(self):
        c = cria_posicao('f', 6)
        p_viz = obtem_posicoes_adjacentes(c, 5, True)
        ref = 'f5, g5, g6, g7, f7, e7, e6, e5'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref

    def test_3(self):
        c = cria_posicao('a', 1)
        p_viz = obtem_posicoes_adjacentes(c, 3, True)
        ref = 'b1, b2, a2'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref

    def test_4(self):
        c = cria_posicao('a', 5)
        p_viz = obtem_posicoes_adjacentes(c, 3, True)
        ref =  'a4, b4, b5, b6, a6'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_5(self):
        c = cria_posicao('d', 6)
        p_viz = obtem_posicoes_adjacentes(c, 3, True)
        ref =  'd5, e5, e6, c6, c5'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_6(self):
        c = cria_posicao('c', 1)
        p_viz = obtem_posicoes_adjacentes(c, 2, True)
        ref = 'd1, d2, c2, b2, b1'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_7(self):
        c = cria_posicao('h', 8)
        p_viz = obtem_posicoes_adjacentes(c, 4, True)
        ref = 'h7, g8, g7'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_8(self):
        c = cria_posicao('f', 6)
        p_viz = obtem_posicoes_adjacentes(c, 5, False)
        assert isinstance(p_viz, tuple) and all((eh_posicao(a) for a in p_viz))

    def test_9(self):
        c = cria_posicao('f', 6)
        p_viz = obtem_posicoes_adjacentes(c, 5, False)
        ref = 'f5, g6, f7, e6'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref

    def test_10(self):
        c = cria_posicao('a', 1)
        p_viz = obtem_posicoes_adjacentes(c, 3, False)
        ref = 'b1, a2'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref

    def test_11(self):
        c = cria_posicao('a', 5)
        p_viz = obtem_posicoes_adjacentes(c, 3, False)
        ref = 'a4, b5, a6'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_12(self):
        c = cria_posicao('d', 6)
        p_viz = obtem_posicoes_adjacentes(c, 3, False)
        ref = 'd5, e6, c6'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_13(self):
        c = cria_posicao('c', 1)
        p_viz = obtem_posicoes_adjacentes(c, 2, False)
        ref = 'd1, c2, b1'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
        
    def test_14(self):
        c = cria_posicao('h', 8)
        p_viz = obtem_posicoes_adjacentes(c, 4, False)
        ref = 'h7, g8'
        assert ', '.join((posicao_para_str(a) for a in p_viz)) == ref
            
class TestPrivatePosicaoOrdena:
    
    def test_1(self):
        orbits = 2
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = 'b2, c2, b3, c3, a1, b1, c1, d1, a2, d2, a3, d3, a4, b4, c4, d4'
        assert ', '.join((posicao_para_str(a) for a in ordena_posicoes(t, orbits))) == ref

    def test_2(self):
        orbits = 3
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = 'c3, d3, c4, d4, b2, c2, d2, e2, b3, e3, b4, e4, b5, c5, d5, e5, a1, b1, c1, d1, e1, f1, a2, f2, a3, f3, a4, f4, a5, f5, a6, b6, c6, d6, e6, f6'
        assert ', '.join((posicao_para_str(a) for a in ordena_posicoes(t, orbits))) == ref

    def test_3(self):
        orbits = 4
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = 'd4, e4, d5, e5, c3, d3, e3, f3, c4, f4, c5, f5, c6, d6, e6, f6, b2, c2, d2, e2, f2, g2, b3, g3, b4, g4, b5, g5, b6, g6, b7, c7, d7, e7, f7, g7, a1, b1, c1, d1, e1, f1, g1, h1, a2, h2, a3, h3, a4, h4, a5, h5, a6, h6, a7, h7, a8, b8, c8, d8, e8, f8, g8, h8'
        assert ', '.join((posicao_para_str(a) for a in ordena_posicoes(t, orbits))) == ref


    def test_4(self):
        orbits = 5
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = 'e5, f5, e6, f6, d4, e4, f4, g4, d5, g5, d6, g6, d7, e7, f7, g7, c3, d3, e3, f3, g3, h3, c4, h4, c5, h5, c6, h6, c7, h7, c8, d8, e8, f8, g8, h8, b2, c2, d2, e2, f2, g2, h2, i2, b3, i3, b4, i4, b5, i5, b6, i6, b7, i7, b8, i8, b9, c9, d9, e9, f9, g9, h9, i9, a1, b1, c1, d1, e1, f1, g1, h1, i1, j1, a2, j2, a3, j3, a4, j4, a5, j5, a6, j6, a7, j7, a8, j8, a9, j9, a10, b10, c10, d10, e10, f10, g10, h10, i10, j10'
        assert ', '.join((posicao_para_str(a) for a in ordena_posicoes(t, orbits))) == ref


# TAD Pedra - 11 tests

class TestPrivatePedraCria:
    def test_1(self):
        assert (cria_pedra_branca()) != (cria_pedra_preta()) \
            and (cria_pedra_branca()) != (cria_pedra_neutra()) \
                and (cria_pedra_preta()) != (cria_pedra_neutra()) 
        
class TestPrivatePedraEhPedra:
    def test_1(self):
        assert eh_pedra(cria_pedra_branca()) and  eh_pedra(cria_pedra_preta()) and eh_pedra(cria_pedra_neutra())

    def test_2(self):
        assert not eh_pedra(cria_posicao('b',8))
   
   
class TestPrivatePedraEhPedraBranca:
    def test_1(self):
        assert eh_pedra_branca(cria_pedra_branca()) and not eh_pedra_branca(cria_pedra_preta()) and not eh_pedra_branca(cria_pedra_neutra())

   
class TestPrivatePedraEhPedraPreta:
    def test_1(self):
        assert not eh_pedra_preta(cria_pedra_branca()) and eh_pedra_preta(cria_pedra_preta()) and not eh_pedra_preta(cria_pedra_neutra())

class TestPrivatePedraIguais:
    def test_1(self):
        p1 = cria_pedra_branca()
        p2 = cria_pedra_preta()
        assert pedras_iguais(p1, p1) and pedras_iguais(p2, p2)

    def test_2(self):
        p1 = cria_pedra_branca()
        p2 = cria_pedra_preta()
        assert not pedras_iguais(p1, p2) 
        
    def test_3(self):
        p1 = cria_pedra_branca()
        p2 = cria_pedra_preta()
        assert not pedras_iguais(p1, cria_pedra_neutra()) \
            and  not pedras_iguais(p2, cria_pedra_neutra())

class TestPrivatePedraToString:
    def test_1(self):
        b = cria_pedra_branca()
        p = cria_pedra_preta()
        n = cria_pedra_neutra()
        assert (pedra_para_str(b), pedra_para_str(p), pedra_para_str(n)) == ('O', 'X', ' ')

class TestPrivatePedraEhPedraJogador:
    def test_1(self):
        assert eh_pedra_jogador(cria_pedra_branca()) and  eh_pedra_jogador(cria_pedra_preta()) and not eh_pedra_jogador(cria_pedra_neutra())

class TestPrivatePedraToInt:
    def test_1(self):
        b = cria_pedra_branca()
        p = cria_pedra_preta()
        n = cria_pedra_neutra()
        assert (pedra_para_int(b), pedra_para_int(p), pedra_para_int(n)) == (-1, 1, 0)


### TAD Tabuleiro


class TestPrivateTabuleiroCriaVazio:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro_vazio(10)
        assert "cria_tabuleiro_vazio: argumento invalido" == str(excinfo.value)
           
    def test_2(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro_vazio(1)
        assert "cria_tabuleiro_vazio: argumento invalido" == str(excinfo.value)
           
    def test_3(self):
        g2 = cria_tabuleiro_vazio(2)
        g3 = cria_tabuleiro_vazio(3)
        g4 = cria_tabuleiro_vazio(4)
        g5 = cria_tabuleiro_vazio(5)
        assert g2 == g2 and g3 == g3 and g4 == g4 and g5 == g5
        
           
class TestPrivateTabuleiroCria:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(7, (), ())
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
           
    def test_2(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(0, (), ())
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
           
    def test_3(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(2, 19, True)
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
         
    def test_4(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(3, [], {})
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
             
    def test_5(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(4, (), cria_posicao('a', 4))
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
                
    def test_6(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(2, (), (cria_posicao('a', 5),))
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
        
    def test_7(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(5, (), (('z', 4),))
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
        
    def test_8(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(3, (), ('hello', 'world'))
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
                   
    def test_9(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(4, (3.14,2.43), ())
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
        
    def test_10(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(2, (cria_posicao('a',1), cria_posicao('a',1)), ())
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
        
    def test_11(self):
        with pytest.raises(ValueError) as excinfo:
            cria_tabuleiro(3, (cria_posicao('a',1), cria_posicao('a',2)), (cria_posicao('b',1), cria_posicao('a',1)))
        assert "cria_tabuleiro: argumentos invalidos" == str(excinfo.value)
        
    def test_12(self):
        g = cria_tabuleiro(4, (cria_posicao('a',1), cria_posicao('a',2)), (cria_posicao('c',1), cria_posicao('b',1), cria_posicao('b',2)))
        assert g == g
        
    def test_13(self):
        g2 = cria_tabuleiro(2, (), ())
        g3 = cria_tabuleiro(3, (), ())
        g4 = cria_tabuleiro(4, (), ())
        g5 = cria_tabuleiro(5, (), ())
        assert g2 == g2 and g3 == g3 and g4 == g4 and g5 == g5
        
    def test_14(self):
        assert tabuleiros_iguais(cria_tabuleiro_vazio(2), cria_tabuleiro(2, (), ()))
        
    def test_15(self):
        assert tabuleiros_iguais(cria_tabuleiro_vazio(5), cria_tabuleiro(5, (), ()))
        
class TestPrivateTabuleiroCriaCopia:
    def test_1(self):
        c1 = cria_tabuleiro_vazio(5)
        c2 = cria_copia_tabuleiro(c1)
        assert id(c1) != id(c2) and tabuleiros_iguais(c1, c2)

    def test_2(self):
        c1 = cria_tabuleiro(5, (), ())
        c2 = cria_copia_tabuleiro(c1)
        assert id(c1) != id(c2) and tabuleiros_iguais(c1, c2)

    def test_3(self):
        ib = cria_posicao('c',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('e',1), cria_posicao('e',3), cria_posicao('f',4)
        c1 = cria_tabuleiro(5, ip, ib)
        c2 = cria_copia_tabuleiro(c1)
        assert id(c1) != id(c2) and tabuleiros_iguais(c1, c2)


class TestPrivateTabuleiroObtemNumOrbitas:
    def test_1(self):
        assert all(obtem_numero_orbitas(cria_tabuleiro_vazio(n)) == n for n in range(2,6)) 
        
    def test_2(self):
        assert all(obtem_numero_orbitas(cria_tabuleiro(n, (),())) == n for n in range(2,6)) 
       
        

class TestPrivateTabuleiroObtemPedra:
    def test_1(self):
        g = cria_tabuleiro_vazio(5)
        p1 = obtem_pedra(g, cria_posicao('a',1))
        p2 = obtem_pedra(g, cria_posicao('j',10))
        assert pedras_iguais(p1, p2) and pedras_iguais(p1, cria_pedra_neutra())
  
    def test_2(self):
        g = cria_tabuleiro_vazio(2)
        p1 = obtem_pedra(g, cria_posicao('a',1))
        p2 = obtem_pedra(g, cria_posicao('d',4))
        assert pedras_iguais(p1, p2) and pedras_iguais(p1, cria_pedra_neutra())
  

    def test_3(self):
        ib = cria_posicao('c',1), cria_posicao('c',3), cria_posicao('c',4)
        ip = cria_posicao('e',1), cria_posicao('e',3), cria_posicao('e',4)
        g = cria_tabuleiro(3, ip, ib)
 
        assert all(eh_pedra_branca(obtem_pedra(g, i)) for i in ib) and \
            all(eh_pedra_preta(obtem_pedra(g, i)) for i in ip) and \
                all((not eh_pedra_jogador(obtem_pedra(g, cria_posicao(L,N))) for L in 'abf' for N in range(1,7)))

class TestPrivateTabuleiroObtemLinhaVertical:
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pos = cria_posicao('c', 3)
        ref = (('c1', ' '), ('c2', ' '), ('c3', 'O'), ('c4', 'X'))
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_vertical(tab, pos)) == ref
        
    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pos = cria_posicao('h', 4)
        ref = (('h1', 'O'), ('h2', ' '), ('h3', 'O'), ('h4', ' '), ('h5', ' '), ('h6', ' '), ('h7', ' '), ('h8', 'X'))
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_vertical(tab, pos)) == ref
        
    def test_3(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('i', 4)
        ref = (('i1', 'X'), ('i2', 'O'), ('i3', ' '), ('i4', 'X'), ('i5', 'X'), ('i6', 'O'), ('i7', 'X'), ('i8', 'O'), ('i9', ' '), ('i10', 'O'))
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_vertical(tab, pos)) == ref
        
class TestPrivateTabuleiroObtemLinhaHorizontal:
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pos = cria_posicao('c', 3)
        ref = (('a3', ' '), ('b3', 'X'), ('c3', 'O'), ('d3', ' '))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_horizontal(tab, pos)) == ref
        
    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pos = cria_posicao('h', 3)
        ref = (('a3', ' '), ('b3', 'X'), ('c3', 'O'), ('d3', ' '), ('e3', ' '), ('f3', ' '), ('g3', ' '), ('h3', 'O'))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_horizontal(tab, pos)) == ref
        
    def test_3(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('i', 4)
        ref = (('a4', 'X'), ('b4', 'X'), ('c4', 'X'), ('d4', 'X'), ('e4', 'X'), ('f4', 'X'), ('g4', ' '), ('h4', 'X'), ('i4', 'X'), ('j4', ' '))
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_horizontal(tab, pos)) == ref
        
class TestPrivateTabuleiroObtemDiags:
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pos = cria_posicao('c', 3)
        ref = (('a1', 'O'), ('b2', ' '), ('c3', 'O'), ('d4', 'O'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diag) == ref
     
    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pos = cria_posicao('c', 3)
        ref = (('b4', ' '), ('c3', 'O'), ('d2', ' '))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        # print(tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti) == ref  
    
    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pos = cria_posicao('h', 3)
        ref = (('f1', ' '), ('g2', ' '), ('h3', 'O'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diag) == ref
        
    def test_4(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pos = cria_posicao('h', 3)
        ref = (('c8', ' '), ('d7', ' '), ('e6', ' '), ('f5', ' '), ('g4', ' '), ('h3', 'O'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        # print(tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti) == ref
        
    def test_5(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('i', 4)
        ref =(('f1', 'X'), ('g2', ' '), ('h3', ' '), ('i4', 'X'), ('j5', 'X'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diag) == ref
        
        
    def test_6(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('i', 4)
        ref = (('c10', ' '), ('d9', ' '), ('e8', ' '), ('f7', 'O'), ('g6', 'O'), ('h5', ' '), ('i4', 'X'), ('j3', 'X'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti) == ref
        
    def test_7(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('e', 5)
        ref = (('a1', 'O'), ('b2', 'X'), ('c3', 'O'), ('d4', 'X'), ('e5', 'X'), ('f6', 'X'), ('g7', 'X'), ('h8', ' '), ('i9', ' '), ('j10', ' '))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diag) == ref
        
        
    def test_8(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pos = cria_posicao('e', 5)
        ref = (('a9', 'O'), ('b8', 'X'), ('c7', 'O'), ('d6', 'O'), ('e5', 'X'), ('f4', 'X'), ('g3', 'X'), ('h2', ' '), ('i1', 'X'))
        diag, anti = obtem_linhas_diagonais(tab, pos)
        
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti) == ref
        
class TestPrivateTabuleiroObtemPosPedras:
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pedra = cria_pedra_preta()
        ref = ('b3', 'b1', 'c4')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
      
    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pedra = cria_pedra_branca()
        ref = ('c3', 'a1', 'd4')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref  
        
    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pedra = cria_pedra_neutra()
        ref = ('b2', 'c2', 'c1', 'd1', 'a2', 'd2', 'a3', 'd3', 'a4', 'b4')    
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
        
        
    def test_4(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pedra = cria_pedra_preta()
        ref = ('c4', 'b3', 'b1', 'h8')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
        
        
    def test_5(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pedra = cria_pedra_branca()
        ref = ('d4', 'c3', 'a1', 'h1', 'h3')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
        
    def test_6(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        pedra = cria_pedra_neutra()
        ref = ('e4', 'd5', 'e5', 'd3', 'e3', 'f3', 'f4', 'c5', 'f5', 'c6', 'd6', 'e6', 'f6', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'g3', 'b4', 'g4', 'b5', 'g5', 'b6', 'g6', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'c1', 'd1', 'e1', 'f1', 'g1', 'a2', 'h2', 'a3', 'a4', 'h4', 'a5', 'h5', 'a6', 'h6', 'a7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
          
    def test_7(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pedra = cria_pedra_preta()
        ref = ('e5', 'e6', 'f6', 'd4', 'e4', 'f4', 'e7', 'g7', 'f3', 'g3', 'c4', 'h4', 'f8', 'b2', 'd2', 'f2', 'b4', 'i4', 'b5', 'i5', 'b7', 'i7', 'b8', 'f9', 'g9', 'f1', 'g1', 'i1', 'j2', 'j3', 'a4', 'j5', 'j9', 'b10')
        
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
          
    def test_8(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pedra = cria_pedra_branca()
        ref = ('f5', 'd6', 'g6', 'd7', 'f7', 'c3', 'd3', 'c5', 'c7', 'h7', 'g8', 'e2', 'i2', 'i6', 'i8', 'e9', 'h9', 'a1', 'b1', 'c1', 'd1', 'e1', 'h1', 'a3', 'a6', 'a8', 'j8', 'a9', 'a10', 'd10', 'e10', 'f10', 'i10')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
          
    def test_9(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        pedra = cria_pedra_neutra()
        ref = ('g4', 'd5', 'g5', 'e3', 'h3', 'h5', 'c6', 'h6', 'c8', 'd8', 'e8', 'h8', 'c2', 'g2', 'h2', 'b3', 'i3', 'b6', 'b9', 'c9', 'd9', 'i9', 'j1', 'a2', 'j4', 'a5', 'j6', 'a7', 'j7', 'c10', 'g10', 'h10', 'j10')
        assert tuple(posicao_para_str(p) for p in obtem_posicoes_pedra(tab, pedra)) == ref
          
class TestPrivateTabuleiroColocaPedra:
    def test_1(self):
        g1 = cria_tabuleiro_vazio(4)
        g2 = coloca_pedra(g1, cria_posicao('a',1), cria_pedra_branca()) 
        assert eh_pedra_branca(obtem_pedra(g1, cria_posicao('a',1))) and id(g1) == id(g2)

    def test_2(self):
        g = cria_tabuleiro_vazio(2)
        _ = coloca_pedra(g, cria_posicao('a',1), cria_pedra_branca()) 
        _ = coloca_pedra(g, cria_posicao('a',1), cria_pedra_preta()) 
        assert eh_pedra_preta(obtem_pedra(g, cria_posicao('a',1)))
        
    def test_3(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6', 'e6', 'e7', 'e8', 'f8', 'f9'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5', 'f6', 'f7', 'g5', 'g8', 'g9'
        g1 = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        
        g2 = cria_tabuleiro_vazio(5)
        for i in ib: coloca_pedra(g2, str_para_posicao(i), cria_pedra_branca())
        for i in ip: coloca_pedra(g2, str_para_posicao(i), cria_pedra_preta())
        
        assert all(pedras_iguais(obtem_pedra(g1, str_para_posicao(i)),obtem_pedra(g2, str_para_posicao(i))) for i in ib + ip)

class TestPrivateTabuleiroRemovePedra:
    def test_1(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6', 'e6', 'e7', 'e8', 'f8', 'f9'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5', 'f6', 'f7', 'g5', 'g8', 'g9'
        g1 = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        g2 = cria_copia_tabuleiro(g1)
        g3 = remove_pedra(g1, cria_posicao('d',2))
        assert eh_pedra_branca(obtem_pedra(g2, cria_posicao('d',2))) and not eh_pedra_jogador(obtem_pedra(g1, cria_posicao('d',2))) and id(g1) == id(g3)

    def test_2(self):
        g = cria_tabuleiro_vazio(2)
        _ = coloca_pedra(g, cria_posicao('a',1), cria_pedra_preta()) 
        _ = coloca_pedra(g, cria_posicao('a',2), cria_pedra_preta()) 
        _ = remove_pedra(g, cria_posicao('a',1)) 
        assert not eh_pedra_jogador(obtem_pedra(g, cria_posicao('a',1))) and eh_pedra_preta(obtem_pedra(g, cria_posicao('a',2)))
        
    def test_3(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6', 'e6', 'e7', 'e8', 'f8', 'f9'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5', 'f6', 'f7', 'g5', 'g8', 'g9'
        g1 = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        g2 = cria_tabuleiro_vazio(5)
        for i in ib+ip: remove_pedra(g1, str_para_posicao(i))
       
        assert all(pedras_iguais(obtem_pedra(g1, str_para_posicao(i)),obtem_pedra(g2, str_para_posicao(i))) for i in ib + ip)

 

class TestPrivateTabuleiroEhTab:
        
    def test_1(self):
        assert not eh_tabuleiro(False) and not eh_tabuleiro(250)
    
    def test_2(self):
        assert not eh_tabuleiro(()) and  not eh_tabuleiro({}) and not eh_tabuleiro([])
    
    def test_3(self):
        assert eh_tabuleiro(cria_tabuleiro_vazio(3))
    
    def test_4(self):
        assert eh_tabuleiro(cria_copia_tabuleiro(cria_tabuleiro_vazio(5)))

    def test_5(self):
        assert eh_tabuleiro(cria_tabuleiro(4,(),()))
    
    def test_6(self):
        assert eh_tabuleiro(cria_copia_tabuleiro(cria_tabuleiro(2,(),())))

    def test_7(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5'
        g = cria_tabuleiro(3, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert eh_tabuleiro(g)
    
    def test_8(self):
        ib = 'd2', 'd3', 'd4', 'c3', 'c2'
        ip = 'd1', 'b2', 'b3', 'b4', 'a3'
        g = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert eh_tabuleiro(cria_copia_tabuleiro(g))

class TestPrivateTabuleiroTabsIguais:
    def test_1(self):
        c1 = cria_tabuleiro_vazio(2)
        c2 = cria_tabuleiro_vazio(2)
        assert tabuleiros_iguais(c1, c2)

    def test_2(self):
        c1 = cria_tabuleiro_vazio(2)
        c2 = cria_tabuleiro_vazio(3)
        assert not tabuleiros_iguais(c1, c2)

    def test_3(self):
        ip = ('d2',) 
        g1 = cria_tabuleiro(4, tuple(str_para_posicao(i) for i in ip), ())
        g2 = cria_tabuleiro(4, (),())
        assert not tabuleiros_iguais(g1, g2)

    def test_4(self):
        ib = ('d2',) 
        g1 = cria_tabuleiro(4, (), tuple(str_para_posicao(i) for i in ib))
        g2 = cria_tabuleiro(4, (),())
        assert not tabuleiros_iguais(g1, g2)
 
    def test_5(self):
        g1 = cria_tabuleiro_vazio(5)
        g2 = cria_tabuleiro(5, (),())
        assert tabuleiros_iguais(g1, g2)

    def test_6(self):
        ib = 'd2', 'd3', 'd4', 'c3', 'c2'
        ip = 'd1', 'b2', 'b3', 'b4', 'a3'
        g1 = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        g2 = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib[:-1]))
        assert not tabuleiros_iguais(g1, g2)
        
    def test_7(self):
        ib = 'd2', 'd3', 'd4', 'c3', 'c2'
        ip = 'd1', 'b2', 'b3', 'b4', 'a3'
        g1 = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ib), tuple(str_para_posicao(i) for i in ip))
        g2 = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert not tabuleiros_iguais(g1, g2)


class TestPrivateTabuleiroToStr:
    def test_1(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5'
        tab = cria_tabuleiro(3, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f
01 [ ]-[ ]-[ ]-[X]-[ ]-[ ]
    |   |   |   |   |   |
02 [ ]-[ ]-[ ]-[O]-[X]-[ ]
    |   |   |   |   |   |
03 [ ]-[ ]-[ ]-[O]-[X]-[ ]
    |   |   |   |   |   |
04 [ ]-[ ]-[ ]-[O]-[X]-[ ]
    |   |   |   |   |   |
05 [ ]-[ ]-[ ]-[O]-[X]-[ ]
    |   |   |   |   |   |
06 [ ]-[ ]-[ ]-[O]-[ ]-[ ]"""

    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d
01 [O]-[X]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[X]-[O]-[ ]
    |   |   |   |
04 [ ]-[ ]-[X]-[O]"""
        
    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f   g   h
01 [O]-[X]-[ ]-[ ]-[ ]-[ ]-[ ]-[O]
    |   |   |   |   |   |   |   |
02 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
03 [ ]-[X]-[O]-[ ]-[ ]-[ ]-[ ]-[O]
    |   |   |   |   |   |   |   |
04 [ ]-[ ]-[X]-[O]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
05 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
06 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
07 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
08 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[X]"""
      
   
    def test_4(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f   g   h   i   j
01 [O]-[O]-[O]-[O]-[O]-[X]-[X]-[O]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
02 [ ]-[X]-[ ]-[X]-[O]-[X]-[ ]-[ ]-[O]-[X]
    |   |   |   |   |   |   |   |   |   |
03 [O]-[ ]-[O]-[O]-[ ]-[X]-[X]-[ ]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
04 [X]-[X]-[X]-[X]-[X]-[X]-[ ]-[X]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
05 [ ]-[X]-[O]-[ ]-[X]-[O]-[ ]-[ ]-[X]-[X]
    |   |   |   |   |   |   |   |   |   |
06 [O]-[ ]-[ ]-[O]-[X]-[X]-[O]-[ ]-[O]-[ ]
    |   |   |   |   |   |   |   |   |   |
07 [ ]-[X]-[O]-[O]-[X]-[O]-[X]-[O]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
08 [O]-[X]-[ ]-[ ]-[ ]-[X]-[O]-[ ]-[O]-[O]
    |   |   |   |   |   |   |   |   |   |
09 [O]-[ ]-[ ]-[ ]-[O]-[X]-[X]-[O]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
10 [O]-[X]-[ ]-[O]-[O]-[O]-[ ]-[ ]-[O]-[ ]"""
      
class TestPrivateTabuleiroMovePedra:
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab1 = cria_tabuleiro(2, ip, ib)
        tab2 = move_pedra(tab1, cria_posicao('a',1), cria_posicao('a',2)) 
        assert not eh_pedra_jogador(obtem_pedra(tab1, cria_posicao('a',1))) and \
            eh_pedra_branca(obtem_pedra(tab1, cria_posicao('a',2))) and \
                all(pedras_iguais(obtem_pedra(tab1, pos), obtem_pedra(tab2, pos)) for pos in ib[1:] + ip) and \
                    id(tab1) == id(tab2)

    def test_2(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab1 = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab1)
        _ = move_pedra(tab1, cria_posicao('a',1), cria_posicao('a',2)) 
        assert not eh_pedra_jogador(obtem_pedra(tab1, cria_posicao('a',1))) and \
            eh_pedra_branca(obtem_pedra(tab1, cria_posicao('a',2))) and \
                all(pedras_iguais(obtem_pedra(tab1, pos), obtem_pedra(tab2, pos)) for pos in ib[1:] + ip) and \
                    not tabuleiros_iguais(tab1, tab2)

    def test_3(self):
        g = cria_tabuleiro_vazio(2)
        _ = coloca_pedra(g, cria_posicao('a',1), cria_pedra_branca()) 
        _ = coloca_pedra(g, cria_posicao('d',4), cria_pedra_preta()) 
        _ = move_pedra(g, cria_posicao('a',1), cria_posicao('d',4)) 
        assert not eh_pedra_jogador(obtem_pedra(g, cria_posicao('a',1))) and \
            eh_pedra_branca(obtem_pedra(g, cria_posicao('d',4)))
       
    def test_4(self):
        g1 = cria_tabuleiro_vazio(2)
        _ = coloca_pedra(g1, cria_posicao('a',1), cria_pedra_branca()) 
        _ = coloca_pedra(g1, cria_posicao('d',4), cria_pedra_preta()) 
        g2 = cria_copia_tabuleiro(g1)
        _ = move_pedra(g1, cria_posicao('a',1), cria_posicao('d',4)) 
        g3 = cria_copia_tabuleiro(g1)
        _ = move_pedra(g1, cria_posicao('d',4), cria_posicao('a',1)) 
        assert not eh_pedra_jogador(obtem_pedra(g1, cria_posicao('d',4))) and \
            eh_pedra_branca(obtem_pedra(g1, cria_posicao('a',1))) and \
                not tabuleiros_iguais(g1, g2) and not tabuleiros_iguais(g1, g3) \
                    and not tabuleiros_iguais(g2, g3)
         
    def test_5(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6', 'e6', 'e7', 'e8', 'f8', 'f9'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5', 'f6', 'f7', 'g5', 'g8', 'g9'
        g1 = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        
        for o, d in zip(ib, ip): move_pedra(g1, str_para_posicao(o),  str_para_posicao(d))
        
        assert all(not eh_pedra_jogador(obtem_pedra(g1, str_para_posicao(i))) for i in ib) and \
           all(eh_pedra_branca(obtem_pedra(g1, str_para_posicao(i))) for i in ip) 

class TestPrivateTabuleiroPosSeguinte:
    def test_1(self):
        orbits = 2
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('a2', 'a3', 'a4', 'b4', 'a1', 'b3', 'c3', 'c4', 'b1', 'b2', 'c2', 'd4', 'c1', 'd1', 'd2', 'd3')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, False)) for p in t) == ref

    def test_2(self):
        orbits = 2
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('b1', 'a1', 'a2', 'a3', 'c1', 'c2', 'b2', 'a4', 'd1', 'c3', 'b3', 'b4', 'd2', 'd3', 'd4', 'c4')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, True)) for p in t) == ref

    def test_3(self):
        orbits = 3
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('a2', 'a3', 'a4', 'a5', 'a6', 'b6', 'a1', 'b3', 'b4', 'b5', 'c5', 'c6', 'b1', 'b2', 'c4', 'd4', 'd5', 'd6', 'c1', 'c2', 'c3', 'd3', 'e5', 'e6', 'd1', 'd2', 'e2', 'e3', 'e4', 'f6', 'e1', 'f1', 'f2', 'f3', 'f4', 'f5')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, False)) for p in t) == ref

    def test_4(self):
        orbits = 3
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('b1', 'a1', 'a2', 'a3', 'a4', 'a5', 'c1', 'c2', 'b2', 'b3', 'b4', 'a6', 'd1', 'd2', 'd3', 'c3', 'b5', 'b6', 'e1', 'e2', 'd4', 'c4', 'c5', 'c6', 'f1', 'e3', 'e4', 'e5', 'd5', 'd6', 'f2', 'f3', 'f4', 'f5', 'f6', 'e6')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, True)) for p in t) == ref

    def test_5(self):
        orbits = 4
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b8', 'a1', 'b3', 'b4', 'b5', 'b6', 'b7', 'c7', 'c8', 'b1', 'b2', 'c4', 'c5', 'c6', 'd6', 'd7', 'd8', 'c1', 'c2', 'c3', 'd5', 'e5', 'e6', 'e7', 'e8', 'd1', 'd2', 'd3', 'd4', 'e4', 'f6', 'f7', 'f8', 'e1', 'e2', 'e3', 'f3', 'f4', 'f5', 'g7', 'g8', 'f1', 'f2', 'g2', 'g3', 'g4', 'g5', 'g6', 'h8', 'g1', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, False)) for p in t) == ref

    def test_6(self):
        orbits = 4
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('b1', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'c1', 'c2', 'b2', 'b3', 'b4', 'b5', 'b6', 'a8', 'd1', 'd2', 'd3', 'c3', 'c4', 'c5', 'b7', 'b8', 'e1', 'e2', 'e3', 'e4', 'd4', 'c6', 'c7', 'c8', 'f1', 'f2', 'f3', 'e5', 'd5', 'd6', 'd7', 'd8', 'g1', 'g2', 'f4', 'f5', 'f6', 'e6', 'e7', 'e8', 'h1', 'g3', 'g4', 'g5', 'g6', 'g7', 'f7', 'f8', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'g8')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, True)) for p in t) == ref

    def test_7(self):
        orbits = 5
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'b10', 'a1', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'c9', 'c10', 'b1', 'b2', 'c4', 'c5', 'c6', 'c7', 'c8', 'd8', 'd9', 'd10', 'c1', 'c2', 'c3', 'd5', 'd6', 'd7', 'e7', 'e8', 'e9', 'e10', 'd1', 'd2', 'd3', 'd4', 'e6', 'f6', 'f7', 'f8', 'f9', 'f10', 'e1', 'e2', 'e3', 'e4', 'e5', 'f5', 'g7', 'g8', 'g9', 'g10', 'f1', 'f2', 'f3', 'f4', 'g4', 'g5', 'g6', 'h8', 'h9', 'h10', 'g1', 'g2', 'g3', 'h3', 'h4', 'h5', 'h6', 'h7', 'i9', 'i10', 'h1', 'h2', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'j10', 'i1', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, False)) for p in t) == ref

    def test_8(self):
        orbits = 5
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('b1', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'c1', 'c2', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'a10', 'd1', 'd2', 'd3', 'c3', 'c4', 'c5', 'c6', 'c7', 'b9', 'b10', 'e1', 'e2', 'e3', 'e4', 'd4', 'd5', 'd6', 'c8', 'c9', 'c10', 'f1', 'f2', 'f3', 'f4', 'f5', 'e5', 'd7', 'd8', 'd9', 'd10', 'g1', 'g2', 'g3', 'g4', 'f6', 'e6', 'e7', 'e8', 'e9', 'e10', 'h1', 'h2', 'h3', 'g5', 'g6', 'g7', 'f7', 'f8', 'f9', 'f10', 'i1', 'i2', 'h4', 'h5', 'h6', 'h7', 'h8', 'g8', 'g9', 'g10', 'j1', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'h9', 'h10', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'j10', 'i10')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, True)) for p in t) == ref


class TestPrivateTabuleiroRoda:
    
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        _ = roda_tabuleiro(tab)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d
01 [X]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[ ]-[O]-[ ]
    |   |   |   |
03 [ ]-[ ]-[X]-[O]
    |   |   |   |
04 [ ]-[ ]-[ ]-[X]"""
        
    def test_2(self):
        ib = 'd2', 'd3', 'd4', 'd5', 'd6'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5'
        tab = cria_tabuleiro(3, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        _ = roda_tabuleiro(tab)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f
01 [ ]-[ ]-[X]-[ ]-[ ]-[ ]
    |   |   |   |   |   |
02 [ ]-[ ]-[O]-[X]-[X]-[ ]
    |   |   |   |   |   |
03 [ ]-[ ]-[O]-[O]-[X]-[ ]
    |   |   |   |   |   |
04 [ ]-[ ]-[ ]-[ ]-[X]-[ ]
    |   |   |   |   |   |
05 [ ]-[ ]-[ ]-[ ]-[O]-[ ]
    |   |   |   |   |   |
06 [ ]-[ ]-[ ]-[ ]-[O]-[ ]"""


    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        _ = roda_tabuleiro(tab)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f   g   h
01 [X]-[ ]-[ ]-[ ]-[ ]-[ ]-[O]-[ ]
    |   |   |   |   |   |   |   |
02 [O]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[O]
    |   |   |   |   |   |   |   |
03 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
04 [ ]-[X]-[O]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
05 [ ]-[ ]-[X]-[O]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
06 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]
    |   |   |   |   |   |   |   |
07 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[X]
    |   |   |   |   |   |   |   |
08 [ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]-[ ]"""
       
    def test_4(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        _ = roda_tabuleiro(tab)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f   g   h   i   j
01 [O]-[O]-[O]-[O]-[X]-[X]-[O]-[X]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
02 [O]-[ ]-[X]-[O]-[X]-[ ]-[ ]-[O]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
03 [ ]-[X]-[O]-[ ]-[X]-[X]-[ ]-[X]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
04 [O]-[ ]-[O]-[X]-[X]-[ ]-[ ]-[ ]-[X]-[X]
    |   |   |   |   |   |   |   |   |   |
05 [X]-[X]-[X]-[X]-[O]-[X]-[O]-[ ]-[O]-[ ]
    |   |   |   |   |   |   |   |   |   |
06 [ ]-[X]-[O]-[ ]-[X]-[X]-[X]-[O]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
07 [O]-[ ]-[ ]-[O]-[O]-[X]-[O]-[ ]-[O]-[O]
    |   |   |   |   |   |   |   |   |   |
08 [ ]-[X]-[O]-[ ]-[ ]-[ ]-[X]-[O]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
09 [O]-[X]-[ ]-[ ]-[ ]-[O]-[X]-[X]-[O]-[ ]
    |   |   |   |   |   |   |   |   |   |
10 [O]-[O]-[X]-[ ]-[O]-[O]-[O]-[ ]-[ ]-[O]"""
      
 
    def test_5(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        _ = roda_tabuleiro(roda_tabuleiro(roda_tabuleiro(roda_tabuleiro(roda_tabuleiro(tab)))))
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d   e   f   g   h   i   j
01 [X]-[X]-[O]-[X]-[ ]-[X]-[X]-[ ]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
02 [O]-[ ]-[ ]-[O]-[ ]-[X]-[X]-[O]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
03 [O]-[X]-[ ]-[X]-[ ]-[ ]-[O]-[ ]-[O]-[O]
    |   |   |   |   |   |   |   |   |   |
04 [O]-[O]-[X]-[O]-[X]-[O]-[X]-[O]-[ ]-[X]
    |   |   |   |   |   |   |   |   |   |
05 [O]-[X]-[X]-[ ]-[O]-[X]-[O]-[X]-[O]-[ ]
    |   |   |   |   |   |   |   |   |   |
06 [O]-[ ]-[ ]-[ ]-[X]-[X]-[O]-[ ]-[X]-[O]
    |   |   |   |   |   |   |   |   |   |
07 [ ]-[X]-[O]-[X]-[X]-[X]-[ ]-[ ]-[X]-[ ]
    |   |   |   |   |   |   |   |   |   |
08 [O]-[ ]-[O]-[X]-[O]-[ ]-[O]-[ ]-[O]-[ ]
    |   |   |   |   |   |   |   |   |   |
09 [X]-[X]-[X]-[ ]-[X]-[X]-[ ]-[ ]-[ ]-[O]
    |   |   |   |   |   |   |   |   |   |
10 [ ]-[O]-[ ]-[O]-[O]-[O]-[X]-[ ]-[O]-[O]"""
      

class TestPrivateTabuleiroVerificaLinha:
    def test_1(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        # print(tabuleiro_para_str(tab))
        pos = 'a1', 'b2', 'c3', 'd4'
        assert all(verifica_linha_pedras(tab, str_para_posicao(p), cria_pedra_preta(), 4) for p in pos)  

    def test_2(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        k_seq = 1, 2, 3, 4, 5
        res = True, True, False, False, False
        assert tuple(verifica_linha_pedras(tab, str_para_posicao('d2'), cria_pedra_preta(), k) for k in k_seq) == res  

    def test_3(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        k_seq = 1, 2, 3, 4, 5
        res = True, True, False, False, False
        assert tuple(verifica_linha_pedras(tab, str_para_posicao('a2'), cria_pedra_branca(), k) for k in k_seq) == res  

    def test_4(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        k_seq = 1, 2, 3, 4, 5, 6, 7
        res = False, False, False, False, False, False, False
        assert tuple(verifica_linha_pedras(tab, str_para_posicao('b2'), cria_pedra_branca(), k) for k in k_seq) == res and \
            tuple(verifica_linha_pedras(tab, str_para_posicao('a3'), cria_pedra_preta(), k) for k in k_seq) == res and \
                tuple(verifica_linha_pedras(tab, str_para_posicao('c2'), cria_pedra_branca(), k) for k in k_seq) == res  

    def test_5(self):
        ip = 'd3', 'c4', 
        ib = 'a1', 'b1', 'c1', 'a2', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        
        assert verifica_linha_pedras(tab, str_para_posicao('c1'), cria_pedra_branca(), 3) and \
            not verifica_linha_pedras(tab, str_para_posicao('d1'), cria_pedra_branca(), 3)
    
    def test_6(self):
        ip = 'd3', 'c4', 'b5', 'a6'
        ib = 'a1', 'b1', 'c1', 'a2' 
        tab = cria_tabuleiro(3, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        k_seq = 1, 2, 3, 4
        assert all(verifica_linha_pedras(tab, str_para_posicao('b5'), cria_pedra_preta(), k) for k in k_seq) 

    def test_7(self):
        ip = 'd5', 'd6', 'd7', 'd9', 'd10'
        ib = 'd8', 'a3' 
        tab = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert (not verifica_linha_pedras(tab, str_para_posicao('d10'), cria_pedra_preta(), 3)) and \
            verifica_linha_pedras(tab, str_para_posicao('d9'), cria_pedra_preta(), 2) and \
                 verifica_linha_pedras(tab, str_para_posicao('d7'), cria_pedra_preta(), 3) and \
                    verifica_linha_pedras(tab, str_para_posicao('d7'), cria_pedra_preta(), 2) 

    def test_8(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        # print(tabuleiro_para_str(tab))
        assert verifica_linha_pedras(tab, cria_posicao('d', 1), cria_pedra_branca(), 5)  and \
            verifica_linha_pedras(tab, cria_posicao('e', 4), cria_pedra_preta(), 6) and \
                verifica_linha_pedras(tab, cria_posicao('f', 3), cria_pedra_preta(), 4) and \
                  verifica_linha_pedras(tab, cria_posicao('f', 3), cria_pedra_preta(), 4) and \
                   verifica_linha_pedras(tab, cria_posicao('g', 7), cria_pedra_preta(), 4)   and \
                   verifica_linha_pedras(tab, cria_posicao('i', 6), cria_pedra_branca(), 3) 
        
    def test_9(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        # print(tabuleiro_para_str(tab))
        assert not verifica_linha_pedras(tab, cria_posicao('d', 1), cria_pedra_branca(), 6)  and \
            not verifica_linha_pedras(tab, cria_posicao('e', 4), cria_pedra_preta(), 7)  and \
                not verifica_linha_pedras(tab, cria_posicao('f', 3), cria_pedra_preta(), 5) and \
                  not verifica_linha_pedras(tab, cria_posicao('f', 3), cria_pedra_preta(), 5) and \
                   not verifica_linha_pedras(tab, cria_posicao('g', 7), cria_pedra_preta(), 5)   and \
                     not verifica_linha_pedras(tab, cria_posicao('i', 6), cria_pedra_branca(), 4)
    
    

class TestPrivateEhVencedor:
    def test_1(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert eh_vencedor(tab, cria_pedra_preta()) and not eh_vencedor(tab, cria_pedra_branca())

    def test_2(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert not eh_vencedor(tab, cria_pedra_preta()) and not eh_vencedor(tab, cria_pedra_branca())

    def test_3(self):
        orbits = 3
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        ip = tuple(cria_posicao(l, 3) for l in LETTERS[:-1])
        ib = tuple(cria_posicao(l, 4) for l in LETTERS)
        tab = cria_tabuleiro(orbits, ip, ib)
        assert not eh_vencedor(tab, cria_pedra_preta()) and eh_vencedor(tab, cria_pedra_branca())

    def test_4(self):
        orbits = 4
        NUMBERS = tuple(range(1,2*orbits + 1))
        ip = tuple(cria_posicao('f', l) for l in NUMBERS)
        ib = tuple(cria_posicao('g', l) for l in NUMBERS[:-1])
        tab = cria_tabuleiro(orbits, ip, ib)
        assert eh_vencedor(tab, cria_pedra_preta()) and not eh_vencedor(tab, cria_pedra_branca())

    def test_5(self):
        orbits = 4
        ib = tuple(str_para_posicao(s) for s in ('a8', 'b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'))
        ip = tuple(str_para_posicao(s) for s in ('a7', 'b6', 'c5', 'd4', 'e3', 'f2', 'g1', 'g4'))
        tab = cria_tabuleiro(orbits, ip, ib)
        # print(tabuleiro_para_str(tab))
        assert not eh_vencedor(tab, cria_pedra_preta()) and eh_vencedor(tab, cria_pedra_branca())
    
    def test_6(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        assert not eh_vencedor(tab, cria_pedra_preta()) and not eh_vencedor(tab, cria_pedra_branca())
    
class TestPrivateEhFimJogo:
    def test_1(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 'd4'
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert eh_fim_jogo(tab)

    def test_2(self):
        ip = 'a1', 'd1', 'b2', 'd2', 'c3', 'a4', 
        ib = 'a2', 'a3', 'd3', 
        tab = cria_tabuleiro(2, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        assert not eh_fim_jogo(tab)

    def test_3(self):
        orbits = 3
        NUMBERS = tuple(range(1,2*orbits + 1))
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        ip = tuple(cria_posicao(l, n) for l in LETTERS for n in NUMBERS[::2])
        ib = tuple(cria_posicao(l, n) for l in LETTERS for n in NUMBERS[1::2])
        tab = cria_tabuleiro(orbits, ip, ib)
        assert eh_fim_jogo(tab)

    def test_4(self):
        orbits = 4
        ib = tuple(str_para_posicao(s) for s in ('a8', 'b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'))
        ip = tuple(str_para_posicao(s) for s in ('a7', 'b6', 'c5', 'd4', 'e3', 'f2', 'g1', 'g4'))
        tab = cria_tabuleiro(orbits, ip, ib)
        # print(tabuleiro_para_str(tab))
        assert eh_fim_jogo(tab)
    
    def test_5(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        assert not eh_fim_jogo(tab)

    def test_6(self):
        orbits = 3
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        ip = tuple(cria_posicao(l, 3) for l in LETTERS[:-1])
        ib = tuple(cria_posicao(l, 4) for l in LETTERS)
        tab = cria_tabuleiro(orbits, ip, ib)
        assert eh_fim_jogo(tab)

    def test_7(self):
        orbits = 4
        NUMBERS = tuple(range(1,2*orbits + 1))
        ip = tuple(cria_posicao('d', l) for l in NUMBERS)
        ib = tuple(cria_posicao('h', l) for l in NUMBERS[:-1])
        tab = cria_tabuleiro(orbits, ip, ib)
        assert  eh_fim_jogo(tab)
   
    def test_8(self):
        orbits = 5
        NUMBERS = tuple(range(1,2*orbits + 1))
        ip = tuple(cria_posicao('d', l) for l in NUMBERS[:-1]) + \
            tuple(cria_posicao('a', l) for l in NUMBERS[:-1])
        ib = tuple(cria_posicao('h', l) for l in NUMBERS[:-1]) + \
            tuple(cria_posicao('e', l) for l in NUMBERS[:-1])
        tab = cria_tabuleiro(orbits, ip, ib)
        assert  not eh_fim_jogo(tab)
    
    def test_9(self):
        assert  not eh_fim_jogo(cria_tabuleiro_vazio(2)) and \
            not eh_fim_jogo(cria_tabuleiro_vazio(3)) and \
                not eh_fim_jogo(cria_tabuleiro_vazio(4)) and \
                    not eh_fim_jogo(cria_tabuleiro_vazio(5))
        
class TestPrivateMovimentoManual:
    def test_1(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, ' \nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
    def test_2(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'ola\nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
    def test_3(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'D1\nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
    
    def test_4(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'dd1\nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
            
    def test_5(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'd123\nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
    
    def test_6(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'd5\nd1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
    
    def test_7(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'e4\na1\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'a1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text            
            
    def test_8(self):
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(5, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'j10\n')
        ref_text = "Escolha uma posicao livre:"
        ref_move =  'j10'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text            
            
                                              
class TestPrivateMovimentoAutoFacil:   
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('b2', 'b2') and \
                    tabuleiros_iguais(tab, tab2)
        
    def test_2(self):
        ib = tuple(str_para_posicao(s) for s in ('e5', 'd6'))
        ip = tuple(str_para_posicao(s) for s in ('a1', 'a2'))
        tab = cria_tabuleiro(3, ip, ib)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('c4', 'b2')   

    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',2), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('b',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('d3', 'c3')
   
    def test_4(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('g4', 'g4')
 
    def test_5(self):
        ib = (cria_posicao('a',1),)
        ip = (cria_posicao('d',4),)
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('b2', 'b3') and \
                    tabuleiros_iguais(tab, tab2)
      
    def test_6(self):
        ib = (cria_posicao('b',2),cria_posicao('c',2),cria_posicao('b',3),cria_posicao('c',3))
        ip = ()
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('a1', 'a1') and \
                    tabuleiros_iguais(tab, tab2)  

    def test_7(self):
        ib = (cria_posicao('b',3),cria_posicao('c',3))
        ip = (cria_posicao('b',2),cria_posicao('c',2))
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('c1', 'a1') and \
                    tabuleiros_iguais(tab, tab2)  


    def test_8(self):
        ib = (('e', 5), ('g', 5), ('d', 7), ('e', 7), ('g', 7), ('c', 3), ('c', 4), ('c', 6), ('h', 6), ('c', 8), ('h', 8), ('d', 2), ('h', 2), ('i', 5), ('i', 7), ('f', 9), ('i', 9), ('a', 1), ('b', 1), ('c', 1), ('d', 1), ('g', 1), ('a', 2), ('a', 4), ('a', 7), ('j', 7), ('a', 9), ('a', 10), ('b', 10), ('e', 10), ('f', 10), ('g', 10), ('j', 10))
        ip = (('f', 5), ('e', 6), ('f', 6), ('d', 4), ('e', 4), ('d', 5), ('g', 6), ('f', 7), ('e', 3), ('f', 3), ('h', 3), ('c', 5), ('g', 8), ('c', 2), ('e', 2), ('b', 3), ('i', 3), ('i', 4), ('b', 5), ('b', 6), ('i', 6), ('b', 8), ('b', 9), ('g', 9), ('h', 9), ('e', 1), ('f', 1), ('h', 1), ('j', 1), ('j', 2), ('j', 4), ('a', 5), ('j', 8), ('c', 10))
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('g4', 'f4')

    def test_9(self):
        ib = (('e', 5), ('d', 4), ('f', 4), ('g', 5), ('g', 6), ('g', 3), ('h', 4), ('c', 7), ('c', 8), ('e', 8), ('g', 8), ('d', 2), ('h', 2), ('i', 3), ('b', 4), ('i', 5), ('i', 8), ('c', 1), ('a', 2), ('a', 3), ('j', 3), ('a', 4), ('a', 5), ('a', 6), ('j', 6), ('a', 8), ('j', 9), ('b', 10), ('d', 10), ('e', 10), ('f', 10), ('i', 10), ('j', 10))
        ip = (('f', 5), ('e', 6), ('f', 6), ('e', 4), ('g', 4), ('d', 7), ('e', 7), ('f', 7), ('d', 3), ('c', 4), ('c', 5), ('h', 5), ('d', 8), ('f', 2), ('g', 2), ('i', 2), ('b', 3), ('b', 5), ('i', 6), ('b', 7), ('i', 7), ('b', 9), ('c', 9), ('e', 9), ('f', 9), ('a', 1), ('b', 1), ('d', 1), ('f', 1), ('g', 1), ('i', 1), ('j', 4), ('a', 9), ('g', 10))
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'facil')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'facil'))) == ('d5', 'd5') 

class TestPrivateMovimentoAutoNormal: 
    def test_1(self):
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('c2', 'c2') and \
                    tabuleiros_iguais(tab, tab2)
        
    def test_2(self):
        ib = tuple(str_para_posicao(s) for s in ('e5', 'd6'))
        ip = tuple(str_para_posicao(s) for s in ('a1', 'a2'))
        tab = cria_tabuleiro(3, ip, ib)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('d5', 'b1')   

    def test_3(self):
        ib = cria_posicao('a',1), cria_posicao('c',2), cria_posicao('h',1), cria_posicao('h',3)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('b',4), cria_posicao('h',8)
        tab = cria_tabuleiro(4, ip, ib)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('d2', 'b2')
   
    def test_4(self):
        ib = [('g', 8), ('d', 10), ('e', 2), ('e', 1), ('f', 5), ('d', 6), ('h', 7), ('i', 2), ('a', 1), ('f', 7), ('e', 9), ('a', 8), ('d', 3), ('c', 3), ('c', 7), ('a', 9), ('h', 9), ('i', 8), ('a', 10), ('a', 6), ('h', 1), ('b', 1), ('g', 6), ('a', 3), ('c', 1), ('e', 10), ('i', 6), ('i', 10), ('d', 1), ('c', 5), ('j', 8), ('d', 7), ('f', 10)]
        ip = [('g', 7), ('d', 2), ('f', 2), ('i', 7), ('b', 10), ('f', 1), ('c', 4), ('g', 9), ('b', 4), ('d', 4), ('e', 6), ('b', 5), ('f', 9), ('b', 2), ('j', 5), ('f', 8), ('f', 3), ('g', 3), ('i', 4), ('e', 5), ('i', 1), ('e', 7), ('b', 8), ('a', 4), ('b', 7), ('h', 4), ('i', 5), ('j', 2), ('j', 9), ('f', 6), ('g', 1), ('e', 4), ('j', 3), ('f', 4)]
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        # print(tabuleiro_para_str(tab))
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('e3', 'h10')
 
    def test_5(self):
        ib = (cria_posicao('a',1),)
        ip = (cria_posicao('d',4),cria_posicao('c',3))
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('b3', 'c1') and \
                    tabuleiros_iguais(tab, tab2)
      
    def test_6(self):
        ib = (cria_posicao('b',3),cria_posicao('c',3))
        ip = (cria_posicao('b',2),cria_posicao('c',2))
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('d1', 'c1') and \
                    tabuleiros_iguais(tab, tab2)  
    def test_7(self):
        ib = cria_posicao('b',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('a',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        tab2 = cria_copia_tabuleiro(tab)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('c1', 'c2') and \
                    tabuleiros_iguais(tab, tab2)

    def test_8(self):
        ib = (('e', 5), ('g', 5), ('d', 7), ('e', 7), ('g', 7), ('c', 3), ('c', 4), ('c', 6), ('h', 6), ('c', 8), ('h', 8), ('d', 2), ('h', 2), ('i', 5), ('i', 7), ('f', 9), ('i', 9), ('a', 1), ('b', 1), ('c', 1), ('d', 1), ('g', 1), ('a', 2), ('a', 4), ('a', 7), ('j', 7), ('a', 9), ('a', 10), ('b', 10), ('e', 10), ('f', 10), ('g', 10), ('j', 10))
        ip = (('f', 5), ('e', 6), ('f', 6), ('d', 4), ('e', 4), ('d', 5), ('g', 6), ('f', 7), ('e', 3), ('f', 3), ('h', 3), ('c', 5), ('g', 8), ('c', 2), ('e', 2), ('b', 3), ('i', 3), ('i', 4), ('b', 5), ('b', 6), ('i', 6), ('b', 8), ('b', 9), ('g', 9), ('h', 9), ('e', 1), ('f', 1), ('h', 1), ('j', 1), ('j', 2), ('j', 4), ('a', 5), ('j', 8), ('c', 10))
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('g4', 'd3')
        
    def test_9(self):
        ib = (('e', 5), ('d', 4), ('f', 4), ('g', 5), ('g', 6), ('g', 3), ('h', 4), ('c', 7), ('c', 8), ('e', 8), ('g', 8), ('d', 2), ('h', 2), ('i', 3), ('b', 4), ('i', 5), ('i', 8), ('c', 1), ('a', 2), ('a', 3), ('j', 3), ('a', 4), ('a', 5), ('a', 6), ('j', 6), ('a', 8), ('j', 9), ('b', 10), ('d', 10), ('e', 10), ('f', 10), ('i', 10), ('j', 10))
        ip = (('f', 5), ('e', 6), ('f', 6), ('e', 4), ('g', 4), ('d', 7), ('e', 7), ('f', 7), ('d', 3), ('c', 4), ('c', 5), ('h', 5), ('d', 8), ('f', 2), ('g', 2), ('i', 2), ('b', 3), ('b', 5), ('i', 6), ('b', 7), ('i', 7), ('b', 9), ('c', 9), ('e', 9), ('f', 9), ('a', 1), ('b', 1), ('d', 1), ('f', 1), ('g', 1), ('i', 1), ('j', 4), ('a', 9), ('g', 10))
        tab = cria_tabuleiro(5, tuple(cria_posicao(*p) for p in ip), tuple(cria_posicao(*p) for p in ib))
        b, p = cria_pedra_branca(), cria_pedra_preta()
        assert (posicao_para_str(escolhe_movimento_auto(tab, b, 'normal')), 
                posicao_para_str(escolhe_movimento_auto(tab, p, 'normal'))) == ('a7', 'c2') 
            
class TestPrivateOrbito:
    def test_1(self):
        JOGADA_PRIVATE_1 = 'd2\nb1\ne2\na3\na4\nd6\nf5\nd2\ne1\nb1\n'
        OUTPUT_PRIVATE_1 = open(f'{SAMPLE_DIR}/sample1.txt').read()

        res, text = orbito_offline(3, 'facil', 'X',  JOGADA_PRIVATE_1)
        assert res == 1 and text == OUTPUT_PRIVATE_1
        
    def test_2(self):
        JOGADA_PRIVATE_2 = 'b2\nb2\nd4\na2\nd2\n'
        OUTPUT_PRIVATE_2 = open(f'{SAMPLE_DIR}/sample2.txt').read()

        res, text = orbito_offline(2, 'normal', 'O',  JOGADA_PRIVATE_2)
        assert res == 1 and text == OUTPUT_PRIVATE_2

    def test_3(self):
        JOGADA_PRIVATE_3 = 'e5\nola\nadeus\nd4\nc1\nb1\nb1\n'
        OUTPUT_PRIVATE_3 = open(f'{SAMPLE_DIR}/sample3.txt').read()

        res, text = orbito_offline(2, 'facil', 'O',  JOGADA_PRIVATE_3)
        assert res == -1 and text == OUTPUT_PRIVATE_3

    def test_4(self):
        JOGADA_PRIVATE_4 = 'b2\nc2\nd4\nd4\nd1\na2\n'
        OUTPUT_PRIVATE_4 = open(f'{SAMPLE_DIR}/sample4.txt').read()

        res, text = orbito_offline(2, 'normal', 'X',  JOGADA_PRIVATE_4)
        assert res == 0 and text == OUTPUT_PRIVATE_4

    def test_5(self):
        JOGADA_PRIVATE_5 = 'b2\na1\nb2\na2\nc2\nc4\nd3\na3\nc4\nb1\nc2\nc4\nb4\n'
        OUTPUT_PRIVATE_5 = open(f'{SAMPLE_DIR}/sample5.txt').read()

        res, text = orbito_offline(2, '2jogadores', 'X',  JOGADA_PRIVATE_5)
        assert res == 1 and text == OUTPUT_PRIVATE_5

class TestPrivateOrbitoExcept:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            orbito('ola', 'facil', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
    def test_2(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(1, 'facil', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_3(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(6, 'facil', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
        
    def test_4(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'facile', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_5(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'a', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_6(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 4, 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
    def test_7(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'NORMAL', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_8(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'normal', '')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_9(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'normal', ['X'])
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        

    def test_10(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(2, 'normal', 1)
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
    def test_11(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(4, 'normal', 'x')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
    def test_12(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(4, 'norm', 'X')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
    def test_13(self):
        with pytest.raises(ValueError) as excinfo:
            orbito(4, 'normal', 'XO')
        assert "orbito: argumentos invalidos" == str(excinfo.value)
        
##################################
####  START ABSTRACTION TESTS ####
##################################            

class TestPrivateTADPosicao:
    
    # score = 0.5
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_posicao.py', encoding="utf-8").read(), globals())
        assert not eh_posicao_valida(cria_posicao('f', 6), 2) and eh_posicao_valida(cria_posicao('f', 6), 3)

    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_posicao.py', encoding="utf-8").read(), globals())
        
        i1 = cria_posicao('a', 2)
        assert ('a1', 'b2', 'a3') == tuple(posicao_para_str(i) for i in obtem_posicoes_adjacentes(i1, 2, False))
        
    def test_3(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_posicao.py', encoding="utf-8").read(), globals())
        
        i1 = cria_posicao('a', 2)
        assert ('a1', 'b1', 'b2', 'b3', 'a3') == tuple(posicao_para_str(i) for i in obtem_posicoes_adjacentes(i1, 2, True))    
        
    def test_4(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_posicao.py', encoding="utf-8").read(), globals())
        tup = (cria_posicao('a',1), cria_posicao('a',3), cria_posicao('b',1), cria_posicao('b',2))
        assert ('b2', 'a1', 'b1', 'a3') == tuple(posicao_para_str(i) for i in ordena_posicoes(tup, 2))
    
class TestPrivateTADPedra:
    # score 0.25
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_pedra.py', encoding="utf-8").read(), globals())
        assert eh_pedra_jogador(cria_pedra_branca()) and  eh_pedra_jogador(cria_pedra_preta()) and not eh_pedra_jogador(cria_pedra_neutra())
       
    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TAD_pedra.py', encoding="utf-8").read(), globals())    
        b = cria_pedra_branca()
        p = cria_pedra_preta()
        n = cria_pedra_neutra()
        assert (pedra_para_int(b), pedra_para_int(p), pedra_para_int(n)) == (-1, 1, 0)

 
        
class TestPrivateTADTabuleiro:
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        print(cria_tabuleiro_vazio(2))
        assert eh_tabuleiro(cria_tabuleiro_vazio(2))
        
    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        tab = cria_tabuleiro_vazio(2)
        pos = cria_posicao('c',2)
        assert pedra_para_str(obtem_pedra(tab, pos)) == ' '
        
    def test_3(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        hyp = \
"""    a   b   c   d
01 [ ]-[X]-[O]-[ ]
    |   |   |   |
02 [ ]-[ ]-[O]-[O]
    |   |   |   |
03 [X]-[X]-[X]-[O]
    |   |   |   |
04 [X]-[ ]-[ ]-[O]"""

        assert tabuleiro_para_str(tab) == hyp
      
    def test_4(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        pos = cria_posicao('c',3)
        ref =  (('c1', 'O'), ('c2', 'O'), ('c3', 'X'), ('c4', ' '))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_vertical(tab, pos)) == ref

    def test_5(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab = cria_tabuleiro(2, ip, ib)
        pos = cria_posicao('c', 3)
        ref = (('a3', ' '), ('b3', 'X'), ('c3', 'O'), ('d3', ' '))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in obtem_linha_horizontal(tab, pos)) == ref
        
        
    def test_6(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        diag, anti = obtem_linhas_diagonais(tab, cria_posicao('c',3))
        ref_d = (('a1', ' '), ('b2', ' '), ('c3', 'X'), ('d4', 'O'))
        ref_a = (('b4', ' '), ('c3', 'X'), ('d2', 'O'))
        assert tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diag) == ref_d and \
            tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti) == ref_a

    def test_7(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        ref = ('b3', 'c3', 'b1', 'a3', 'a4')
        
        assert tuple(posicao_para_str(pos) for pos in obtem_posicoes_pedra(tab, p)) == ref

    def test_8(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        
        ib = 'd2', 'd3', 'd4', 'd5', 'd6', 'e6', 'e7', 'e8', 'f8', 'f9'
        ip = 'd1', 'e2', 'e3', 'e4', 'e5', 'f6', 'f7', 'g5', 'g8', 'g9'
        g1 = cria_tabuleiro(5, tuple(str_para_posicao(i) for i in ip), tuple(str_para_posicao(i) for i in ib))
        g2 = cria_copia_tabuleiro(g1)
        g3 = remove_pedra(g1, cria_posicao('d',2))
        assert eh_pedra_branca(obtem_pedra(g2, cria_posicao('d',2))) and not eh_pedra_jogador(obtem_pedra(g1, cria_posicao('d',2))) and id(g1) == id(g3)
 
    def test_9(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
       
        orbits = 2
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        ib = tuple(str_para_posicao(i) for i in ib)
        ip = tuple(str_para_posicao(i) for i in ip)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        
        tab1 = cria_tabuleiro_vazio(2)

        for i in ib: coloca_pedra(tab1, i, b)
        for i in ip: coloca_pedra(tab1, i, p)
        
        tab2 = cria_tabuleiro(2, ip, ib)
        assert tabuleiros_iguais(tab1, tab2)
        

class TestPrivateTADTabuleiroFAN:

    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TAD_tabuleiro.py', encoding="utf-8").read(), globals())
       
        ib = cria_posicao('a',1), cria_posicao('c',3), cria_posicao('d',4)
        ip = cria_posicao('b',1), cria_posicao('b',3), cria_posicao('c',4)
        tab1 = cria_tabuleiro(2, ip, ib)
        tab2 = move_pedra(tab1, cria_posicao('a',1), cria_posicao('a',2)) 
        assert not eh_pedra_jogador(obtem_pedra(tab1, cria_posicao('a',1))) and \
            eh_pedra_branca(obtem_pedra(tab1, cria_posicao('a',2))) and \
                all(pedras_iguais(obtem_pedra(tab1, pos), obtem_pedra(tab2, pos)) for pos in ib[1:] + ip) and \
                    id(tab1) == id(tab2)

    def test_2(self):
        
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TAD_tabuleiro.py', encoding="utf-8").read(), globals())
       
        orbits = 2
        LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*orbits]
        NUMBERS = tuple(range(1,2*orbits + 1))
        
        t = tuple(cria_posicao(l,n) for l in LETTERS for n in NUMBERS)
        ref = ('a2', 'a3', 'a4', 'b4', 'a1', 'b3', 'c3', 'c4', 'b1', 'b2', 'c2', 'd4', 'c1', 'd1', 'd2', 'd3')
        assert tuple(posicao_para_str(obtem_posicao_seguinte(cria_tabuleiro_vazio(orbits), p, False)) for p in t) == ref

    def test_3(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TAD_tabuleiro.py', encoding="utf-8").read(), globals())
       
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        _ = roda_tabuleiro(tab)
        assert tabuleiro_para_str(tab) == \
"""    a   b   c   d
01 [X]-[O]-[ ]-[O]
    |   |   |   |
02 [ ]-[O]-[X]-[O]
    |   |   |   |
03 [ ]-[ ]-[X]-[O]
    |   |   |   |
04 [X]-[X]-[ ]-[ ]"""

    def test_4(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TAD_tabuleiro.py', encoding="utf-8").read(), globals())
       
        orbits = 2
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        ib = tuple(str_para_posicao(i) for i in ib)
        ip = tuple(str_para_posicao(i) for i in ip)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        
        tab1 = cria_tabuleiro_vazio(2)


        for i in ib: coloca_pedra(tab1, i, b)
        for i in ip: coloca_pedra(tab1, i, p)
        
        _ = roda_tabuleiro(tab1)
        
        tab2 = cria_tabuleiro(2, ip, ib)
        print(tabuleiro_para_str(tab1))
        print(tabuleiro_para_str(tab2))
        assert not tabuleiros_iguais(tab1, tab2)
        

    def test_5(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TAD_tabuleiro.py', encoding="utf-8").read(), globals())
       
        tab = cria_tabuleiro_vazio(2)
        b, p = cria_pedra_branca(), cria_pedra_preta()
        ib = 'c1', 'c2', 'd2', 'd3', 'd4'
        ip = 'a3', 'a4', 'b1', 'b3', 'c3'
        for i in ib: coloca_pedra(tab, str_para_posicao(i), b)
        for i in ip: coloca_pedra(tab, str_para_posicao(i), p)
        
        assert (not verifica_linha_pedras(tab,cria_posicao('d',1), cria_pedra_branca(), 3)) and \
            verifica_linha_pedras(tab,cria_posicao('d',2), cria_pedra_branca(), 3)
       
        

class TestPrivateTADEhVendedor:
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
       
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        assert (eh_vencedor(t, cria_pedra_preta()), eh_vencedor(t, cria_pedra_branca())) == (False, False)

    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
       
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        _ = coloca_pedra(t, cria_posicao('d',1), cria_pedra_branca())    
        assert (eh_vencedor(t, cria_pedra_preta()), eh_vencedor(t, cria_pedra_branca())) == (False, True)

class TestPrivateTADEhFimJogo: 
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_vencedor.py', encoding="utf-8").read(), globals()) 
        assert not eh_fim_jogo(cria_tabuleiro_vazio(2))
        
    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_vencedor.py', encoding="utf-8").read(), globals())
         
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        _ = coloca_pedra(t, cria_posicao('d',1), cria_pedra_branca())    
        assert eh_fim_jogo(t)

class TestPrivateTADMovimentoManual: 
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'd1\n')
        ref_text = "Escolha uma posicao livre:"
        ref_move =  'd1'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
                
    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        hyp_move, hyp_text = escolhe_movimento_manual_offline(t, 'c1\nc3\nc4\n')
        ref_text = "Escolha uma posicao livre:Escolha uma posicao livre:Escolha uma posicao livre:"
        ref_move =  'c4'
        assert posicao_para_str(hyp_move) == ref_move and \
            ref_text == hyp_text
        
class TestPrivateTADMovimentoAuto: 
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        move_p = escolhe_movimento_auto(t, cria_pedra_preta(), 'facil')
        move_b = escolhe_movimento_auto(t, cria_pedra_branca(), 'facil')
        assert posicao_para_str(move_p) == 'b2' and \
            posicao_para_str(move_b) == 'b2' 
        
    
    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        move = escolhe_movimento_auto(t, cria_pedra_preta(), 'normal')
        assert posicao_para_str(move) == 'd1'
        
    
    def test_3(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        
        ib = tuple(str_para_posicao(i) for i in ('c1','c2','d2','d3','d4'))
        ip = tuple(str_para_posicao(i) for i in ('a3','a4','b1','b3','c3'))
        t = cria_tabuleiro(2, ip, ib)
        move = escolhe_movimento_auto(t, cria_pedra_branca(), 'normal')
        assert posicao_para_str(move) == 'c4'

class TestPrivateTADOrbito:      
        
    def test_1(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_vencedor.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_fim_jogo.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_auto.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_manual.py', encoding="utf-8").read(), globals())

        res, text = orbito_offline(2, 'facil', 'O',  JOGADA_PUBLIC_1)
        assert res == -1 and text == OUTPUT_PUBLIC_1

    def test_2(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_vencedor.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_fim_jogo.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_auto.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_manual.py', encoding="utf-8").read(), globals())

        res, text = orbito_offline(2, 'normal', 'X', JOGADA_PUBLIC_2)
        assert res ==0 and text == OUTPUT_PUBLIC_2

    def test_3(self):
        exec(open(f'{TAD_CODE_PATH}/TF_posicao.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_pedra.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/TF_tabuleiro.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_vencedor.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_eh_fim_jogo.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_auto.py', encoding="utf-8").read(), globals())
        exec(open(f'{TAD_CODE_PATH}/FAN_movimento_manual.py', encoding="utf-8").read(), globals())

        res, text = orbito_offline(2, '2jogadores', 'X', JOGADA_PUBLIC_3)
        assert res == 1 and text == OUTPUT_PUBLIC_3




##################################
#####  END ABSTRACTION TESTS #####
##################################    

##################################
######### AUXIALIAR CODE #########
##################################

### AUXILIAR CODE NECESSARY TO REPLACE STANDARD INPUT 
class ReplaceStdIn:
    def __init__(self, input_handle):
        self.input = input_handle.split('\n')
        self.line = 0

    def readline(self):
        if len(self.input) == self.line:
            return ''
        result = self.input[self.line]
        self.line += 1
        return result

class ReplaceStdOut:
    def __init__(self):
        self.output = ''

    def write(self, s):
        self.output += s
        return len(s)

    def flush(self):
        return 


def escolhe_movimento_manual_offline(tab, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = escolhe_movimento_manual(tab)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout


def orbito_offline(orbits, lvl, jog, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = orbito(orbits, lvl, jog)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout


JOGADA_PUBLIC_1 = 'd1\nc1\nb1\nb4\n'
OUTPUT_PUBLIC_1 = \
"""Bem-vindo ao ORBITO-2.
Jogo contra o computador (facil).
O jogador joga com 'O'.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[O]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[O]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [O]-[O]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [O]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [O]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[ ]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[X]-[X]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[X]-[ ]
    |   |   |   |
03 [O]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[O]-[O]-[ ]
Turno do computador (facil):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[X]-[X]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [O]-[O]-[O]-[O]
VITORIA
"""

JOGADA_PUBLIC_2 = "c2\na3\nb2\na2\na3\na2\nb1\n"
OUTPUT_PUBLIC_2 = \
"""Bem-vindo ao ORBITO-2.
Jogo contra o computador (normal).
O jogador joga com 'X'.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[ ]-[ ]
    |   |   |   |
03 [ ]-[X]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[O]-[X]-[ ]
    |   |   |   |
04 [X]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[X]-[ ]
    |   |   |   |
03 [ ]-[O]-[O]-[ ]
    |   |   |   |
04 [ ]-[X]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[O]-[ ]
    |   |   |   |
04 [ ]-[ ]-[X]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [O]-[O]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[X]
Turno do jogador.
Escolha uma posicao livre:Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[X]-[ ]
    |   |   |   |
03 [O]-[O]-[X]-[X]
    |   |   |   |
04 [X]-[ ]-[ ]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[X]-[X]-[X]
    |   |   |   |
03 [O]-[O]-[O]-[ ]
    |   |   |   |
04 [O]-[X]-[ ]-[ ]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[X]
    |   |   |   |
02 [ ]-[X]-[O]-[ ]
    |   |   |   |
03 [X]-[X]-[O]-[ ]
    |   |   |   |
04 [O]-[O]-[X]-[ ]
Turno do computador (normal):
    a   b   c   d
01 [ ]-[ ]-[X]-[ ]
    |   |   |   |
02 [O]-[O]-[O]-[ ]
    |   |   |   |
03 [ ]-[X]-[X]-[ ]
    |   |   |   |
04 [X]-[O]-[O]-[X]
Turno do jogador.
Escolha uma posicao livre:    a   b   c   d
01 [X]-[X]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[X]-[ ]
    |   |   |   |
03 [O]-[O]-[X]-[X]
    |   |   |   |
04 [ ]-[X]-[O]-[O]
Turno do computador (normal):
    a   b   c   d
01 [X]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[X]-[X]-[X]
    |   |   |   |
03 [O]-[O]-[O]-[O]
    |   |   |   |
04 [O]-[ ]-[X]-[O]
EMPATE
"""

JOGADA_PUBLIC_3 = "a1\nb2\na4\nc4\na4\nb3\nb4\na3\n"
OUTPUT_PUBLIC_3 = \
"""Bem-vindo ao ORBITO-2.
Jogo para dois jogadores.
    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [X]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [X]-[O]-[ ]-[ ]
    |   |   |   |
04 [ ]-[ ]-[ ]-[ ]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[O]-[ ]
    |   |   |   |
04 [X]-[X]-[ ]-[ ]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[O]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
04 [ ]-[X]-[X]-[O]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[O]-[ ]-[ ]
    |   |   |   |
03 [ ]-[ ]-[ ]-[O]
    |   |   |   |
04 [ ]-[X]-[X]-[X]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[ ]
    |   |   |   |
02 [ ]-[ ]-[ ]-[O]
    |   |   |   |
03 [ ]-[O]-[O]-[X]
    |   |   |   |
04 [ ]-[ ]-[X]-[X]
Turno do jogador 'X'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[ ]-[O]
    |   |   |   |
02 [ ]-[ ]-[O]-[X]
    |   |   |   |
03 [ ]-[ ]-[O]-[X]
    |   |   |   |
04 [ ]-[ ]-[X]-[X]
Turno do jogador 'O'.
Escolha uma posicao livre:    a   b   c   d
01 [ ]-[ ]-[O]-[X]
    |   |   |   |
02 [ ]-[O]-[O]-[X]
    |   |   |   |
03 [ ]-[ ]-[ ]-[X]
    |   |   |   |
04 [O]-[ ]-[ ]-[X]
VITORIA DO JOGADOR 'X'
"""
