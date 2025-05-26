# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:19:31 2025

@author: Isabelly
"""

from backend.data_manager import DataManager

class KeywordManager:
    def __init__(self):
        self.data_manager = DataManager()

    def get_all_keyword_names(self):
        return [item["Keyword"] for item in self.data_manager.get_all_keywords()]

    def get_keyword_details(self, keyword_name):
        return self.data_manager.get_keyword_data(keyword_name)

    def search_keywords(self, query):
        query_lower = query.lower()
        found_keywords = []
        for item in self.data_manager.get_all_keywords():
            if query_lower in item["Keyword"].lower() or query_lower in item["Comment"].lower():
                found_keywords.append(item)
        return found_keywords