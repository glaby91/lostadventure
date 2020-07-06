org #6000

miams EQU #5500

;affichage du niveau 

LD H,1   ; locate H,L 
LD L,1   ;
LD IX,#5000
blcy:
	bclx:

	ld a,(IX)  ; charge la valeur de l'index 
	CP 2
	CALL Z,CMIAM
	;CP 0
	;JP Z,FOND
	CP 1
	JP Z,MUR
	CP 2
	JP Z,MIAM
	CP 3
	JP Z,PORTE
	CP 4
	JP Z,MUR1
	CP 5
	JP Z,MUR2
	CP 6
	JP Z,MUR3
	CP 7
	JP Z,MUR4
	CP 8
	JP Z,COEUR
		SUITE:
		INC H
		LD A,H
		CP 41
		JP Z,SORT
		INC IX
	JP bclx
	
SORT:
LD H,1
INC L
INC IX
LD A,L
CP 26
JP Z,FIN
JP BLCY
FIN:
;trace les coins:
LD H,40
BCLCOIN:
LD L,1
CALL COIN1
LD L,25
CALL COIN1
DEC H
LD A,H
JP Z,S1
JP BCLCOIN
S1:

LD L,25
BCLCOIN1:
LD H,1
CALL COIN1
LD H,40
CALL COIN1
DEC L
LD A,L
JP Z,S2
JP BCLCOIN1
S2:

RET
CMIAM:
LD A,(miams)
INC A
LD A,(IX)
RET

COIN1:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,143 ; caractere de fond mur
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
RET

FOND:
PUSH HL
LD A,0
CALL #BB90 ; selection de l'encre 0
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,143 ; caractere de fond mur
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE 

MUR:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,143 ; caractere de fond mur
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL

JP SUITE

MIAM:
PUSH HL
LD A,3
CALL #BB90 ; selection de l'encre 3
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,231 ; caractere de mima
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

PORTE:
PUSH HL
LD A,2
CALL #BB90 ; selection de l'encre 3
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,207 ; caractere de mima
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

COEUR:
PUSH HL
LD A,2
CALL #BB90 ; selection de l'encre 3
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,228 ; caractere de coeur
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

mur1:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,244 ; caractere de mur1
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

mur2:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,245 ; caractere de mur2
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

mur3:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,246 ; caractere de mur3
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE

mur4:
PUSH HL
LD A,1
CALL #BB90 ; selection de l'encre 1
POP HL
PUSH HL
CALL #BB75 ; locate H,L
POP HL
LD A,247 ; caractere de mur4
PUSH HL
CALL #BB5A ; affiche le caractere
POP HL
JP SUITE



