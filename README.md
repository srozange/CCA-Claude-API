# CCA-Claude-API

Exercices du training https://anthropic.skilljar.com/claude-with-the-anthropic-api

## Prérequis

- Python 3.x
- Une clé API Anthropic ([console.anthropic.com](https://console.anthropic.com))

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine du projet avec votre clé API :

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Utilisation

Le venv doit être activé (`source .venv/bin/activate`) dans chaque nouveau terminal.

- Scripts : `python 1-accessing_claude_with_api.py`, `python 2-prompt_evaluation.py`
- Notebooks : Visual Code avec l'extension Jupyter puis ouvrir l'un des fichiers `.ipynb`