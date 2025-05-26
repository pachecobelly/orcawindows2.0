# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:18:28 2025

@author: Isabelly
"""

import json
import os

class DataManager:
    _instance = None
    _data = None
    # Construct the path to the data file robustly
    DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/orca_data.json')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.DATA_FILE}")
            self._data = {"keywords": [], "basis_sets": {}, "dft_methods": {}}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.DATA_FILE}")
            self._data = {"keywords": [], "basis_sets": {}, "dft_methods": {}}

    def get_all_keywords(self):
        return self._data.get("keywords", [])

    def get_keyword_data(self, keyword_name):
        return [item for item in self._data.get("keywords", []) if item["Keyword"].lower() == keyword_name.lower()]

    def get_all_basis_sets(self):
        return self._data.get("basis_sets", {})

    def get_basis_set_data(self, group_name):
        return self._data.get("basis_sets", {}).get(group_name, [])

    def get_all_dft_methods(self):
        return self._data.get("dft_methods", {})

    def get_dft_method_data(self, group_name):
        return self._data.get("dft_methods", {}).get(group_name, [])

    def search_all_data(self, query):
        query_lower = query.lower()
        results = {
            "keywords": [],
            "basis_sets": [],
            "dft_methods": []
        }

        # Search Keywords
        for keyword_entry in self.get_all_keywords():
            if query_lower in keyword_entry.get("Keyword", "").lower() or \
               query_lower in keyword_entry.get("Comment", "").lower():
                results["keywords"].append(keyword_entry)

        # Search Basis Sets
        for group_name, entries in self.get_all_basis_sets().items():
            if query_lower in group_name.lower():
                results["basis_sets"].append({"group": group_name, "entries": entries})
            else:
                for entry_text in entries:
                    if query_lower in entry_text.lower():
                        results["basis_sets"].append({"group": group_name, "entries": entries})
                        break # Only add the group once if a match is found within its entries

        # Search DFT Methods
        for group_name, entries in self.get_all_dft_methods().items():
            if query_lower in group_name.lower():
                results["dft_methods"].append({"group": group_name, "entries": entries})
            else:
                for item in entries:
                    if query_lower in item.get("Keyword", "").lower() or \
                       query_lower in item.get("Comment", "").lower():
                        results["dft_methods"].append({"group": group_name, "entries": entries})
                        break # Only add the group once if a match is found within its entries

        return results