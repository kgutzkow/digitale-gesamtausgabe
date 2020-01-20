import os

for basepath, _, filenames in os.walk('content'):
    for filename in filenames:
        if filename.endswith('.tei'):
            with open(os.path.join(basepath, filename)) as in_f:
                data = in_f.read()
                if 'Dieses Werk ist zur Zeit nur als PDF verfügbar.' not in data:
                    if os.path.exists(os.path.join(basepath, filename.replace('.tei', '.pdf'))):
                        os.unlink(os.path.join(basepath, filename.replace('.tei', '.pdf')))
