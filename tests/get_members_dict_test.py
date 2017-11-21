import json
import os
import unittest

class GetMembersDictTestCase(unittest.TestCase):

    data_path = ''
    results = {}

    def set_up(self, **kwargs):
        with open(self.data_path, 'r') as readfile:
            results = json.loads(readfile.read())

    def test_first_two_groups(self):
        group_0 = set(results['data'][0]['members'])
        group_1 = set(results['data'][1]['members'])

        self.assertFalse(group_0.union(group_1) == group_1)

    def test_second_two_groups(self):
        group_1 = set(results['data'][1]['members'])
        group_2 = set(results['data'][2]['members'])
            
        self.assertFalse(group_1.union(group_2) == group_2)
    
    def test_outer_two_groups(self):
        group_0 = set(results['data'][0]['members'])
        group_2 = set(results['data'][2]['members'])
            
        self.assertFalse(group_0.union(group_2) == group_2)
