# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:20:14 2025

@author: Isabelly
"""

from backend.data_manager import DataManager

class DFTManager:
    def __init__(self):
        self.data_manager = DataManager()

    def get_all_dft_method_groups(self):
        return list(self.data_manager.get_all_dft_methods().keys())

    def get_dft_method_details(self, group_name):
        return self.data_manager.get_dft_method_data(group_name)

    def search_dft_methods(self, query):
        query_lower = query.lower()
        found_dft_methods = {}
        for group_name, entries in self.data_manager.get_all_dft_methods().items():
            if query_lower in group_name.lower():
                found_dft_methods[group_name] = entries
            else:
                for item in entries:
                    if query_lower in item["Keyword"].lower() or query_lower in item["Comment"].lower():
                        found_dft_methods[group_name] = entries
                        break
        return found_dft_methods