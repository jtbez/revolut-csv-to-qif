# Revolut CSV to QIF Converter - Python GUI

A modern, user-friendly Graphical User Interface for converting Revolut CSV transaction files to QIF format.

## Features

- **File Browser**: Easy-to-use file selection dialogs
- **Folder Conversion**: Convert all CSV files in a directory
- **Progress Tracking**: Visual progress bars and status updates
- **Error Handling**: Graceful error messages and logging
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. Ensure Node.js is installed and the main conversion script is available:
```bash
# Navigate to the repository root
cd /path/to/revolut-csv-to-qif

# Make sure the node script exists
ls src/index.js
```

2. Run the GUI application:
```bash
cd python-ui
python3 ui.py
```

## Usage

1. **Convert Single File**:
   - Click "Select File" and choose a CSV file
   - Click "Convert Selected File" to convert it

2. **Convert Multiple Files**:
   - Click "Select Folder with CSV files" and choose a directory
   - All CSV files in that directory will be converted
   - Progress is displayed as each file is processed

## Requirements

- Python 3.6 or higher
- Node.js (for the conversion engine)
- tkinter (usually included with Python)

## Troubleshooting

- If you get a `FileNotFoundError` for the Node script, ensure you're running the application from the Python UI directory
- If Node.js is not in your PATH, the application will show an error when trying to start the conversion
- Make sure you have permission to write output files in the directory where the CSV files are located

## License

See the main repository LICENSE file