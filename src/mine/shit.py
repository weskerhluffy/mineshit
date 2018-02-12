'''
Created on 09/02/2018

@author: 

XXX: https://code.google.com/codejam/contest/2974486/dashboard#s=p2
'''

import logging
import sys
from sys import stdin
from functools import partial

nivel_log = logging.ERROR
#nivel_log = logging.DEBUG
logger_cagada = None

def posicion_genera_vecinos_alrededor(posicion):
    movs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    return list(map(partial(posicion_suma, posicion), movs))

def caca_comun_lee_valor_en_posicion(matrix, pos):
    return matrix[pos[0]][pos[1]]

def mineshit_valida_matrix(matrix):
    x = len(matrix)
    y = len(matrix[0])
    xr = x + 2
    yr = y + 2
    matrixr = caca_comun_crea_matrix(xr, yr, "x")
    for xa in range(1, x + 1):
        for ya in range(1, y + 1):
            caca_comun_asigna_valor_en_posicion(matrixr, (xa, ya), matrix[xa - 1][ya - 1])
            
    logger_cagada.debug("matrix antes de validar \n{}".format(caca_comun_imprime_matrix(matrixr)))
    
    for xa in range(1, x + 1):
        for ya in range(1, y + 1):
            pa = (xa, ya)
            if caca_comun_lee_valor_en_posicion(matrixr, pa) == ".":
                c = 0
                for v in posicion_genera_vecinos_alrededor(pa):
                    if caca_comun_lee_valor_en_posicion(matrixr, v) == "*":
                        c += 1
                caca_comun_asigna_valor_en_posicion(matrixr, pa, "{}".format(c))
                
    logger_cagada.debug("matrix numerada \n{}".format(caca_comun_imprime_matrix(matrixr)))
    
    pila = []
    
    pila.append((1, 1))
    while pila:
        pa = pila.pop()
        vs = posicion_genera_vecinos_alrededor(pa)
        for v in vs:
            if caca_comun_lee_valor_en_posicion(matrixr, v) == "0":
                pila.append(v)
            if caca_comun_lee_valor_en_posicion(matrixr, v) != "x":
                caca_comun_asigna_valor_en_posicion(matrixr, v, "c")
    
    for xa in range(1, x + 1):
        for ya in range(1, y + 1):
            pa = (xa, ya)
            assert caca_comun_lee_valor_en_posicion(matrixr, pa) in ["c", "*"]
    logger_cagada.debug("matrix validada\n{}".format(caca_comun_imprime_matrix(matrixr)))
        
    

def mineshit_encuentra_rectangulo(x, y, libres, primera_llamada):
    resultados = []
    logger_cagada.debug("x {} y {} libres {}".format(x, y, libres))
    if not x or not y:
        return resultados
    if primera_llamada:
        min_x = 2
    else:
        min_x = 1
    for yi in range(y, 1, -1):
        for xi in range(x, min_x - 1, -1):
            t = xi * yi
            if t <= libres:
                r = libres % t
                logger_cagada.debug("probando con xi {} yi {} librres {} r {}".format(xi, yi, libres, r))
                if not r:
                    resultados.append((xi, yi))
                    break
                else:
                    res_tmp = mineshit_encuentra_rectangulo(x - xi, yi, r, False)
                    if res_tmp:
                        resultados = [(xi, yi)] + res_tmp
                        break
        if resultados:
            break
    logger_cagada.debug("x {} y {} libres {} res {}".format(x, y, libres, resultados))
    return resultados

def posicion_suma(pos_1, pos_2):
    return [pos_1[0] + pos_2[0], pos_1[1] + pos_2[1]]

def caca_comun_asigna_valor_en_posicion(matrix, pos, valor):
    matrix[pos[0]][pos[1]] = valor

def caca_comun_imprime_matrix(matrix):
    return "\n".join(map(lambda fila:"".join(fila), matrix))

def minishit_pinta_recto(matrix, pos_ini, rx, ry):
    tx = len(matrix)
    ty = len(matrix[0])
    logger_cagada.debug("caca matrix {} {} pos {} tam {} {}".format(tx, ty, pos_ini, rx, ry))
    assert rx <= tx
    assert ry <= ty
    assert pos_ini[0] + rx <= tx
    assert pos_ini[1] + ry <= ty
    
    posis = map(partial(posicion_suma, pos_ini), [(i, j) for i in range(rx) for j in range(ry)])
#    logger_cagada.debug("las pos a pintar {}".format(posis))
#    map(lambda posi:caca_comun_asigna_valor_en_posicion(matrix, posi, "."), posis)
    for posi in posis:
        caca_comun_asigna_valor_en_posicion(matrix, posi, ".")
#        matrix[posi[0]][posi[1]] = "A"
#    logger_cagada.debug("la matrix kedo {}".format(matrix))
    
def caca_comun_crea_matrix(x, y, valor):
    matrix = []
    for _ in range(x):
        matrix.append([valor] * y)
    return matrix
        
def mineshit_core(x, y, m):
    se_volteo = False
    if x > y:
        x, y = y, x
        se_volteo = True
    t = x * y
    libres = t - m
    if not m or libres == 1:
        if not m:
            caca="."
        else:
            caca="*"
        if se_volteo:
            x, y = y, x
        matrix = caca_comun_crea_matrix(x, y, caca)
        caca_comun_asigna_valor_en_posicion(matrix, (0, 0), "c")
        return matrix
    matrix = None
    rectos = []
    if(x == 1):
        if libres > 1:
            rectos = [(1, libres)]
    if(x == 2):
        if libres > 2 and not (libres & 1):
            rectos = [(2, libres // 2)]
    if(x > 2):
        if(libres >= 4):
            rectos = mineshit_encuentra_rectangulo(x, y, libres, True)
    
    logger_cagada.debug("para cuadro {}x{} con libres {} se encontron cuadros {}".format(x, y, libres, rectos))
    if rectos:
        mierda = 0
        matrix = caca_comun_crea_matrix(x, y, "*")
        posi = [0, 0]
        for recto_x, recto_y in rectos:
            mierda += recto_x * recto_y
            minishit_pinta_recto(matrix, posi, recto_x, recto_y)
            posi[0] += recto_x
            logger_cagada.debug("la matrix con recto {}x{} es\n{}".format(recto_x, recto_y, caca_comun_imprime_matrix(matrix)))
        assert mierda == libres
        caca_comun_asigna_valor_en_posicion(matrix, (0, 0), "c")
        mineshit_valida_matrix(matrix)
        
    if se_volteo:
        if matrix:
            matrix = list(zip(*matrix[::]))
    return matrix
        
def caca_comun_lee_linea_como_num():
    return int(stdin.readline().strip())

def caca_comun_lee_linea_como_monton_de_numeros():
    return list(map(int, stdin.readline().strip().split(" ")))
def mineshit_main():
    cacasos = caca_comun_lee_linea_como_num()
    for i in range(cacasos):
        x, y, m = caca_comun_lee_linea_como_monton_de_numeros()
        mamada = mineshit_core(x, y, m)
        print("Case #{}:".format(i + 1))
        if(mamada):
            pass
            print("{}".format(caca_comun_imprime_matrix(mamada)))
        else:
            pass
            print("Impossible")

if __name__ == '__main__':
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)
        mineshit_main()
