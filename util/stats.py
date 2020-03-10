import os

total = 0
transcribed = 0

for basepath, dirs, filenames in os.walk('content'):
    for filename in filenames:
        if filename.endswith('.tei'):
            total = total + 1
            with open(os.path.join(basepath, filename)) as in_f:
                data = in_f.read()
                if 'Dieses Werk ist zur Zeit nicht verfügbar' not in data \
                        and 'Dieses Werk ist zur Zeit nicht online verfügbar' not in data \
                        and 'Dieses Werk ist zur Zeit nur als PDF verfügbar' not in data:
                    transcribed = transcribed + 1

print('{0} of {1} ({2:.2f}%)'.format(transcribed, total, 100 / total * transcribed))
