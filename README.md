# PANW License Key Retrieval

This repository contains a small Python script to download `.key` license files for a specific Palo Alto Networks NGFW serial number using the Palo Alto Networks licensing API.

## Prerequisites

- Python 3
- A Palo Alto Networks Licensing API key

You must generate a Licensing API key in the Palo Alto Networks Support Portal before using this script.

## Setup

Run the setup command once to store your API key locally in `config.py`:

```bash
python3 licence.py setup
```

This writes your API key to a local file named `config.py` in the same directory.

## Usage

Interactive (prompts for serial number):

```bash
python3 licence.py serial
```

Non-interactive (pass serial and optional output directory):

```bash
python3 licence.py serial <SERIAL_NUMBER> <OUTPUT_DIR>
```

Examples:

```bash
python3 licence.py serial 001606064532
python3 licence.py serial 001606064532 ./keys
```

## Output

For each license returned by the API, the script writes a `.key` file in the form:

```
<SERIAL>-<PART_ID>.key
```

## Notes

- If you regenerate your Licensing API key, re-run `python3 licence.py setup` to update `config.py`.
- Keep `config.py` private; it contains your API key.
