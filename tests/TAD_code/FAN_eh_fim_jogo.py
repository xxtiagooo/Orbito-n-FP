def eh_fim_jogo(tab):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    orbits = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    all_pos = tuple(cria_posicao(col, lin) for lin in NUMBERS for col in LETTERS)
    return all((eh_pedra_jogador(obtem_pedra(tab, pos)) for pos in all_pos)) or \
        (eh_vencedor(tab, cria_pedra_branca()) or eh_vencedor(tab, cria_pedra_preta()))
