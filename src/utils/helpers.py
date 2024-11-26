# src/utils/helpers.py

import pandas as pd

def convert_frequency(freq):
    """
    Convertit une fréquence donnée en alias de pandas.

    Args:
        freq (str): Fréquence ('D', 'W', 'M', 'Q', 'Y').

    Returns:
        str: Alias de fréquence pandas correspondant.
    """
    freq_map = {
        'D': 'D',
        'W': 'W-MON',
        'M': 'MS',
        'Q': 'QS',
        'Y': 'AS'
    }
    return freq_map.get(freq, 'M')  # Par défaut mensuel

def apply_offset(df, offset):
    """
    Applique un offset de mois sur la colonne 'Date'.

    Args:
        df (pd.DataFrame): DataFrame contenant la colonne 'Date'.
        offset (int): Nombre de mois à ajouter.

    Returns:
        pd.DataFrame: DataFrame avec la colonne 'Date' ajustée.
    """
    if offset is not None:
        df['Date'] += pd.DateOffset(months=offset)
    return df