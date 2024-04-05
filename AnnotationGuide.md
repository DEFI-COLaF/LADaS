# Annotation Guide
This annotation guide primarily incorporates [Segmonto guidelines](https://segmonto.github.io), with some adjustments made to align with our documents, particularly regarding the subtypes.

## DigitizationArtefactZone
### 1. Definition
DigitalArtefactZone: contains any types of item external to the document itself present on the image because of the digitisation process.
### 2. Examples
<p class="float" align="center">
<img src="Images_annotation/Le_Prince_Dgem_chronique_dauphinoise_-----Arnaud_Victor_bpt6k5468703r_11.jpeg.png" width="400"/>
<img src="Images_annotation/bpt6k1092529g_f14.jpg" width="400"/>
</p>
The digitalizationartefactZone is in orange.</br>
Right: Le_Prince_Dgem_chronique_dauphinoise_-----Arnaud_Victor_bpt6k5468703r_11.jpeg </br>
Left: bpt6k1092529g_f14.jpg

## DropCapitalZone

### 1.Definition
DropCapitalZone: contains any type of initial letter occupying a space corresponding to several lines of the main text or bearing  significant ornementation, be they historiated, ornated, flourished or painted initials (and excluding the following text line).
### 2. Examples

## GraphicZone
### 1. Definition
GraphicZone: a zone containing any type of graphic element, from purely ornamental information to information consubstantial to the text (e.g. full-page paintings, line-fillers, marginal drawings, figures, etc.). Captions, if there are any, is part of this zone, and its text line is labelled HeadingLine. If an image contains text, it is possible to label the lines as DefaultLine.
### 2. Subtypes
   Values used:
   - GraphicZone:Part : a graphic element (photography, plot, etc...) defined as a sub-element of a GraphicZone containing at least one graphic (picture, schema, plot, etc.) and one element identifying it as a part of a whole (a GraphicZone:FigDesc or a NumberingZone)
   - GraphicZone:Decoration: a graphical element decorating the text, such as separator ornament.
   - GraphicZone:Head: GraphicZone's main caption (usually, in scientific paper, the part preceded by Figure X:)
   - GraphicZone:FigDesc :GraphicZone's secondaries captions. A GraphicZone:FigDesc can only be present if a GraphicZone:Head has already been used. A GraphicZone:FigDesc encompasses secondary explanation (usually a small paragraph below a GraphicZone:Head) or serves as names for Part of the `GraphicZone` (a figure with two different plot and two plot titles on top of the main caption).
   - GraphicZone:Maths: Mathematical Formula separated from the main text. This doesn't apply to formula within the text. A GraphicZoneMaths can be associated with a GraphicZone:Legend.
   - GraphicZone:TextualContent: Text in an illustration which is not a caption. Usually a commentary and explanation on the illustration. When it is possible, the graphicZone:P is included in the principle GraphiZone.
### 3. Examples
graphiczone:maths
<p class="float" align="center">
 <img src="Images_annotation/bpt6k1421246p_f358.jpg" width="400"/>
</p>
Example: bpt6k1421246p_f358.jpg

Geometric Illustration are not GraphicZone:Maths but rather simple GraphicZone.

<p class="float" align="center">
 <img src="Images_annotation/bd6t5371525p_f68.jpg" width="400"/>
</p>
Example :  bd6t5371525p_f68.jpg

Graphiczone textualcontent

<p class="float" align="center">
 <img src="Images_annotation/bd6t53682106_f109.jpg" width="400"/>
</p>
Example : bd6t53682106_f109.jpg

## MainZone
### 1.Definition
MainZone is the main area containing the text, excluding any paratext, and it is either a single block or multiple columns. Thus, the MainZone is characterised by the importance of the text it bears, yet it does not exclude the presence of non-textual information (music notation, illuminationdots). When a page is divided into columns or blocks, each one is a different zone. Possible ornamentations (headpiece, tailpiece, etc.) are part of the MainZone, even if there is no text above or above those GraphicZone.
### 2.Subtypes
     - MainZone:Date: A date in a correspondance or an article. The date should be visually recognizable due to its geographical position in the page rather than its meaning.
     - MainZone:Entry, MainZone:Entry#Continued: A catalogue's entry. Graphically, an entry is usually defined by a typographic elements (italic, bold) and a structuration (alphabetical, numerical..).
     - MainZone:Form:A form.
     - MainZone:Head: A header separated from the rest of the text. A MainZone:Head should not overlap with a MainZone:P or MainZone:P#Continued. 
     - MainZone:Lg, MainZone:Lg#Continued: A group of verses lines.
     - MainZone:List, MainZone:List#Continued: A list item. MainZone:List#Continued allows to annotate a liste item that begin on another page or was interrupted.
     - MainZone:Other: When none of the mainZone can be used.
     - MainZone:P, MainZone:P#Continued: A normal paragraph of text. MainZone:P and MainZone:P#Continued should not overlap with a MainZone:Head.
     - MainZone:Signature: A signature (For example, in a correspondance, the authors' name). It should be graphically separated from the rest of the text.
     - MainZone:Sp, MainZone:Sp#Continued: A dialog element, mostly for theatre. It must contain the speaker's name, stage directions and a graphical element separating the speaker's name from his speech.
### 3.Examples
<p class="float" align="center">
 <img src="Images_annotation/bd6t5369916x_f31.jpg" width="400"/>
</p>
Example : bd6t5369916x_f31.jpg




<p class="float" align="center">
 <img src="Images_annotation/bd6t53771507_f86.jpg" width="400"/>
</p>
Example : bd6t53771507_f86.jpg

## MarginTextZone
### 1. Definition
### 2.Subtypes
    - MarginTextZone:ManuscriptAddendum: A handwritten margin note.
    - MarginTextZone:Notes, MarginTextZone:Notes#Continued: Footnotes and Margin Notes (not separated invidually). MarginTextZone:Notes#Continued is used when there are multiple columns of notes on the page.
### 3.Examples
<p class="float" align="center">
 <img src="Images_annotation/bd6t53717102_f63.jpg" width="400"/>
</p>

Example: bd6t53717102_f63.jpg

## NumberingZone
### 1.Definition
MarginTextZone: characterises any text zone contained in the margins no matter its position on the page (upper, lower, inner or outer), including the space between two columns. We do not differentiate the zone's particular semantic status (gloss, addition, correction, intertextual or bibliographic reference…).
### 2.Subtypes
### 3.Examples

## PageTitleZone
### 1.Definition
PageTitleZone: characterises the entire page, rather than a section within a page, that contains for instance headings (chapter title, act or scene number, etc.). It is distinct from other pages and is traditionally the first page of a document, especially in the case of prints. It provides bibliographic or identifying information, such as the title of the work, the production date, the names of the printer(s), publisher(s) and author(s), etc. This area normally contains HeadingLine. Information added a posteriori (for example by the librarian) is in a MarginTextZone.
### 2.Subtypes
     - PageTitleZone:Index: Table of contents
### 3.Examples
<p class="float" align="center">
 <img src="Images_annotation/bd6t5372200f_f3.jpg" width="400"/>
</p>

Example: bd6t5372200f_f3.jpg

## QuireMarkZone
### 1.Definition
QuireMarksZone: is a zone containing a quire signature (e.g. a ii), catchword, or any kind of element relative to the material organisation of the source, with the exclusion of page, folio, or item numbers. The zone usually is at the bottom of the page.
### 2.Subtypes
### 3.Examples
## RunningTitleZone

A (complete or abbreviated) title outside of the main text, usually placed at the top of the page.
<p class="float" align="center">
 <img src="Images_annotation/bpt6k10981259_f27.jpg" width="400"/>
</p>
RunningTitleZone is in pink.</br>
Example: bpt6k10981259_f27.jpg

## StampZone
### 1.Definition
StampZone: is a zone containing a stamp, be it a library stamp or a mark from a postal service.
### 2.Subtypes
    - StampZone:Sticker: A sticker identifying the book (usually with a code)
### 3.Examples

## TableZone
### 1.Definition
TableZone: is a zone containing a table of any kind. The table can be clearly drawn (with rows and columns) or not. The tables of contents are in the vast majority of cases not tables.
Caption should be included. If there is some text not contained by the graphical form of the table but it is appart of the table, include it in the tableZone.
### 2.Subtypes
   - TableZone:Legend: The caption of the table. Should be contained by the tableZone.

### 3.Examples
<p class="float" align="center">
 <img src="Images_annotation/bd6t53701166_f31.jpg" width="400"/>
</p>
Example : bd6t53701166_f31.jpg




