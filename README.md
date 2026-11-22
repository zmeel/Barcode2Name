# Barcode2Name

Collects the FASTQ files (`.fastq`, `.fq`, `.fastq.gz`, `.fq.gz`) from each barcode folder into a folder named after its sample, using a tab-separated mapping file:

```
barcode01	Ecoli-A0274-2505
barcode02	Ecoli-A0275-2504
```

The files in `barcode01/` go into `Ecoli-A0274-2505/`, and so on.

## Usage

```bash
python3 barcode2name.py barcode2map.txt /path/to/fastq_pass
```

| Option | Meaning |
|---|---|
| `input_dir` | Folder that contains `barcode01`, `barcode02`, … (default: current folder) |
| `-o DIR`, `--output-dir DIR` | Where the sample folders are created (default: `input_dir`) |
| `--move` | Move the files instead of copying them |
| `--overwrite` | Replace files that already exist in the destination (they are skipped by default) |
| `-n`, `--dry-run` | Print what would happen, without changing anything |

Needs Python 3.9 or newer and no extra packages.
