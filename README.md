# Layout Analysis Dataset with SegmOnto (LADaS)

[![DOI](https://zenodo.org/badge/726002822.svg)](https://zenodo.org/doi/10.5281/zenodo.10682623) [![License: CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)

LADaS, created by the [ALMANaCH team-project](https://almanach.inria.fr/index-en.html) at Inria,
continued in partnership with other researchers, is a multidocuments diachronic layout analysis 
dataset. This dataset includes:

- Monographs from the Bibliothèque Nationale de France (17th century - today);
- PhD Thesis, in various fields (not only STEM, 20th-21st century);
- Selling Catalogs (for manuscripts and art pieces), in various fields (18th-20th century);
- Noisy digitization (with fingers for example, 20th-21st century);
- Academic papers (mostly Humanities and Social Sciences) (19th-21st century);
- Magazines about technologies and video games, from 1920s to 2010;
- Misc stuff found here and there.

The data are in YoloV8 txt format (class center_x center_y width height).

The script in document is mostly Latin script, and language is mostly French with some representation of the main
western academic languages.

### Annotation

Label Annotation have been conducted using the [SegmOnto](https://segmonto.github.io/) vocabulary. 
An annotation guide is available [here](AnnotationGuide.md).

### More details about some subsets

![./figures/corpus.png](./figures/corpus.png)

*Last update of the plot: 15/12/2023*

## Structure

The data can be found in `./data`. Each subset is present in its own subset folder if you want to train cross-genre.

A script, `collate.sh` allows for having a single directory with train/dev/test folders for YoloV8 training.

## Partners
|Funding|Project|Comment|
|---|---|---|
|<img src="figures/inria.png" width="100"/>|<img src="figures/colaf.png" width="100"/>|Originally established and funded as part of the DEFI COLaF (2023–2027).|
|<img src="figures/eu.webp" width="100"/>|<img src="figures/atrium.png" width="100"/>|Funded by the European Union under Grant Agreement n. 101132163. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union. Neither the European Union nor the granting authority can be held responsible for them. |
|<img src="figures/fns.png" width="100"/>|The Geographic Horizon of writers|Funded by FNS-Spark project [N°220833](https://data.snf.ch/grants/grant/220833). |

## Licence

![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115525743-a78d2400-a28f-11eb-8e45-4b6e3265a527.png)

## Citation

See the CITATION.CFF file

## Contact

Thibault Clérice ( th[a-z]+.cle[a-z]+ [at] inria.fr)
