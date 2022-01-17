# Gutzkow - Digitale Gesamtausgabe

[![pipeline status](https://gitlab.informatik.uni-halle.de/gutzkow/digitale-gesamtausgabe/badges/master/pipeline.svg)](https://gitlab.informatik.uni-halle.de/gutzkow/digitale-gesamtausgabe/commits/master)

## Softwareabhängigkeiten

* `Node.js <https://nodejs.org>`_
* `poetry <https://python-poetry.org>`_
* `NPM <https://www.npmjs.com/>`_

## Data Preprocessing

Quell HTML Text in TEI Umwandeln:

.. sourcecode:: console

  $ python util/text-body-extract.py source.fodt config.json body-output.tei

## TEI Validierung

Validiert alle TEI Dateien gegen eine Reihe von Regeln.

.. sourcecode:: console

  $ python util/validate-tei.py
