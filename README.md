# Visualization Tool

This project is a visualization platform designed to explore **single-cell metabolic networks** and **pathway activity scores** across gynecologic and breast cancers. It enables researchers to investigate protein–protein interaction (PPI) networks and corresponding metabolic pathway activity levels in an interactive dashboard.

---

## Features

- Load subtype-specific PPI networks (e.g., breast cancer, ovarian cancer).
- Display gene-level networks with degree centrality.
- Visualize pathway activity as interactive bar charts.
- Toggle between cancer types to compare metabolic regulation.

---

## Installation & Setup

### Requirements

- Python 3.8 or higher
- macOS or Linux recommended

### Input Files

- visualization.py
- tsv files for PPI graph and Pathway scoring derived from scRNA seq data.

### Install the Python Libraries required
```
python3 -m venv venv
source venv/bin/activate
pip install dash pandas networkx plotly
```

### Now run the code 
```
python3 visualization.py
```

