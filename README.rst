Gutzkow - Digitale Gesamtausgabe
================================

Softwareabhängigkeiten
++++++++++++++++++++++

* `Node.js <nodejs.org>`_
* `pipenv <pipenv.org>`_

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
