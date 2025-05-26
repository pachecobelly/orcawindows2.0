# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:19:47 2025

@author: Isabelly
"""

from backend.data_manager import DataManager

class BasisSetManager:
    def __init__(self):
        self.data_manager = DataManager()

    def get_all_basis_set_groups(self):
        return list(self.data_manager.get_all_basis_sets().keys())

    def get_basis_set_details(self, group_name):
        return self.data_manager.get_basis_set_data(group_name)

    def search_basis_sets(self, query):
        query_lower = query.lower()
        found_basis_sets = {}
        for group_name, entries in self.data_manager.get_all_basis_sets().items():
            if query_lower in group_name.lower():
                found_basis_sets[group_name] = entries
            else:
                for entry_text in entries:
                    if query_lower in entry_text.lower():
                        found_basis_sets[group_name] = entries
                        break
        return found_basis_sets