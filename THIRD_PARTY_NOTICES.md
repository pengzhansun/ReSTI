# Upstream attribution

ReSTI is a modified annotation release derived from **STI-Bench: Are MLLMs
Ready for Precise Spatial-Temporal World Understanding?**, by Yun Li,
Yiming Zhang, Tao Lin, XiangRui Liu, Wenxiao Cai, Zheng Liu, and Bo Zhao.

- Original dataset: <https://huggingface.co/datasets/MINT-SJTU/STI-Bench>
- Original paper: <https://arxiv.org/abs/2503.23765>
- Original evaluation repository: <https://github.com/MINT-SJTU/STI-Bench>

The upstream dataset card identifies **Apache-2.0** as its license. A copy is
preserved in [LICENSES/STI-Bench-Apache-2.0.txt](LICENSES/STI-Bench-Apache-2.0.txt)
for the upstream material. This attribution does not assign that license to
all original ReSTI code, figures, or source media.

## Modifications

Relative to STI-Bench, ReSTI rewrites under-specified questions, reconstructs
source-backed answers, rebuilds candidates and answer keys, adds stable row
identifiers, and records exclusions. The present public package preserves the
August 15, 2026 ReSTI v5 annotations without changing their contents; only
filenames and packaging were simplified. Details are in
[the README](README.md) and [release provenance](docs/release.md).

## Source datasets

STI-Bench draws on ScanNet, the Waymo Open Dataset, and Omni6DPose. Their
source videos and raw annotations retain their own access and usage terms.
This repository does not redistribute the original video collection or raw
source datasets. The example figures in `assets/` are from the ReSTI report.
