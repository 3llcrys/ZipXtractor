# ZipXtractor
ZipXtractor is a python script that extracts specific files for folders from a zip archive. 

## Getting Started

### Usage

```bash
usage: ZipXtractor [-h] -a {list,extract} -f FILE [-p PATH] [-s {True,False}] [-o OUTPUT] [-ex REGEX]
```

The tool can be used with several arguments, at least `--action` and `--file`.

```bash
python .\ZipXtractor.py --action list --file .\MUC-System1-2025-01-31.zip
```

### Options

options:
  `-h`, `--help` | show this help message and exit<br>
  `-a {list,extract}`, `--action {list,extract}` | action to take; Required<br>
  `-f FILE`, `--file FILE` | Zipfile to extract<br>
  `-p PATH`, `--path PATH` | file or directory path to extract from archive<br>
  `-s {True,False}`, `--structure {True,False}` | Keep original structure for export (True) or export only file (False)<br>
  `-o OUTPUT`, `--output OUTPUT` | output path; if $match is used enclosing the path in '' is required<br>
  `-ex REGEX`, `--regex REGEX` | regex that can be used on the input filename to modify the output path using groups ()<br>


### Examples

List contents of ZipFile
```bash
python .\ZipXtractor.py --action list --file .\MUC-System1-2025-01-31.zip
```

Extract all files of ZipFile
```bash
python .\ZipXtractor.py --action extract --file .\MUC-System1-2025-01-31.zip --output '.\out'
```

Extract specific directory 'Logs' of ZipFile (Structure MUC-System1-2025-01-31.zip\Logs)
```bash
python .\ZipXtractor.py --action extract --file .\MUC-System1-2025-01-31.zip --path 'Logs\' --output '.\out'
```

Extract specific file 'Logs\file.log' of ZipFile without keeping the original filestructure (file will be directrly stored in output path)
```bash
python .\ZipXtractor.py --action extract --file .\MUC-System1-2025-01-31.zip --path 'Logs\file.log' --output '.\out' --structure 'False'
```

Extract specific directory 'Logs' of ZipFile in a output directory named as a regular expression match of the input ZipFile
```bash
python .\ZipXtractor.py --action extract --file .\MUC-System1-2025-01-31.zip --path 'Logs\' --output '.\out\$match' --structure 'False' --regex 'MUC-([A-Za-z0-9\-]+)-[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'
#Regex MUC-([A-Za-z0-9\-]+)-[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} identified "System1"
#Files will be extracted to '.\out\System1'
```
