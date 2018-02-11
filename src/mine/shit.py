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
nivel_log = logging.DEBUG
logger_cagada = None

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
        d = libres // yi
        r = libres % yi
        logger_cagada.debug("probando con {} d {} r {}".format(yi, d, r))
        if min_x <= d <= x:
            if not r:
                resultados.append((d, yi))
                break
            else:
                if min_x <= d <= x:
                    res_tmp = mineshit_encuentra_rectangulo(x - d, yi, r, False)
                    if res_tmp:
                        resultados = [(d, yi)] + res_tmp
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
    if not m:
        matrix = caca_comun_crea_matrix(x, y, ".")
        caca_comun_asigna_valor_en_posicion(matrix, (0, 0), "c")
        return matrix
    if x > y:
        x, y = y, x
        se_volteo = True
    t = x * y
    libres = t - m
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
        matrix = caca_comun_crea_matrix(x, y, "*")
        posi = [0, 0]
        for recto_x, recto_y in rectos:
            minishit_pinta_recto(matrix, posi, recto_x, recto_y)
            posi[0] += recto_x
            logger_cagada.debug("la matrix con recto {}x{} es\n{}".format(recto_x, recto_y, caca_comun_imprime_matrix(matrix)))
        caca_comun_asigna_valor_en_posicion(matrix, (0, 0), "c")
        
    if se_volteo:
        if matrix:
            matrix = zip(*matrix[::])
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
#            print("{}".format(caca_comun_imprime_matrix(mamada)))
        else:
            pass
#            print("Impossible")

if __name__ == '__main__':
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)
        mineshit_main()
