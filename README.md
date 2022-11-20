# Python Planner Generator

This code creates a digital planner (maybe printable someday) for use with the
iPad app goodnotes 5.

## Prerequisites 

- Python3
- Jinja2
- python-dateutil
- Node / NPM

## Install

Run 

```bash
npm install
```

to install the tailwind dependency.

## Building the planner

```bash
npm run build
```

To create the PDF from the HTML output, I recommend opening `index.html` in 
Chrome and using the "Save as PDF" feature in the print menu. If using this 
technique, set margins to none and enable background images.
