# Data & AI Lab

This repository is a public, progressive laboratory for developing and documenting practical skills in data and applied artificial intelligence. It is currently at its foundation stage: the structure and working standards are in place, but no data projects have been published yet.

> Building products with purpose.

The laboratory follows a simple approach: learn by building, demonstrate through understanding, and document to evolve.

## Purpose

The purpose of this repository is to turn technical learning into public evidence that is understandable, reproducible, and honestly documented. Each future project should make its reasoning visible, not only its output.

## Focus Areas

The laboratory will progressively explore:

- Python for data.
- Data cleaning and transformation.
- Exploratory data analysis.
- Data visualization.
- Applied statistics.
- Machine learning.
- Model evaluation.
- Big data.
- Automation.
- Applied artificial intelligence.

These are planned areas of development, not claims about work already completed.

## Working Principles

- Understanding before complexity.
- Reproducibility from data preparation to interpretation.
- Clear technical documentation.
- Honest interpretation of results.
- Explicit assumptions and limitations.
- Progressive difficulty.
- Simple solutions before unnecessary abstraction.
- No hidden failures or selective reporting.

## Repository Structure

- `notebooks/`: focused, numbered notebooks for exploration, explanation, and experiments.
- `datasets/`: datasets that may be stored legally and responsibly, or instructions for obtaining data that cannot be committed.
- `projects/`: self-contained, numbered data projects with descriptive names.
- `src/`: reusable Python modules when a concrete project justifies shared code.
- `docs/`: supporting technical documentation that does not belong in a project README.
- `requirements.txt`: external Python packages actually required by executable repository code.

The structure may evolve when a concrete need appears. `requirements.txt` is intentionally empty because the repository does not yet contain executable Python code requiring external packages.

## Project Organization

Future projects will be numbered and named descriptively, for example:

```text
projects/
└── 01-online-shoppers-analysis/
```

Each project should document:

- Objective.
- Context.
- Dataset source.
- Dataset usage conditions or license.
- Questions or hypotheses.
- Data preparation.
- Methodology.
- Results.
- Interpretation.
- Limitations.
- Conclusions.
- Next steps.

Folders will use lowercase `kebab-case`; Python files will use lowercase `snake_case`. Notebooks will be numbered and descriptive, for example:

```text
notebooks/
├── 01-data-loading.ipynb
├── 02-data-cleaning.ipynb
└── 03-exploratory-analysis.ipynb
```

Future code should use clear names, avoid unnecessary duplication, separate responsibilities when useful, prefer relative paths, and avoid undocumented local assumptions. Notebooks should follow a logical order, run from beginning to end, distinguish code and results from interpretation, use random seeds when appropriate, and avoid abandoned cells or excessive output.

## Roadmap

1. Repository foundation — completed by this initial setup.
2. Exploratory data analysis.
3. Supervised learning.
4. Segmentation or clustering.
5. Big data workflows.
6. Applied AI and automation.

This roadmap is a direction for future work, not a delivery schedule.

## Current Status

Initial repository setup. No data projects have been published yet.

## Reproducibility and Documentation

Future projects should:

- Use identifiable data sources and respect their licenses and usage conditions.
- Avoid private, sensitive, or unnecessary personal information.
- Explain how to obtain datasets that cannot be stored on GitHub.
- Prefer relative paths where practical.
- Record only real, necessary dependencies.
- Run in a clear and reproducible sequence.
- Explain decisions, failures, and limitations.
- Interpret results instead of presenting metrics without context.

## Author

Felipe Toro — building at the intersection of software, data, product, and applied artificial intelligence.
