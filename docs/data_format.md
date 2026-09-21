# Annotation format

## Accepted questions

`annotations/resti.parquet` and `annotations/resti.jsonl` contain the same
**1,782 rows**, in the same order. JSONL has one JSON object per line and can
be read with the Python standard library. Candidate values and answer details
are strings, including answers that encode structured geometry as JSON text.

| Field | Type | Meaning |
| --- | --- | --- |
| `ReSTI ID` | string | Unique, stable identifier for evaluation results and checkpoints. |
| `Legacy Row Key` | string | Link to the original benchmark row, including a disambiguating `uid` suffix. |
| `Video` | string | Original STI-Bench video filename. |
| `Source` | string | `ScanNet`, `Waymo`, or `Omni6DPose`. |
| `Task` | string | One of the eight task names listed in the README. |
| `QType` | string | Question type inherited from the benchmark. |
| `Question` | string | Repaired question specifying the requested measurement. |
| `Prompt` | string | Associated prompt field; it can be empty. |
| `time_start`, `time_end` | number | Start and end timestamps in seconds; use the times and conventions stated in the question. |
| `Candidates` | object | Five choices, with keys `A`, `B`, `C`, `D`, and `E` and string values. |
| `Answer` | string | Correct candidate letter. |
| `Answer Detail` | string | Reference answer; exactly equal to `Candidates[Answer]`. |
| `ID` | integer | Legacy question ID; not globally unique. |
| `scene` | string | Legacy scene metadata. |

Do not rename, truncate, or reconstruct `ReSTI ID` values. Strings such as
`resti-orientation-v1` or `resti-rem6r2` inside an identifier are historical
namespaces, not the version of the dataset being loaded. All accepted rows in
this repository belong to **ReSTI v5**.

Geometric conventions depend on the task and source. Read the question and
serialized reference value rather than imposing a single convention on every
task. In particular, the Orientation task measures signed optical heading in
the gravity-horizontal plane, with angles wrapped to `[-180, 180)` degrees.
The technical report defines the task-specific reconstruction operators.

## Excluded questions

`annotations/excluded.jsonl` contains **282 records**. These are exclusion
records, not additional accepted evaluation questions. Their `key` values
are disjoint from the accepted set's `Legacy Row Key` values.

Common fields:

| Field | Meaning |
| --- | --- |
| `key` | Unique key of the excluded legacy row. |
| `legacy_id`, `legacy_video` | Original question ID and video filename. |
| `source`, `task` | Source dataset and task name. |
| `reason_codes` | Nonempty list of the recorded exclusion reasons. |

There are two original record formats: 279 records additionally contain
`verification_verdict` and `verification_evidence`; the other three contain
`component`. These original fields are preserved. Detailed evidence is
therefore not represented by the same fields in every exclusion record.

A historical reason code can describe the construction stage at which a row
was excluded; use the associated verification verdict and evidence when
present. Exclusion means the released question does not yield one scoreable
answer under the available evidence. It does not imply that every excluded
legacy number is numerically wrong.

## Loading and checking

The README provides JSONL and PyArrow examples. To check the complete release:

```sh
python scripts/verify_annotations.py --parquet
```

PyArrow is required only for the `--parquet` comparison. The other checks use
the Python standard library. All files and counters are described in
[`release.json`](../release.json); file digests are also listed in
[`checksums.sha256`](../checksums.sha256).
