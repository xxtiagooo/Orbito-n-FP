
def escolhe_movimento_manual(tab):
    MAX_ORBITS = 5
    MAX_LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:2*MAX_ORBITS]
    MAX_NUMBERS = tuple(range(1,2*MAX_ORBITS + 1))
    
    orbits = obtem_numero_orbitas(tab)
    LETTERS = MAX_LETTERS[:2*orbits]
    NUMBERS = MAX_NUMBERS[:2*orbits]

    while True:
        # Repetir pergunta até escolher uma posicao valida 
        cad = input('Escolha uma posicao livre:')
        if len(cad) >= 2 and cad[0] in LETTERS and cad[1:].isdigit() and int(cad[1:]) in NUMBERS:
            pos = cria_posicao(cad[0], int(cad[1:]))
            
            if not eh_pedra_jogador(obtem_pedra(tab, pos)):
                return pos 
            