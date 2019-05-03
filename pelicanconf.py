#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = 'Mark M Hall'
SITENAME = 'Karl Gutzkow'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('eHumanities@Martin-Luther-Universität Halle-Wittenberg', 'https://blogs.urz.uni-halle.de/ehumanities/'),)

DEFAULT_PAGINATION = 6

DISPLAY_CATEGORIES_ON_MENU = False

PLUGIN_PATHS = ['./']
PLUGINS = ['tei_reader',
           'pelican_page_order',
           'pelican_page_hierarchy']

STATIC_PATHS = ['pages']

THEME = './theme'

GENERATION_DATE = datetime.now()

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

TAXONOMY = (
    ('I. Erzählerische Werke', 'erzaehlerische-werke', (
        ('1. Briefe eines Narren an eine Närrin', 'briefe-eines-narren-an-eine-naerrin', ()),
        ('3. Novellen', 'novellen', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
        )),
        ('4. Wally die Zweiflerin', 'wally-die-zweiflerin', ()),
        ('7. Kleine erzählerische Werke I', 'kleine-erzaehlerische-werke-i', (
            ('Imagina Unruh', 'imagina-unruh', ()),
        )),
        ('10. Die Diakonissin', 'die-diakonissin', ()),
        ('11. Der Zauberer von Rom', 'der-zauberer-von-rom', (
            ('Erstes Buch', 'erstes-buch', ()),
            ('Zweites Buch', 'zweites-buch', ()),
            ('Drittes Buch', 'drittes-buch', ()),
            ('Viertes Buch', 'viertes-buch', ()),
            ('Fünftes Buch', 'fuenftest-buch', ()),
            ('Sechstes Buch', 'sechstes-buch', ()),
            ('Siebentes Buch', 'siebentes-buch', ()),
            ('Achtes Buch', 'achtes-buch', ()),
            ('Neuntes Buch', 'neuntes-buch', ()),
        )),
        ('17. Die neuen Serapionsbrüder', 'die-neuen-serapionsbrueder', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
            ('Dritter Band', 'dritter-band', ())
        ))
    )),
    ('II. Dramatische Werke', 'dramatische-werke', (
        ('1. Marino Falieri', 'marino-falieri', ()),
		('1. Hamlet in Wittenberg', 'hamlet-in-wittenberg', ()),
		('1. Nero', 'nero', ()),
		('1. König Saul', 'koenig-saul', ()),
		('2. Richard Savage. Oder: Der Sohn einer Mutter', 'richard-savage', ()),
		('2. Werner. Oder: Herz und Welt', 'werner', ()),
		('2. Die Gräfin Esther', 'die-graefin-esther', ()),
		('2. Patkul', 'patkul', ())
    )),
    ('III. Schriften zur Politik und Gesellschaft', 'schriften-zur-politik-und-gesellschaft', (
        ('3. Die Zeitgenossen', 'die-zeitgenossen', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
        )),
        ('Säkularbilder (1846)', 'saekularbilder-1846', (
            ('Vorwort', 'vorwort', ()),
        )),
        ('Säkularbilder (1875)', 'saekularbilder-1875', (
            ('Vorwort', 'vorwort', ()),
        )),
        ('6. Verstreute Schriften zur Geschichte und Politik', 'verstreute-schriften-zur-geschichte-und-politik', (
            ('Zur Arnim-Affaire', 'zur-arnim-affaire', ()),
        )),
        ('8. Zum Gesellschaftsleben - Skizzen und Zeitfragen', 'zum-gesellschaftsleben-skizzen-und-zeitfragen', (
            ('Studien über das Negligé', 'studien-ueber-das-neglige', ()),
			('Naturgeschichte der deutschen Kameele', 'naturgeschichte-der-deutschen-kameele', ()),
			('Eine Criminalerinnerung', 'eine-criminalerinnerung', ()),
			('Die zoologischen Gärten', 'die-zoologischen-gaerten', ()),
			('Der Papierkorb', 'der-papierkorb', ())
        ))
    )),
    ('IV. Schriften zur Literatur und zum Theater', 'schriften-zur-literatur-und-zum-theater', (
        ('2. Beiträge zur Geschichte der neuesten Literatur', 'beitraege-zur-geschichte-der-neuesten-literatur', (
            ('Literarische Industrie', 'literarische-industrie', ()),
        )),
        ('5. Börne\'s Leben', 'boerne-s-leben', ()),
        ('6. Literaturkritik', 'literaturkritik', (
            ('6.1. Rezensionen und literaturkritische Essays', 'rezensionen-und-literaturkritische-essays', (
                ('[Vorwort zum "Literatur-Blatt" des "Phönix"]', 'vorwort-zum-literatur-blatt-des-phoenix', ()),
			    ('Dichter und ihre Gesellen. Novelle von Jos. Freih. von Eichendorff', 'dichter-und-ihre-gesellen-novelle-von-jos-freih-von-eichendorfff', ()),
			    ('Schriften in bunter Reihe. Herausgegeben von Theodor Mundt', 'schriften-in-bunter-reihe-herausgegeben-von-theodor-mundt', ()),
			    ('Der Salon von H. Heine. Zweiter Theil', 'der-salon-von-h-heine-zweiter-theil', ()),
			    ('Menzel\'s Geist der Geschichte', 'menzel-s-geist-der-geschichte', ()),
			    ('Bulwer\'s Pilger am Rhein. Aus dem Englischen von le Petit. Mit Stahlstichen', 'bulwer-s-pilger-am-rhein-aus-dem-englischen-von-le-petit-mit-stahltischen', ()),
			    ('Wolfgang Menzel und der deutsche Tiersparti', 'wolfgang-menzel-und-der-deutsche-tiersparti', ()),
			    ('Madonna. Unterhaltungen mit einer Heiligen. Von Th. Mundt', 'madonna-unterhaltungen-mit-einer-heiligen-von-th-mundt', ()),
			    ('Liebesbriefe. Novelle von Heinrich Laube', 'liebesbriefe-novelle-von-heinrich-laube', ()),
			    ('Das Haus Düsterweg. Eine Geschichte aus der Gegenwart. Von Wilibald Alexis', 'das-haus-duesterweg-eine-geschichte-aus-der-gegenwart-von-wilibald-alexis', ()),
			    ('Danton\'s Tod, von Georg Büchner', 'danton-s-tod-von-georg-buechner', ()),
			    ('Lelia. Ein Roman nach dem Französischen des Georges Sand. Von A. Braun', 'lelia-ein-roman-nach-dem-franzoesischen-des-georges-sand-von-a-braun', ()),
			    ('Zur neuesten Literatur, von L. Wienbarg', 'zur-neuesten-literatur-von-l-wienbarg', ()),
			    ('Eine Quarantäne im Irrenhause, von F. G. Kühne', 'eine-quarantaene-im-irrenhaus-von-f-g-kuehne', ()),
			    ('Zwei neue Dramen von Grabbe', 'zwei-neue-dramen-von-grabbe', ()),
			    ('Heine über den Denunzianten', 'heine-ueber-den-denunzianten', ()),
			    ('Laubes neue Reisenovellen', 'laubes-neue-reisenovellen', ()),
			    ('Theater-Roman. Von August Lewald. Erster und zweiter Band', 'theater-roman-von-august-lewald-erster-und-zweiter-band', ()),
			    ('Theater-Roman. Von August Lewald. Dritter, vierter und fünfter Band', 'theater-roman-von-august-lewald-dritter-vierter-und-fuenfter-band', ()),
			    ('Diese Kritik gehört Bettinen', 'diese-kritik-gehoert-bettinen', ()),
			    ('Was sollen wir lesen?', 'was-wollen-wir-lesen', ()),
			    ('Die neuen Dorf- und Bauern-Novellen', 'die-neuen-dorf-und-bauern-novellen', ()),
			    ('Vierzig Jahre von Karl von Holtei', 'vierzig-jahre-von-karl-von-holtei', ()),
			    ('Josef Rank', 'josef-rank', ()),
			    ('Winke für die Lesewelt', 'winke-fuer-die-lesewelt', ()),
			    ('Ein preußischer Roman [Fanny Lewald, "Prinz Louis Ferdinand"]', 'ein-preussischer-roman-fanny-lewald-prinz-louis-ferdinand', ()),
			    ('Ein neuer Roman von Wilibald Alexis', 'ein-neuer-roman-von-wilibald-alexis', ()),
			    ('Berthold Auerbach\'s neueste Dorfgeschichten', 'berthold-auerbach-s-neueste-dorfgeschichten', ()),
			    ('Vom deutschen Parnaß', 'vom-deutschen-parnass', ()),
			    ('Ein neuer Roman [Gustav Freytag, "Soll und Haben"]', 'ein-neuer-roman-gustav-freytag-soll-und-haben', ()),
			    ('Die Leute von Seldwyla', 'die-leute-von-seldwyla', ()),
			    ('Die "realistischen" Erzähler', 'die-realistischen-erzaehler', ()),
			    ('Vom Berliner Büchertisch. I - IV', 'vom-berliner-buechertisch-i-iv', ())
            )),
            ('6.2. Schriften zur Literatur', 'schriften-zur-literatur', (
                ('Der Hofrath Tieck', 'der-hofrath-tieck', ()),
			    ('Der deutsche Roman', 'der-deutsche-roman', ()),
			    ('Theodor Mundt, Willibald Alexis und die Pommersche Dichterschule, oder über einige literar-historische Symptome', 'theodor-mundt-willibald-alexis-und-die-pommersche-dichterschule-oder-ueber-einige-literar-historische-symptome', ()),
			    ('Der historische Roman', 'der-historische-roman', ()),
			    ('Börne gegen Heine', 'boerne-gegen-heine', ()),
			    ('Vergangenheit und Gegenwart', 'vergangenheit-und-gegenwart', ()),
			    ('Herr Heine und sein Schwabenspiegel', 'herr-heine-und-sein-schwabenspiegel', ()),
			    ('Ein Besuch bei Bettina', 'ein-besuch-bei-bettina', ()),
			    ('Der Geist des Ortes', 'der-geist-des-ortes', ()),
			    ('Der Tages-Cours unserer Classiker', 'der-tages-cours-unserer-classiker', ()),
			    ('Weltberühmt oder gar nicht', 'weltberuehmt-oder-gar-nicht', ()),
			    ('Unsere gegenwärtige Literatur', 'unsere-gegenwaertige-literatur', ()),
			    ('Ludwig Tieck', 'ludwig-tieck', ()),
			    ('Ein deutsches Dichterleben', 'ein-deutsches-dichterleben', ()),
			    ('[Redaktionelle Anmerkung zu Hieronymus Lorm, "Charles Dickens"]', 'redaktionelle-anmerkung-zu-hieronymus-lorm-charles-dickens', ()),
			    ('Tendenzpoesie', 'tendenzpoesie', ()),
			    ('Der Roman und die Arbeit', 'der-roman-und-die-arbeit', ()),
			    ('Realismus und Idealismus', 'realismus-und-idealismus', ()),
			    ('Die Baronin von Gravenreuth, geb. Gräfin Hirschberg, und mein "Plagiat" an ihrer Lebensbeschreibung', 'die-baronin-von-gravenreuth-geb-graefin-hirschberg-und-main-plagiat-an-ihrer-lebensbeschreibung', ()),
			    ('Theodor Mundt', 'theodor-mundt', ()),
			    ('Die Familie Büchner', 'die-familie-buechner', ()),
			    ('Zum Gedächtniß Wilhelm Härings', 'zum-gedaechtniss-wilhelm-haerings', ()),
			    ('Wolfgang Menzel und das "junge Deutschland"', 'woflgang-menzel-und-das-junge-deutschland', ()),
			    ('Zur deutschen Rechtschreibung', 'zur-deutschen-rechtschreibung', ()),
			    ('Deutsche Classiker-Philologie', 'deutsche classiker-philologie', ()),
			    ('Das Feuilleton', 'das-feuilleton', ())
            ))
        )),
        ('7. Schriften zum Buchhandel und zur literarischen Praxis', 'schriften-zum-buchhandel-und-zur-literarischen-praxis', (
            ('Rahmenbedingungen schriftstellerischer und verlegerischer Produktion', 'rahmenbedingungen-schriftstellerischer-und-verlegerischer-production', (
                ('Autor- und Verlagsrecht', 'autor-und-verlagsrecht', (
                    ('In Sachen des Nachdrucks', 'in-sachen-des-nachdrucks', ()),
			        ('[Kampf gegen den Nachdruck]', 'kampf-gegen-den-nachdruck', ()),
			        ('[Deduktion des Eigentumsrechts der Schriftsteller]', 'deduktion-des-eigentumsrechts-der-schriftsteller', ()),
			        ('[Nachdruck unter den Augen des Bundestages]', 'nachdruck-unter-den-augen-des-bundestages', ()),
			        ('Das königl. sächsische Gesetz zur Sicherstellung des literarischen und artistischen Eigenthums', 'das-koenigl-saechsische-gesetz-zur-sicherstellung-des-literarischen-und-artistischen-eigenthums', ()),
			        ('[Eigentumsrecht an Dramen]', 'eigentumsrecht-an-dramen', ()),
			        ('Der Birch-Pfeiffer-Auerbach\'sche Handel', 'der-birch-pfeiffer-auerbach-sche-handel', ()),
			        ('Bedenken gegen ein Gutachten des leipziger Sachverständigenvereins', 'bedenken-gegen-ein-gutachten-des-leipziger-sachverstaendigenvereins', ()),
			        ('Das geistige Eigenthum', 'das-geistige-eigenthum', ()),
			        ('Internationales Autor- und Verlagsrecht', 'internationales-autor-und-verlagsrecht', ()),
			        ('In Sachen des geistigen Eigenthums', 'in-sachen-des-geistigen-eigenthums', ())
                )),
                ('Der soziale Status des Schriftstellers', 'der-soziale-status-des-schriftstellers', (
                    ('Hitzig über die Existenz der Schriftsteller', 'hitzig-ueber-die-existenz-der-schriftsteller', ()),
			        ('[Kampf gegen die schlechte Schriftstellerei]', 'kampf-gegen-die-schlechte-schriftstellerei', ()),
			        ('[Beschimpfung des Schriftstellerstandes]', 'beschimpfung-des-schriftstellerstandes', ())
                )),
                ('Zensur und Pressepolitik', 'zensur-und-pressepolitik', (
                    ('[Allgemeines Pressgesetz des Bundestages]', 'allgemeines-pressgesetz-des-bundestages', ()),
    			    ('Ueber die Gesetzgebung der Presse', 'ueber-die-gesetzgebung-der-presse', ()),
	    		    ('[Zensur in Frankfurt am Main]', 'zensur-in-frankfurt-am-main', ()),
		    	    ('[Berliner Zensur streicht Namen jungdeutscher Autoren in Journalen]', 'berliner-zensur-streicht-namen-jungdeutscher-autoren-in-journalen', ()),
			        ('[Eduard Hitzig und die "Preßzeitung"]', 'eduard-hitzig-und-die-presszeitung', ()),
			        ('[Österreichische Zensur]', 'oesterreichische-zensur', ()),
    			    ('[Neues Pressgesetz in Berlin]', 'neues-pressgesetz-in-berlin', ()),
	    		    ('[Pressgesetz und Pressefreiheit]', 'pressgesetz-und-pressefreiheit', ()),
		    	    ('[Verbot von Jungs "Literaturblatt"]', 'verbot-von-jungs-literaturblatt', ()),
			        ('[Konflikt zwischen den Verlegern Friedrich Fleischer und Baron von Cotta]', 'konflikt-zwischen-den-verlegern-friedrich-fleischer-und-baron-von-cotta', ()),
    			    ('[Verbot der Verlagserzeugnisse von Hoffmann und Campe in Preußen]', 'verbot-der-verlagserzeugnisse-von-hoffmann-und-campe-in-preussen', ()),
	    		    ('[Verbot der Leipziger Allgemeinen Zeitung]', 'verbot-der-leipziger-allgemeinen-zeitung', ()),
		    	    ('[Gutzkows Schriften und Dramatische Werke von Berlins Zensurbehörde abgewiesen]', 'gutzkows-schriften-und-dramatische-werke-von-berlins-zensurbehoerde-abgewiesen', ()),
			        ('Die Freiheit der Zerrbilder', 'die-freiheit-der-zerrbilder', ()),
			        ('Die Furcht vor der Preßfreiheit', 'die-furcht-vor-der-pressfreiheit', ()),
    			    ('Nothwendiger Nachtrag zu dem in Nr. 38 enthaltenen Aufsatze: Die Furcht vor der Preßfreiheit', 'notwendiger-nachtrag-zu-dem-in-nr-38-enthaltenen-aufsatze-die-furcht-vor-der-pressfreiheit', ()),
	    		    ('An die löbliche Redaktion der Zeitung für die elegante Welt', 'an-die-loebliche-redaktion-der-zeitung-fuer-die-elegante-welt', ()),
		    	    ('[Leipziger Literaturpöbel gegen Gutzkows Furcht vor der Preßfreiheit]', 'leipziger-literaturpoebel-gegen-gutzkows-furcht-vor-der-pressfreiheit', ()),
			        ('[Fleischer und Cotta]', 'fleischer-und-cotta', ()),
			        ('Der Ehrgeiz als Censor und eine Erziehung der Geister', 'der-ehrzeigt-als-censor-und-eine-erziehung-der-geister', ())
                ))
            )),
            ('Buchmarkt, verlegerische Strategien und buchhändlerischer Vertrieb', 'buchmarkt-verlegerische-strategien-und-buchhaendlerischer-vertrieb', (
                ('Buchproduktion und literarische Moden', 'buchproduktion-und-literarische-moden', (
                    ('Die Deutschen Uebersetzungsfabriken', 'die-deutschen-uebersetzungsfabriken', ()),
			        ('[Katalog des Verlags B. F. Voigt]', 'katalog-des-verlags-b-f-voigt', ()),
			        ('Der B. F. Voigt\'sche Verlag in Weimar', 'der-b-f-voigt-sche-verlag-in-weimar', ()),
			        ('[Krise der französischen Belletristik und Jules Janin]', 'krise-der-franzoesischen-belletristik-und-jules-janin', ()),
			        ('Eine neue deutsche Original-Roman-Bibliothek', 'eine-neue-deutsche-original-roman-bibliothek', ()),
			        ('Das Kaufen von Büchern', 'das-kaufen-von-buechern', ()),
			        ('Der deutsche Gänsekiel', 'der-deutsche-gaensekiel', ()),
			        ('Volk und Publicum', 'volk-und-publicum', ()),
			        ('Unsere Bücherfabrikation', 'unsere-buecherfabrikation', ())
                )),
                ('Populäre Lesestoffe und Illustrationen', 'populaere-lesestoffe-und-illustrationen', (
                    ('Der neue Don-Quixote mit Holzschnitten', 'der-neue-don-quixote-mit-holzschnitten', ()),
			        ('[Neue Prachtausgabe des "Don Quixote" und von "Tausend und Einer Nacht"]', 'eine-neue-prachtausgabe-des-don-quixote-und-von-tausend-und-einer-nacht', ()),
			        ('Deutsche Holzschnitte', 'deutsche-holzschnitte', ()),
			        ('Illustration und Volksverdummung', 'illustration-und-volksverdummung', ())
                )),
                ('Buchhandelsusancen und Buchvertrieb', 'buchhandelsusancen-und-buchvertrieb', (
                    ('Ueber eine Reform des deutschen Buchhandels', 'ueber-eine-reform-des-deutschen-buchhandels', ()),
			        ('Ueber Preisherabsetzungen im Buchhandel', 'ueber-preisherabsetzungen-im-buchhandel', ()),
			        ('Verfall des deutschen Buchhandels', 'verfall-des-deutschen-buchhandels', ()),
			        ('Die Buchhändlermesse', 'die-buchhaendlermesse', ()),
			        ('Der deutsche Buchhandel', 'der-deutsche-buchhandel', ()),
			        ('Eisenbahn-Bibliotheken', 'eisenbahn-bibliotheken', ()),
			        ('Eine Eisenbahn-Bibliothek', 'eine-eisenbahn-bibliothek', ()),
			        ('Wovon leben die deutschen Buchhändler?', 'wovon-leben-die-deutschen-buchhaendler', ())
                )),
                ('Journalistische Praxis und Presse', 'jouirnalistische-praxis-und-presse', (
                    ('H. Brockhaus, P. Lyser und die kritischen Zahlen um Leipzig', 'h-brockhaus-p-lyser-und-die-kritischen-zahlen-um-leipzig', ()),
			        ('Die Journale Hamburgs', 'die-journale-hamburgs', ()),
			        ('Soll sich die Theaterkritik bestechen lassen?', 'soll-sich-die-theaterkritik-bestechen-lassen', ()),
			        ('Statistik des Absatzes deutscher Zeitschriften und Zeitungen', 'statistik-des-absatzes-deutscher-zeitschriften-und-zeitungen', ()),
			        ('Zeitungslügen', 'zeitungsluegen', ()),
			        ('Die gewandten Federn', 'die-gewandten-federn', ()),
			        ('Ueber deutsche Publicistik', 'ueber-deutsche-publicistik', ()),
			        ('Das Publicum und die Zeitschriften', 'das-publicum-und-die-zeitschriften', ()),
			        ('Buchhandel und Kritik', 'buchhandel-und-kritik', ()),
			        ('Literarischer Augiasstall', 'literarischer-augiasstall', ())
                ))
            ))
        )),
        ('9. Theaterkritiken', 'theaterkritiken', (
            ('[Über Dramen Edward Lytton Bulwers]', 'ueber-dramen-edward-lytton-bulwers', ()),
        )),
        ('10. Dramaturgische Schriften - Zum Bühnenleben - Oper und Musik', 'dramaturgische-schriften-zum-buehnenleben-oper-und-musik', (
            ('[Franz Liszt in Hamburg]', 'franz-list-in-hamburg', ()),
            ('Richard Wagner\'sche Musik', 'richard-wagner-sche-musik', ())
        ))
    )),
    ('VI. Reiseliteratur', 'reiseliteratur', (
        ('1. Briefe aus Paris', 'briefe-aus-paris', ()),
        ('3. Berliner Eindruecke', 'berliner-eindruecke', (
            ('Berliner Eindrücke', 'berliner-eindruecke', ()),
			('Eine Woche in Berlin', 'eine-woche-in-berlin', ()),
			('Eine nächtliche Unterkunft', 'eine-naechtliche-unterkunft', ())
        ))
    )),
    ('VII. Autobiographische Schriften', 'autobiographische-schriften', (
        ('Rückblicke auf mein Leben (Zeitschriftenfassung)', 'rueckblicke-auf-mein-leben-zeitschriftenfassung', ()),
        ('2. Rückblicke auf mein Leben', 'rueckblicke-auf-mein-leben', ()),
        ('3. Kleine autobiographische Schriften und Memorabilien', 'kleine-autobiographische-schriften-und-memorabilien', (
            ('Julius Max Schottky, Professor', 'julios-max-schottky-professor', ()),
			('Eine männliche Gräfin Hahn-Hahn', 'eine-maennliche-graefin-hahn-hahn', ()),
			('Onkel Spener', 'onkel-spener', ())
        ))
    ))
)
