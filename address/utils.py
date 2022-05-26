#!/usr/local/python3.10.4/bin/python3.10
# coding: utf-8

import re
import json
import unicodedata


class AddressParser:
    # https://www.soumu.go.jp/denshijiti/code.html のデータを元にして使用
    def __init__(self, city_file, ordinance_designated_city_file):
        HEADER_NUM = 5
        self.pref, self.pref_city, self.pref_od_city = set(), {}, {}

        with open(city_file) as f:
            for i, line in enumerate(f):
                if i < HEADER_NUM:
                    continue
                cols = line.split(",")
                pref = cols[1]
                city = cols[2]
                self.pref.add(pref)
                if pref not in self.pref_city:
                    self.pref_city.update({pref: [city]})
                else:
                    self.pref_city[pref].append(city)
            for v in self.pref_city.values():
                # データの都合上不要な''がリストに含まれるので、削除
                v.remove('')

        with open(ordinance_designated_city_file) as f:
            for i, line in enumerate(f):
                if i < HEADER_NUM:
                    continue
                cols = line.split(",")
                pref = cols[1]
                od_city = cols[2]
                if pref not in self.pref_od_city:
                    self.pref_od_city.update({pref: [od_city]})
                else:
                    self.pref_od_city[pref].append(od_city)
            for cites in self.pref_od_city.values():
                # データの都合上不要な'xxx市'がリストに含まれるので、削除
                cites.remove([c for c in cites if c[-1] == '市'][0])
                
    def get_parsed_address(self, address_raw):
        target_pref, target_city, target_area, target_street = None, None, None, None
        for pref in self.pref:
            # 都道府県の一致を検索
            if address_raw.startswith(pref):
                address_ex_pref = address_raw.replace(pref, '')
                target_pref = pref
                break
        if target_pref in self.pref_od_city:
            # 政令指定都市がある都道府県であれば、政令指定都市の市区の一致を検索
            for od_city in self.pref_od_city.get(target_pref):
                if address_ex_pref.startswith(od_city):
                    target_city = od_city
                    address_ex_city = address_ex_pref.replace(od_city)
                    break
        if not target_city:
            # 政令指定都市以外の市区の一致を検索
            for city in self.pref_city.get(target_pref):
                if address_ex_pref.startswith(city):
                    target_city = city
                    address_ex_city = address_ex_pref.replace(city, '')
                    break
        if target_pref and target_city:
            # 町名+○丁目を取得
            # 全角→半角
            address_ex_city_normalized = unicodedata.normalize("NFKC", address_ex_city)
            target_area = re.search(r'[^0-9]+[0-9]+', address_ex_city_normalized).group()
            target_street = address_ex_city_normalized.replace(target_area, '').lstrip('-')

        return [target_pref, target_city, target_area, target_street]