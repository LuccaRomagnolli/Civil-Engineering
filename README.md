# Civil Engineering - Machine Learning & AI Systems

## Description
This project develops machine learning models for civil engineering data, with focus on robust preprocessing, reproducible evaluation, and clear project structure.

## Repository Structure
```
Civil-Engineering/
|
|-- LICENSE
|-- README.md
|-- datasets/                  # Raw datasets (immutable)
|-- notebooks/                 # Exploration notebooks
|-- src/                       # Reusable code (pipelines, configs)
|-- models/                    # Saved models and artifacts
|-- reports/                   # Figures and analysis outputs
|-- outputs/                   # Temporary outputs
```

## Reproducibility
- Fixed random seed in notebooks and pipelines.
- No data leakage: preprocessing happens inside pipelines and is fit only on training folds.
- Stratified splitting is used for imbalanced targets.

## How to Run
1. Install dependencies from `requirements.txt`.
2. Open `notebooks/Ensemble.ipynb` and run the cells in order.

## Author
Lucca Romagnolli

## License
See `LICENSE` for details.

Last update: February 2026
