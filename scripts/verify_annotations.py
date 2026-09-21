"""Verify release hashes, annotation integrity, and optional Parquet/JSONL parity."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_jsonl(path):
    def invalid_constant(value):
        raise ValueError(f'Non-finite JSON constant: {value}')
    return [json.loads(line, parse_constant=invalid_constant)
            for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def verify(parquet=False):
    release = json.loads((ROOT / 'release.json').read_text())
    for name, info in release['artifacts'].items():
        data = (ROOT / name).read_bytes()
        require(len(data) == info['bytes'], f'File size mismatch: {name}')
        require(hashlib.sha256(data).hexdigest() == info['sha256'],
                f'SHA-256 mismatch: {name}')
    for line in (ROOT / 'checksums.sha256').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                f'Checksum list mismatch: {name}')

    rows = read_jsonl(ROOT / 'annotations/resti.jsonl')
    excluded = read_jsonl(ROOT / 'annotations/excluded.jsonl')
    require(len(rows) == release['counts']['accepted'] == 1782, 'Accepted count')
    require(len(excluded) == release['counts']['excluded'] == 282, 'Excluded count')
    require(len(rows) + len(excluded) == release['counts']['original'] == 2064,
            'Total accounting')
    fields = {'Video', 'Source', 'Task', 'QType', 'Question', 'Prompt',
              'time_start', 'time_end', 'Candidates', 'Answer', 'Answer Detail',
              'ID', 'scene', 'ReSTI ID', 'Legacy Row Key'}
    ids, keys = set(), set()
    for row in rows:
        require(set(row) == fields, 'Accepted schema mismatch')
        identity = row['ReSTI ID']
        require(identity and identity not in ids, f'Duplicate ReSTI ID: {identity}')
        require(row['Legacy Row Key'] not in keys, f'Duplicate legacy key: {identity}')
        ids.add(identity)
        keys.add(row['Legacy Row Key'])
        candidates = row['Candidates']
        require(set(candidates) == set('ABCDE'), f'Five A–E choices: {identity}')
        require(all(isinstance(v, str) and v for v in candidates.values()),
                f'Invalid candidate string: {identity}')
        require(len(set(candidates.values())) == 5, f'Exact duplicate choices: {identity}')
        require(row['Answer'] in candidates, f'Invalid answer letter: {identity}')
        require(candidates[row['Answer']] == row['Answer Detail'],
                f'Key/detail mismatch: {identity}')
        require(row['Question'].strip() and row['Video'].strip(), f'Missing input: {identity}')
        require(all(isinstance(row[k], (int, float)) and math.isfinite(row[k])
                    for k in ('time_start', 'time_end')), f'Invalid time: {identity}')
        require(0 <= row['time_start'] <= row['time_end'], f'Time order: {identity}')

    excluded_keys = set()
    for row in excluded:
        require(row['key'] not in excluded_keys, 'Duplicate exclusion key')
        require(row['key'] not in keys, 'Accepted/excluded overlap')
        require(isinstance(row['reason_codes'], list) and row['reason_codes'],
                'Exclusion has no reason codes')
        excluded_keys.add(row['key'])

    for name, actual in (
        ('accepted_by_source', Counter(r['Source'] for r in rows)),
        ('accepted_by_task', Counter(r['Task'] for r in rows)),
        ('excluded_by_task', Counter(r['task'] for r in excluded)),
        ('answer_letters', Counter(r['Answer'] for r in rows)),
    ):
        require(dict(actual) == release[name], f'Summary mismatch: {name}')

    if parquet:
        try:
            import pyarrow.parquet as pq
        except ImportError as exc:
            raise RuntimeError('Install pyarrow to use --parquet.') from exc
        table = pq.read_table(ROOT / 'annotations/resti.parquet')
        require(table.to_pylist() == rows, 'Parquet and JSONL records differ')

    return {
        'release': 'ReSTI v5', 'accepted_rows': len(rows),
        'excluded_rows': len(excluded), 'unique_accepted_ids': len(ids),
        'accepted_excluded_disjoint': True,
        'sha256_checks': 'pass', 'key_detail_agreement': 'pass',
        'exact_candidate_uniqueness': 'pass', 'timestamp_order': 'pass',
        'summary_counts': 'pass',
        'parquet_jsonl_parity': 'pass' if parquet else 'not run',
        'scope': 'Packaged annotation integrity; does not rerun raw-source reconstruction or model evaluation.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parquet', action='store_true', help='Also compare every Parquet record using pyarrow.')
    parser.add_argument('--output', type=Path, help='Write the validation result as JSON.')
    args = parser.parse_args()
    result = verify(args.parquet)
    output = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')
