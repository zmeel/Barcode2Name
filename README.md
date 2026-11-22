# Barcode2Name

Collects the FASTQ files (`.fastq`, `.fq`, `.fastq.gz`, `.fq.gz`) from each barcode folder into a folder named after its sample, using a tab-separated mapping file:

```
barcode01	Ecoli-A0274-2505
barcode02	Ecoli-A0275-2504
```

The files in `barcode01/` go into `Ecoli-A0274-2505/`, and so on.

## Usage

The default locations are set at the top of `barcode2name.py`:

```python
# Definieer het pad naar de directory met de submappen
base_directory = r"\\amg\medisch\MMI-Backup\Backup MMI-Moleculair\WGS\Main\Fastq data"
barcode_file = "barcode2map.txt"
```

With those defaults you can simply run:

```bash
python barcode2name.py
```

`barcode2map.txt` is looked for in the current folder, then in `base_directory`, then next to the script.
You can override both on the command line:

```bash
python barcode2name.py other_map.txt "D:\some\other\folder"
```

| Option | Meaning |
|---|---|
| `map_file` | Mapping file (default: `barcode_file`) |
| `input_dir` | Folder that contains `barcode01`, `barcode02`, … (default: `base_directory`) |
| `-o DIR`, `--output-dir DIR` | Where the sample folders are created (default: `input_dir`) |
| `--move` | Move the files instead of copying them |
| `--overwrite` | Replace files that already exist in the destination (they are skipped by default) |
| `-n`, `--dry-run` | Print what would happen, without changing anything |

Needs Python 3.9 or newer and no extra packages.
