# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

#CONSTANTES 

ANCHO_CADRO = 85
ALTO_CADRO = 85

MARCO = 15

GROSOR_LINHA = 2

COLOR_FONDO = [255,255,255]
COLOR_LINHAS = [80,80,80]
COLOR_1 = [0,0,100]
COLOR_2 = [200,0,0]
COLOR_VICTORIA = [100,200,100]

ANCHO_VENTANA = ANCHO_CADRO*3 + MARCO*2
ALTO_VENTANA = ALTO_CADRO*3 + MARCO*2

lista_casillas = [[0,0,0],[0,0,0],[0,0,0]]
lista_colores = [[0,0,0],[0,0,0],[0,0,0]]

#FUNCIÓNS

def enraia(list,xogador):
	for linha in range(len(list)):
		if "".join(map(str, list[linha])) == str(xogador)*3:
			lista_colores[linha] = [1,1,1]
			return True
	for columna in range(len(list)):
		if "".join(map(str, [list[0][columna],list[1][columna],list[2][columna]])) == str(xogador)*3:
			lista_colores[0][columna],lista_colores[1][columna],lista_colores[2][columna] = 1,1,1
			return True
	if "".join(map(str, [list[0][0],list[1][1],list[2][2]])) == str(xogador)*3:
		lista_colores[0][0],lista_colores[1][1],lista_colores[2][2] = 1,1,1
		return True
	if "".join(map(str, [list[0][2],list[1][1],list[2][0]])) == str(xogador)*3:
		lista_colores[0][2],lista_colores[1][1],lista_colores[2][0] = 1,1,1
		return True
	return False
	
#XOGO

ganador = False
casilla_rato = False
xogador = 1

pygame.init()
ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
font = pygame.font.SysFont("System", ANCHO_VENTANA/5)

on = True

while on:

	reloj = pygame.time.Clock()
	
	#DEBUXAR
	
	ventana.fill(COLOR_FONDO)
	
	rect_xogo = pygame.Rect(MARCO, MARCO, ANCHO_VENTANA-(MARCO*2), ALTO_VENTANA-(MARCO*2))
	pygame.draw.rect(ventana, [250,250,250], rect_xogo)
						
	for linha in range(len(lista_casillas)):
		for casilla in range(len(lista_casillas[linha])):
			#DEBUXAR SELECCIÓN
			if casilla_rato == [casilla,linha]:
				rect_sel = pygame.Rect(MARCO+ANCHO_CADRO*casilla, MARCO+ALTO_CADRO*linha, 
							ANCHO_CADRO, ALTO_CADRO)
				pygame.draw.rect(ventana, [240,240,240], rect_sel)
			#DEBUXAR GAÑADORES
			if ganador and lista_colores[linha][casilla]:
				rect_ganador = pygame.Rect(MARCO+ANCHO_CADRO*casilla, MARCO+ALTO_CADRO*linha, 
							ANCHO_CADRO, ALTO_CADRO)
				pygame.draw.rect(ventana, COLOR_VICTORIA, rect_ganador)
			#DEBUXAR SÍMBOLOS
			if lista_casillas[linha][casilla]:
				if lista_casillas[linha][casilla] == 1:
					simbolo = font.render("X", 1, COLOR_1)
				else:
					simbolo = font.render("O", 1, COLOR_2)
				ventana.blit(simbolo, [(MARCO+ANCHO_CADRO*casilla)+(ANCHO_CADRO/2)-simbolo.get_width()/2,
										(MARCO+ALTO_CADRO*linha)+(ALTO_CADRO/2)-simbolo.get_height()/2])
			
	for i in range(4):
		pygame.draw.line(ventana, COLOR_LINHAS, [MARCO, MARCO+i*ALTO_CADRO],
						[ANCHO_VENTANA-MARCO, MARCO+i*ALTO_CADRO], GROSOR_LINHA)
		pygame.draw.line(ventana, COLOR_LINHAS, [MARCO+i*ANCHO_CADRO, MARCO],
						[MARCO+i*ANCHO_CADRO, ALTO_VENTANA-(MARCO)], GROSOR_LINHA)
	
	#UPDATE DA PANTALLA
	
	pygame.display.update()
	
	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	if (MARCO < pos_mouse[0] < ANCHO_VENTANA-MARCO
		and MARCO < pos_mouse[1] < ALTO_VENTANA-(MARCO)):
		casilla_rato = [(pos_mouse[0]-MARCO)/ANCHO_CADRO,(pos_mouse[1]-MARCO)/ALTO_CADRO]
	else:
		casilla_rato = False
		
	if (not ganador) and casilla_rato and pygame.mouse.get_pressed()[0]:
		if not lista_casillas[casilla_rato[1]][casilla_rato[0]]:
			lista_casillas[casilla_rato[1]][casilla_rato[0]] = xogador
			if enraia(lista_casillas,xogador):
				ganador = xogador
			xogador = 2 if xogador == 1 else 1
	
	#EVENTOS
	
	for evento in pygame.event.get():
	
		if evento.type == pygame.KEYDOWN:
			if evento.key == K_SPACE:
				lista_casillas = [[0,0,0],[0,0,0],[0,0,0]]
				lista_colores = [[0,0,0],[0,0,0],[0,0,0]]
				ganador = False

		#EXIT
		
		if evento.type == pygame.QUIT:
			pygame.display.quit()
			on = False
	
	reloj.tick(60)
