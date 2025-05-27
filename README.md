# Flash GN Calculator

A simple cross-platform desktop application to calculate flash **Guide Number**, **f-number (aperture)**, or **distance** for manual flash photography. Built using `wxPython` and ChatGPT.

## Features

- Calculates:
  -  Guide Number
  -  F-Number
  -  Distance
- Supports both **Meters** and **Feet**
- Supports **ISO adjustment**
- Accepts **European decimals** (`,` or `.`)
- Input validation with helpful error messages
- Clean UI with real-time results

---

## Getting Started

### Prerequisites

Make sure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

##  Run the app
python PyFlashGNCalc.py

## File Structure

- PyFlashGNCalc.py – Main App
- fgnc.png – App Window Icon
- requirements.txt – Dependencies

---

## Calculation Logic

The app uses the formula:

```bash
GN = F-Number × Distance × sqrt(ISO / 100)
```
You can calculate any one value by entering the other two. All Guide Numbers are assumed to be based on ISO 100.

---

## Packaging (optional)
To build a standalone .exe (Windows):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=flash_icon.ico PyGNCalc.py
```

---

## Powered by

- [wxPython](https://wxpython.org/)
- [PyInstaller](https://pyinstaller.org/)

## Made by

- [MySQL](https://github.com/0r4cl3MySQL)
- [ChatGPT](https://chat.openai.com/)
- [wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder)
