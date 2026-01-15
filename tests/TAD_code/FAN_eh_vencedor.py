def eh_vencedor(tab, jogador):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    orbits = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]
    
    # nao preciso em todas basta com a primeira linha e a primeira coluna
    all_pos = tuple(cria_posicao('a', lin) for lin in NUMBERS) + \
        tuple(cria_posicao(col, 1) for col in LETTERS)
    
    return any(verifica_linha_pedras(tab, pos, jogador,2*orbits) for pos in all_pos)
             