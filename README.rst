Gutzkow - Digitale Gesamtausgabe
================================

Softwareabhängigkeiten
++++++++++++++++++++++

* `Node.js <https://nodejs.org>`_
* `pipenv <https://docs.pipenv.org>`_

Installation
++++++++++++

Voll-automatische Installation und Generierung:

.. sourcecode:: console

  $ ./build.sh

Manuelle Installation
---------------------

.. sourcecode:: console

  $ npm install
  $ pipenv --three install

Manuelle Generierung
--------------------

In zwei separaten Terminals die folgenden Befehle ausführen

.. sourcecode:: console

  $ gulp watch

.. sourcecode:: console

  $ pipenv shell
  $ pelican -o output -d -r content

Data Preprocessing
++++++++++++++++++

Quell HTML Text in TEI Umwandeln:

.. sourcecode:: console

  $ python util/xslt-transform.py quelle util/extract-main-text-as-tei.xslt ziel --input-html

Die folgenden manuellen Schritte müssen nach der Transformation ausgeführt werden:

  * Leere Absätze entfernen
  * Absätze des Attributionsbereichs entfernen
  * TEI Header ausfüllen
  * ``about`` Attribute aktualisieren, "urn:aX" durch "urn:hierarchie:aX" ersetzen
  * Dem ``body`` das ``about`` Attribut mit voller Hierarchie-URN ausfüllen
