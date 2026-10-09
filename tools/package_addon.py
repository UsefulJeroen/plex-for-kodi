"""Build an installable Kodi zip from runtime files only."""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


def build(output):
    root = Path(__file__).resolve().parents[1]
    addon = ET.parse(root / 'addon.xml').getroot()
    addon_id, version = addon.attrib['id'], addon.attrib['version']
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    target = output / '{}-{}.zip'.format(addon_id, version)
    files = [p for p in root.iterdir() if p.is_file() and
             (p.suffix == '.py' or p.name in
              ('addon.xml', 'LICENSE.txt', 'changelog.txt', 'fanart.png', 'icon2.png',
               'pm4k_cache_template.xml', 'path_mapping.example.json'))]
    for folder in ('lib', 'resources'):
        files.extend(p for p in (root / folder).rglob('*') if p.is_file() and
                     '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.pyo'))
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, '{}/{}'.format(addon_id, path.relative_to(root).as_posix()))
    with ZipFile(target) as archive:
        bad_file = archive.testzip()
        if bad_file:
            raise RuntimeError('Corrupt archive member: ' + bad_file)
        for name in ('addon.xml', 'lib/community.py', 'lib/windows/community.py', 'LICENSE.txt'):
            if '{}/{}'.format(addon_id, name) not in archive.namelist():
                raise RuntimeError('Missing runtime file: ' + name)
    print(target)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    build(parser.parse_args().output)
