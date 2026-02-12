#!/usr/bin/env python3
"""
AI Classifier per Bandi - HuggingFace Gratuito
Classifica automaticamente se un testo è un bando e estrae informazioni.
"""

import os
import requests
import json
import re
from typing import Dict, List, Optional

HF_TOKEN = os.environ.get('HF_TOKEN', '')
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

def classify_text(text: str, labels: List[str]) -> Dict:
    """
    Classifica un testo usando zero-shot classification.
    Gratuito con HuggingFace Inference API.
    """
    if not HF_TOKEN:
        return {'label': labels[0], 'score': 0.5}
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": text[:1000],
        "parameters": {"candidate_labels": labels}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return {
                'label': result.get('labels', [labels[0]])[0],
                'score': result.get('scores', [0.5])[0]
            }
    except:
        pass
    
    return {'label': labels[0], 'score': 0.5}


def is_bando(text: str) -> bool:
    """Verifica se un testo è relativo a un bando/finanziamento."""
    labels = ["bando finanziamento incentivo", "notizia generica", "altro"]
    result = classify_text(text, labels)
    return result['label'] == "bando finanziamento incentivo" and result['score'] > 0.6


def extract_importo(text: str) -> str:
    """Estrae l'importo dal testo con regex avanzate."""
    patterns = [
        r'€\s*[\d.,]+(?:\s*(?:milioni|mila|mln|k|m))?',
        r'[\d.,]+\s*(?:euro|€|EUR)',
        r'fino\s+a\s+€?\s*[\d.,]+',
        r'massimo\s+€?\s*[\d.,]+',
        r'importo[:\s]+€?\s*[\d.,]+',
        r'contributo[:\s]+€?\s*[\d.,]+',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    return 'Vedi bando'


def extract_scadenza(text: str) -> str:
    """Estrae la scadenza dal testo."""
    patterns = [
        r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}',
        r'\d{1,2}\s+(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+\d{4}',
        r'entro\s+il\s+\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}',
        r'scadenza[:\s]+\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    return 'Vedi bando'


def extract_beneficiari(text: str) -> str:
    """Estrae i beneficiari dal testo."""
    keywords = {
        'startup': 'Startup',
        'pmi': 'PMI',
        'piccole e medie': 'PMI',
        'microimprese': 'Microimprese',
        'grandi imprese': 'Grandi imprese',
        'imprese femminili': 'Imprese femminili',
        'donne': 'Imprese femminili',
        'giovani': 'Giovani imprenditori',
        'under 35': 'Under 35',
        'under 56': 'Under 56',
        'artigian': 'Artigiani',
        'commerc': 'Commercianti',
        'turist': 'Settore turistico',
        'agricol': 'Agricoltura',
        'manifattur': 'Manifatturiero',
        'professionist': 'Professionisti',
    }
    
    text_lower = text.lower()
    found = []
    
    for keyword, label in keywords.items():
        if keyword in text_lower and label not in found:
            found.append(label)
    
    return ', '.join(found[:3]) if found else 'Imprese'


def analyze_bando(text: str) -> Dict:
    """
    Analizza un testo e estrae tutte le informazioni rilevanti.
    """
    return {
        'is_bando': is_bando(text),
        'importo': extract_importo(text),
        'scadenza': extract_scadenza(text),
        'beneficiari': extract_beneficiari(text),
    }


def enrich_bando(bando: Dict) -> Dict:
    """
    Arricchisce un bando con informazioni estratte via AI.
    """
    text = f"{bando.get('titolo', '')} {bando.get('descrizione', '')}"
    
    analysis = analyze_bando(text)
    
    # Aggiorna solo se i valori sono generici
    if bando.get('contributo_max') in ['Vedi bando', 'N/A', '']:
        bando['contributo_max'] = analysis['importo']
    
    if bando.get('scadenza') in ['Vedi bando', 'N/A', '']:
        bando['scadenza'] = analysis['scadenza']
    
    if bando.get('beneficiari') in ['Imprese', 'Vedi bando', 'N/A', '']:
        bando['beneficiari'] = analysis['beneficiari']
    
    return bando


if __name__ == '__main__':
    # Test
    test_text = """
    Bando Nuova Sabatini 2025: finanziamento agevolato fino a €4.000.000 
    per l'acquisto di macchinari e attrezzature. Scadenza 31/12/2025.
    Beneficiari: PMI di tutti i settori.
    """
    
    print("Test AI Classifier...")
    result = analyze_bando(test_text)
    print(f"È un bando: {result['is_bando']}")
    print(f"Importo: {result['importo']}")
    print(f"Scadenza: {result['scadenza']}")
    print(f"Beneficiari: {result['beneficiari']}")
