from pelican import signals


def startswith(a, b):
    """Tests whether a starts with b."""
    return a.startswith(b)


def install_extra_tests(generator):
    """Install the extra tests."""
    generator.env.tests['startswith'] = startswith


def register():
    """Register the extra tests installation"""
    signals.generator_init.connect(install_extra_tests)
