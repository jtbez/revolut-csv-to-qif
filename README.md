# Revolut CSV to QIF Converter

Convert Revolut CSV transaction files to QIF format for use in accounting software

## Features

- ✅ **Node.js conversion script**: Efficient CSV to QIF conversion
- 🖥️ **Python GUI**: Modern, user-friendly interface (see python-ui/ directory)

### How to use ?

#### Command Line
You need to have `node.js` >= 10.5

```bash
git@github.com:hqro/revolut-csv-to-qif.git
cd revolut-csv-to-qif
npm install --production
node src/index.js $FILE
```

Replace `$FILE` with your *Revolut* export. You can now find a `*.qif` file on your current directory

```
more Revolut-Statement-*.qif

!Type:Bank
D06/12/2018
T-14.09
P<label>
^
D05/12/2018
T-2.80
P<label>
^
```

#### Python GUI
A modern GUI application with drag-and-drop file selection and folder conversion support.

```bash
cd python-ui
python3 ui.py
```

See [python-ui/README.md](python-ui/README.md) for more details.