
def escolhe_movimento_auto(tab, pedra, lvl):
    
    cambio_turno = lambda jog: (cria_pedra_preta() if pedras_iguais(jog, cria_pedra_branca()) else cria_pedra_branca())
  
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
    
    mode = {'facil': facil,
            'normal': normal}
    
    candidates = mode[lvl](tab, pedra)    
    if not candidates:
        candidates = obtem_posicoes_pedra(tab, cria_pedra_neutra())
    
    return candidates[0]