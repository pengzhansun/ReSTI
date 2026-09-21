# Release identity and provenance

## One release name

The public dataset version is **ReSTI v5**, originally packaged on
**August 15, 2026**. It is the release described in the technical report.
The original package called its merged dataset `resti_expanded_v4`.
That internal build name is not a different public version.

On September 21, 2026, the final annotation files were copied into this
repository under descriptive names:

| Original archive member under `ReSTI_v5/` | Public path |
| --- | --- |
| `qa_resti_expanded_v4.parquet` | `annotations/resti.parquet` |
| `qa_resti_expanded_v4.jsonl` | `annotations/resti.jsonl` |
| `excluded_rows.jsonl` | `annotations/excluded.jsonl` |

**The three files are byte-identical to their originals.** No question,
answer, candidate, timestamp, row ordering, column, stable identifier, or
exclusion reason was changed. The original names appear only where needed
for provenance; users should load the public paths above.

The original archive is `ReSTI_v5_20260815.zip`. Its checksum, original artifact
paths, and individual file checksums are recorded in
[`release.json`](../release.json). All 46 entries of its packaged
`MANIFEST.sha256` were checked before copying the final data.

The Parquet SHA-256 is:

```text
5b3dbbb30aef6d078944ee9c0c91bb01dd5d487faf94eeb1ae854e1f46ea10b8
```

## What is included

- All 1,782 accepted questions, in both Parquet and JSONL.
- All 282 exclusion records.
- Descriptions of the annotation schema and release identity.
- A verifier and its recorded result.
- The five current report figures, with PNG previews and vector PDFs.

The original videos are reused. Raw ScanNet, Waymo, and Omni6DPose source
data are not included in this annotation repository. Earlier component
Parquets, historical build scripts, and draft work logs are not alternative
entry points to the released dataset and are not copied into this repository.

## Relation to the report

The report accounts for all 2,064 original questions: 1,782 accepted and
282 excluded. V5 includes the completed rebuild of the 185 Orientation
candidate sets, while retaining their reconstructed target values. Historical
version numbers inside record identifiers are preserved for stable joins.

The figures were exported from the final PDF assets in
[report commit `27a9ab4`](https://github.com/pengzhansun/ReSTI-Technical-Report/tree/27a9ab4).
The report's earlier release-verification notes remain on its
[archive branch](https://github.com/pengzhansun/ReSTI-Technical-Report/tree/archive/pre-arxiv-2026-09-21).

## Validation scope

The publication check verifies file hashes, row counts, IDs, exact candidate
uniqueness, keyed-answer agreement, timestamp ordering, and task/source
summaries. It also compares every Parquet record against the JSONL export.
These are checks of the packaged release, not a rerun of the source-data
reconstruction or a model evaluation. The repository does not claim that
all possible answer-only strategies are eliminated.

The results are recorded in [`validation.json`](../validation.json).
