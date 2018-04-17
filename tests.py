# -*- coding: utf-8 -*-


import sys
import unittest

from unittest.mock import patch

from gothon import *


class TestGothon(unittest.TestCase):

    maxDiff, __slots__ = None, ()

    def test_GoImporter(self):
        go_importer = GoImporter([])
        result = go_importer.find_module("python_module")

        self.assertIsInstance(result, GoImporter)
        self.assertEqual(result.go_path, 'python_module.go')
        self.assertEqual(result.module_names, ([], ))
        self.assertTrue(callable(result.find_module))
        self.assertTrue(callable(result.load_module))

        go_importer.load_module("python_module")

        self.assertIsInstance(result, GoImporter)
        self.assertEqual(result.go_path, 'python_module.go')
        self.assertEqual(result.module_names, ([], ))
        self.assertTrue(callable(result.find_module))
        self.assertTrue(callable(result.load_module))

    def test_import_hook(self):
        with patch.object(sys, 'path_hooks', []):
            with patch.object(sys, 'meta_path', []):
                result = import_hook()
                self.assertIsInstance(result, GoImporter)
                self.assertTrue(len(sys.path_hooks) == 1)
                self.assertTrue(len(sys.meta_path) == 1)
