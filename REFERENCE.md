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
        <bibl><author>name  of author</author><title level="a">title</title><ref target="url"/></bibl>
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
For a change of language within a line use:
<span xml:lang="latin">Mare Liberum</span>
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
### title tag
The title tag includes an attribute level. Refer to the following reference to choose the right value:
Legal values are:	
- a (analytic) the title applies to an analytic item, such as an article, poem, or other work published as part of a larger item.
- m (monographic) the title applies to a monograph such as a book or other item considered to be a distinct publication, including single volumes of multi-volume works
- j (journal) the title applies to any serial or periodical publication such as a journal, magazine, or newspaper
- s (series) the title applies to a series of otherwise distinct publications such as a collection
- u (unpublished) the title applies to any unpublished material (including theses and dissertations unless published by a commercial press)
Example : ```<title level="a">Sonnet 12</title>```

### persName
Examples
```xml
<!--first occurrence of many-->
<persName key="Robert Boyle" ref="http://www.wikidata.org/entity/Q43393" cert="medium" type="real" xml:id="robertBoyle">Robert Boyle</persName> 
<!--other occurrences of same key-->
<persName key="Robert Boyle" type="real" corresp="#robertBoyle">Mr. Boyle</persName>

<!--unique occurrence-->
<persName key="King James VI of Scotland and I of England (1566–1625)" ref="http://www.wikidata.org/entity/Q118876108" cert="high" type="real">King James</persName>

<!-- for families-->
<persName role="family" key="Sydneys, Earls of Leicester">Sydneys, Earls of Leicester</persName>

```

### placeName
Indicate country in @corresp attribute for the placeName tag even when the key contains the name of a country.

Example:

```xml
<placeName key="Siena" corresp="Italy" ref="http://www.wikidata.org/entity/Q2751" cert="high">the City of Sienna</placeName>

To distinguish between types of places the @type attribute can be used:
Country
Continent
City : Includes cities and towns
Street
Region : for regions and islands. These regions can be regions of a country or unspecified places within a city, for example.
Physical : for natural features like mountains, lakes, forest etc.
Pub : for pubs that one drinks at
Theatre
Address : for addresses such as those found at the end of tracts such as a publsiher's
Road : for any place involved with travel
Landmark : for physical monuments including bridges
Commerce : for any place invloved with exchange like shops and inns
Building : for buildings, churches and hospitals
Prison

Fictional
```

### Quote elements
To indicate something in quotation marks
```xml
For text in quotation elements the <q> </q> element should be used around the word or phrase containing the qutation marks with the quotation marks removed.
The quote tag includes an attribute element. <q type=""> These can also be contained int their own tags.
spoken : for direct speech or dialogue
thought : for a person/character's thoughts
written : from written source material
soCalled : (so called) contains a word or phrase for which the author or narrator indicates a disclaiming of responsibility, for example by the use of scare quotes or italics.
foreign : identifies a word or phrase as belonging to some language other than that of the surrounding text
distinct : identifies any word or phrase which is regarded as linguistically distinct, for example as archaic, technical, dialectal, non-preferred, etc., or as forming part of a sublanguage.
term : (term) contains a single-word, multi-word, or symbolic designation which is regarded as a technical term.
emph : (emphasized) marks words or phrases which are stressed or emphasized for linguistic or rhetorical effect.
mentioned : marks words or phrases mentioned, not used
```

