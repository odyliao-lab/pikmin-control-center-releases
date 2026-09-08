"""Public metadata checks only. Never builds/signs APKs or accesses devices."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.request

REPO = 'odyliao-lab/pikmin-control-center-releases'
LEGACY = (49, '24af6067f636f895f23c5661246f178ce7640438c23d3c3a6538a5c1a208f0c1')
CERT = '9080c5d8c9a138a3a8eb42ec65755cf2abd64b881a7bf398feabe3547b934a7e'

def parse(text):
    result = {}
    for line in text.splitlines():
        if not line or '=' not in line:
            raise ValueError('Invalid metadata line')
        key, value = line.split('=', 1)
        if key in result or not value:
            raise ValueError('Duplicate/empty field')
        result[key] = value
    if set(result) != set('schema packageName versionName versionCode apkUrl sha256 size minSdk summary compatibility'.split()):
        raise ValueError('Unexpected metadata fields')
    assert result['schema'] == '1' and result['packageName'] == 'dev.ody.pikmincontrol'
    assert re.fullmatch(r'\d+\.\d+\.\d+', result['versionName'])
    assert re.fullmatch('[a-f0-9]{64}', result['sha256'])
    for field in ['versionCode', 'size', 'minSdk']:
        assert re.fullmatch('[0-9]+', result[field])
    assert 0 < int(result['versionCode']) <= 2147483647
    assert 0 < int(result['size']) <= 104857600 and 28 <= int(result['minSdk']) <= 100
    assert len(result['summary']) <= 500 and len(result['compatibility']) <= 180
    v = result['versionName']
    assert result['apkUrl'] == f'https://github.com/{REPO}/releases/download/v{v}/pikmin-control-center-{v}.apk'
    return result

def fetch(url, limit):
    headers = {'User-Agent': 'Control-Center-release-validation'}
    if url.startswith('https://api.github.com/') and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        data = response.read(limit + 1)
        assert len(data) <= limit, 'Response exceeds limit'
        return data

def main():
    raw = Path('update.properties').read_text(encoding='utf-8')
    info = parse(raw)
    if '--self-test' in sys.argv:
        for bad in [raw + 'schema=1\n', raw.replace('https://github.com/', 'https://example.com/'),
                    raw.replace('versionCode=49', 'versionCode=-1'), raw.replace('sha256=', 'unknown=')]:
            # Version-independent mutation for future releases.
            if bad == raw:
                bad = re.sub(r'versionCode=\d+', 'versionCode=-1', raw)
            try:
                parse(bad)
            except (ValueError, AssertionError):
                continue
            raise AssertionError('Invalid metadata accepted')
        print('PASS: parser and four negative cases')
        return
    allowed = {'README.md', 'update.properties', '.github/workflows/release-index.yml', 'scripts/verify-index.py'}
    tracked = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()
    assert set(tracked) <= allowed, 'Unexpected file in public repository'
    base = os.environ.get('BASE_SHA', '')
    if base:
        assert re.fullmatch('[a-f0-9]{40}', base)
        old = parse(subprocess.check_output(['git', 'show', f'{base}:update.properties'], text=True))
        assert info == old or int(info['versionCode']) > int(old['versionCode']), 'Same-code replacement or downgrade'
    release = json.loads(fetch(f'https://api.github.com/repos/{REPO}/releases/tags/v{info["versionName"]}', 1048576))
    assert not release['draft'] and not release['prerelease']
    assert release.get('immutable') or (int(info['versionCode']), info['sha256']) == LEGACY, 'New releases must be immutable'
    assets = {item['name']: item for item in release['assets']}
    expected = f'pikmin-control-center-{info["versionName"]}.apk'
    assert assets[expected]['size'] == int(info['size'])
    asset_index = parse(fetch(assets['update.properties']['browser_download_url'], 8192).decode('utf-8'))
    assert asset_index == info, 'Index differs from release attachment'
    payload = fetch(info['apkUrl'], int(info['size']))
    assert len(payload) == int(info['size']) and hashlib.sha256(payload).hexdigest() == info['sha256']
    sdk = Path(os.environ.get('ANDROID_HOME', '/usr/local/lib/android/sdk'))
    signers = sorted((sdk / 'build-tools').glob('*/apksigner'))
    assert signers, 'Android apksigner missing'
    with tempfile.TemporaryDirectory(prefix='cc-index-') as stage:
        apk = Path(stage) / 'release.apk'
        apk.write_bytes(payload)
        cert = subprocess.check_output([str(signers[-1]), 'verify', '--print-certs', str(apk)], text=True)
        assert 'Signer #1 certificate SHA-256 digest: ' + CERT in cert, 'Wrong signing identity'
        badging = subprocess.check_output([str(signers[-1].parent / 'aapt2'), 'dump', 'badging', str(apk)], text=True)
        assert f"package: name='dev.ody.pikmincontrol' versionCode='{info['versionCode']}' versionName='{info['versionName']}'" in badging
    if release.get('immutable'):
        provenance = json.loads(fetch(assets['build-provenance.json']['browser_download_url'], 32768))
        assert provenance['apkSha256'] == info['sha256'] and provenance['versionCode'] == int(info['versionCode'])
        assert re.fullmatch('[a-f0-9]{40}', provenance['sourceCommit']) and int(provenance['ciRunId']) > 0
    print('PASS: allowlist, monotonic index, immutable release, anonymous SHA, APK identity and signature')

if __name__ == '__main__':
    main()
