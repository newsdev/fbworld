import json
import os
import unittest


class GetMembersDictTestCase(unittest.TestCase):
    DATA_DIR = "%s/" % os.path.dirname(os.path.realpath(__file__))

    data_path = "%s/member_groups_output.json" % DATA_DIR.replace('tests/', 'data')

    results = None
    key_0 = "391246377893952"
    key_1 = "1136709433084412"
    key_2 = "280768775366358"

    def setUp(self, **kwargs):
        with open(self.data_path, 'r') as readfile:
            self.results = dict(json.loads(readfile.read()))

    def test_first_two_groups(self):
        group_0 = set(self.results['data'].get(self.key_0))
        group_1 = set(self.results['data'].get(self.key_1))

        self.assertFalse(group_0.union(group_1) == group_1)

    def test_second_two_groups(self):
        group_1 = set(self.results['data'].get(self.key_1))
        group_2 = set(self.results['data'].get(self.key_2))

        self.assertFalse(group_1.union(group_2) == group_2)
    
    def test_outer_two_groups(self):
        group_0 = set(self.results['data'].get(self.key_0))
        group_2 = set(self.results['data'].get(self.key_2))

        self.assertFalse(group_0.union(group_2) == group_2)
