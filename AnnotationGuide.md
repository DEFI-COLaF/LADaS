# Annotation Guide

## DigitizationArtefactZone
All the elements resulting from the digitalization process (for example watermarks of the institution preserving the document)

 Le_Prince_Dgem_chronique_dauphinoise_-----Arnaud_Victor_bpt6k5468703r_11.jpeg



Fichier exemple : bpt6k1092529g_f14.jpg

## DropCapitalZone

## GraphicZone

Inclut toute la figure (photographie, schéma, dessin) et légende.

## GraphicZone:Decoration

## Un tampon ou un élément graphique servant à décorer le texte, généralement pour séparer deux éléments.

## GraphicZone:Legend

La légende d'une GraphicZone.

## GraphicZone:Maths

Une formule mathématique à part du corps du texte (et non au milieu d'une ligne d'un paragraphe).

Une GraphicZoneMaths peut être accompagnée d’une GraphicZone:Legend.


Fichier exemple :  bpt6k1421246p_f358.jpg

Une GraphicZone:Maths ne peut pas être une illustration type géométrie : 


Fichier exemple :  bd6t5371525p_f68.jpg

## GraphicZone:P
Un paragraphe intégré dans une illustration et qui n’est pas une légende. Généralement un commentaire ou une explication en lien avec l’illustration avec lequel la GraphicZone:P est lié. 
Quand cela est possible, intégrer la GraphicZone:P dans la GraphicZone principale.

Fichier exemple : bd6t53682106_f109.jpg
MainZone:Date

Une date dans une correspondance ou un article. Attention, la date doit être reconnaissable par sa position "géographique", et non son contenu textuel.

MainZone:Entry, MainZone:Entry#Continued

Une entrée de catalogue. Graphiquement, une entrée est généralement définie par un artifice typographique (gras, italique) et d'un ordonnancement (alphabétique, numérique, etc.).


Fichier exemple : bd6t5369916x_f31.jpg

## MainZone:Form

Un formulaire

## MainZone:Head

Un ent-tête séparé du reste du texte
Une MainZone:Head ne peut pas être superposé avec une MainZone:P et #Continued.

## MainZone:Lg, MainZone:Lg#Continued

Un ensemble de vers

## MainZone:List, MainZone:List#Continued

Un élément d'une liste.

 MainZone:List#Continued permet d’annoter un élément de liste commencé sur une autre page, ou interrompu dans la page.


Fichier exemple : bd6t53771507_f86.jpg
## MainZone:Other

Tout truc qui passe pas dans le reste

## MainZone:P, MainZone:P#Continued

Paragraphe de texte classique.

Une MainZone:P et #Continued ne peut pas être superposé avec une MainZone:Head.

## MainZone:Signature

Une signature (nom d'auteur par exemple dans une correspondance)

## MainZone:Sp, MainZone:Sp#Continued

Un élément de dialogue pour le théâtre (principalement). Graphiquement, l'élément représentant le nom du speaker doit être visible, une didascalie peut être inclue, et un élément graphique doit séparer le nom du speaker du texte dit.

## MarginTextZone:ManuscriptAddendum

Une note marginale manuscrite

## MarginTextZone:Notes, MarginTextZone:Notes#Continued

Un ensemble de notes (non séparées individuellement). Si en plusieurs colonnes, utiliser #continued pour la deuxième colonne.


Fichier exemple : bd6t53717102_f63.jpg

## NumberingZone

Un numéro de page

## PageTitleZone

Un ensemble de segments de texte formant une page de titre qui n’est pas comprise dans le corps du texte.



Fichier exemple : bd6t5372200f_f3.jpg
PageTitleZone:Index

Un index ou sommaire

## QuireMarkZone

## RunningTitleZone

Un titre (complet ou abrégé) en dehors du corps du texte, majoritairement placé en haut de page.


Fichier exemple : bpt6k10981259_f27.jpg

## StampZone


## StampZone:Sticker

Un sticker identifiant le livre (généralement avec un côte)

## TableZone

Une table, légende inclue. Comprend toute forme graphique reproduisant un système de colonne et de lignes, y compris sans bordure.

Si du texte est exclu de la forme graphique du tableau mais appartient à celui-ci, l’inclure dans la TableZone. 


Fichier exemple : bd6t53701166_f31.jpg

## TableZone:Legend

La légende table


