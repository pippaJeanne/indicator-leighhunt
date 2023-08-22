# Reference Document
This document is intended for reference purposes. It contains a list of various tagging elements and their descriptions, with the aim of uniformity in tagging.

## Table of Contents
- [Using the Undoubler](#using-the-undoubler)
- [Elements](#elements)
    - [Div Elements](#div-elements)
    - [Page Elements](#page-elements)
    - [Head Elements](#head-elements)
    - [Note Elements](#note-elements)
    - [Citation Elements](#citation-elements)
    - [Choice Elements](#choice-elements)
    - [Hi Elements](#hi-elements)
    _ [lg Elements](#lg-elements)
- Examples

## Using the Undoubler
In the repository you'll find a script titled 'undoubler'. This script was written to rectify some basic issues with the OCRed text, principally the use of double spaces in place of single spaces. The script is a Python script, and takes an input text ('raw_double.txt') and outputs it to a new clean file ('un_double.txt').

## Elements

### Div Elements
```<div>``` (text division) contains a subdivision of the front, body, or back of a text. [4.1 Divisions of the Body](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/DS.html#DSDIV)

The divider elements are numbered to provide a more immediate indication of their relative position in the hierarchy.

```<div1 type="issue" n="">``` elements are used as general containers for the entire issue (aka chapter) of the publication. This is mostly to future-proof the layout in case all the publications get combined into one file. The type is always "issue" and the n attribute is the issue number in modern Arabic numerals.

```<div2 type="{ title, section, correspondents, colophon }" n="">``` elements are used as general containers for the title, sections, and colophon of the publication issue. The title div contains the title, epigraph, and catalogue data. The section contains the header and text. The correspondents type contains the occasional note to correspondents that closes some issues and precedes the colophon. The colophon contains the publication and printing notice appended to each issue. The type is always "title", "section", "correspondents", or "colophon" and the n attribute is the section number in modern Arabic numerals when using the "section" divider.

```<div3 type="subsection" n="">``` elements are used as containers for the subsections within the main div2 type sections. The type will always be "subsection" and the value of the n attribute corresponds to the subsection number in modern Arabic numerals. 

### Page Elements
```<pb n="" />``` (page beginning) marks the beginning of a new page in a paginated document. [3.11.3 Milestone Elements](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/CO.html#CORS5) This is for reference purposes only, and is not intended to signal that the page is reproduced exactly in the digital edition.

### Head Elements
```<head type="" n="">``` (heading) contains any type of heading, for example the title of a section, or the heading of a list, glossary, manuscript description, etc. [4.2.1 Headings and Trailers](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/DS.html#DSHD)

Types:
- title: The title of the document (ie. The Indicator)
- catalogue: Publication no., and date of publication (ie. No. XXIV.—WEDNESDAY, MARCH 22d, 1820.)
- header: The header of a section or subsection within the publication issue (ie. "ON THE REALITIES OF IMAGINATION.")

### Note Elements
```<note type="">```

Types:
- source: indicating the source of a text or reference.
- hunt: note present in the original / written by Hunt.
- editorial: editorial note.

### Citation Elements
```xml
<cit>
    <quote>
        <!--Quoted elements exist here. They can be formatted normally (i.e. <lg> and <l> for verse, <p> for prose).-->
    </quote>
    <note type="source"> 
        <bibl> </bibl>
    </note>
</cit>
 ```
For rendering of poems: 
```xml
 <!--This can be inserted inside quote tags following the previous example if they are citations -->
 <lg xml:lang="en" type="ex:hunt-translation" xml:id="poem-title" rend="center">
    <lg xml:id="verse1"> 
    <l></l>
    <l></l>
    </lg>

    <lg xml:id="verse2"> 
    <l></l>
    <l></l>
    </lg> 
 <!--[…]-->
</lg>
```
Use the ```<q>``` tags when the quote is used inline within the paragraph. 
```xml
<q> text </q>
```

### Choice Elements
```xml 
<choice>
    <corr> </corr>
    <sic> </sic>
</choice>
```

OR

```xml 
<choice>
    <orig> </orig>
    <reg> </reg>
</choice>
```
[3.5 Simple Editorial Changes](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/CO.html#COED)

Choice elements allow flexibility in the viewing of a text's editorial interventions. The first example is used when the editor has corrected a word, where the corr element contains the corrected word, and the sic element contains the original word. The second is used when the editor has regularised a word, where the orig element contains the original word, and the reg element contains the regularised word.

### Hi Elements
```<hi rend="">``` (highlighted) marks a word or phrase as graphically distinct from the surrounding text, for reasons concerning which no claim is made. [TEI element hi](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-hi.html)

The hi tag always has a rend attribute, which is used to indicate a specific type of highlighting, which should be one of the following:
- bold
- italic
- underline
- smallcaps

### lg Elements
Verses containing more than one line should be encoded with  a ```<lg>``` tag containing an xml:lang attribute and a rend attribute. A @type attribute with the value "citation" is to be added if the verse is a citation and/or a @type attribute with the value "translation-hunt" if the verse is the translation of a passage provided by Hunt. Ex:
```xml
<lg xml:lang="" rend="" xml:id="some-text" corresp="#trans"> <!--The @xml:id will give an identifier so we can point back to it--> <!--the @corresp attribute points to the translation of the text if present in text-->
<l></l>
<l></l>
</lg>
<!-- Add the source as a note like explained in the Citation Elements section -->

<lg xml:lang="" rend="" type="translation-hunt" corresp="#some-text" xml:id="trans"> <!-- The @type attribute is optional.--> <!--The @xml:id will give an identifier so we can point back to it--> <!--the @corresp attribute points back to the source text of the translation if present in text-->
<l></l>
<l></l>
</lg>
```
