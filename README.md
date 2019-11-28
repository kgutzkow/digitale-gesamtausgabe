# Gutzkow - Digitale Gesamtausgabe

[![pipeline status](https://gitlab.informatik.uni-halle.de/gutzkow/digitale-gesamtausgabe/badges/master/pipeline.svg)](https://gitlab.informatik.uni-halle.de/gutzkow/digitale-gesamtausgabe/commits/master)

## Softwareabhängigkeiten

* `Node.js <https://nodejs.org>`_
* `pipenv <https://docs.pipenv.org>`_
* `Yarn <https://yarnpkg.com>`_

## Installation

Voll-automatische Installation und Generierung:

.. sourcecode:: console

  $ ./build.sh

### Manuelle Installation

.. sourcecode:: console

  $ yarn install
  $ pipenv --three install

### Manuelle Generierung

In zwei separaten Terminals die folgenden Befehle ausführen

.. sourcecode:: console

  $ gulp watch

.. sourcecode:: console

  $ pipenv shell
  $ pelican -o output -d -r content

## Preview Generierung

Wenn eine Datei ``branches.txt`` existiert, dann generiert das ``build.js`` Skript für jeden Branch der darin
aufgeführt wird eine Kopie unter ``output/preview/{branch-name}``.

## Data Preprocessing

Quell HTML Text in TEI Umwandeln:

.. sourcecode:: console

  $ python util/text-body-extract.py source.fodt config.json body-output.tei

## TEI Validierung

Validiert alle TEI Dateien gegen eine Reihe von Regeln.

.. sourcecode:: console

  $ python util/validate-tei.py
