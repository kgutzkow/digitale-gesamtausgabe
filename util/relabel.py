import os

for basename, dirnames, filenames in os.walk('content'):
    for filename in filenames:
        if filename.endswith('.tei'):
            with open(os.path.join(basename, filename)) as in_f:
                data = in_f.read()
            # Fix main data
            #data = data.replace('Digitale edition', 'Herausgeber')
            #if '<tei:respStmt xml:id="MarkMichaelHall"' in data:
            #    data = data[:data.find('<tei:respStmt xml:id="MarkMichaelHall"')] + data[data.find('</tei:respStmt>', data.find('<tei:respStmt xml:id="MarkMichaelHall"')) + 15:]
            #while 'who="#MarkMichaelHall"' in data:
            #    start = data.rfind('<tei:change', 0, data.find('who="#MarkMichaelHall"'))
            #    end = data.find('</tei:change>', start) + 13
            #    data = data[:start] + data[end:]
            #while '<tei:resp>TEI transform</tei:resp>' in data:
            #    data = data[:data.find('<tei:resp>TEI transform</tei:resp>')] + data[data.find('<tei:resp>TEI transform</tei:resp>') + 34:]
            # Fix lexikon
            #data = data.replace('TEI transform', 'Herausgeber')
            # Fix Fassungen
            while 'Fassung' in data:
                start = data.rfind('>', 0, data.find('Fassung'))
                end = data.find('<', start)
                if end < data.find('<tei:text>'):
                    data = data[:start + 1] + '1.0' + data[end:]
                else:
                    break
            while 'Erstfassung' in data:
                start = data.rfind('>', 0, data.find('Erstfassung'))
                end = data.find('<', start)
                if end < data.find('<tei:text>'):
                    data = data[:start + 1] + '1.0' + data[end:]
                else:
                    break
            while 'TEI-Auszeichnung' in data:
                start = data.rfind('>', 0, data.find('TEI-Auszeichnung'))
                end = data.find('<', start)
                if end < data.find('<tei:text>'):
                    data = data[:start + 1] + '1.0' + data[end:]
                else:
                    break
            with open(os.path.join(basename, filename), 'w') as out_f:
                out_f.write(data)
