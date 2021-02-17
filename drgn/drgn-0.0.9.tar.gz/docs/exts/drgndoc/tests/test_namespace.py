# Copyright (c) Facebook, Inc. and its affiliates.
# SPDX-License-Identifier: GPL-3.0+

import os.path
import unittest

from drgndoc.namespace import Namespace, ResolvedNode
from drgndoc.parse import Class, Function, Module, parse_paths


class TestNamespace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        modules = parse_paths([os.path.join(os.path.dirname(__file__), "package")])
        cls.namespace = Namespace(modules)

    def assertModules(self, resolved_node, names):
        self.assertEqual([module.name for module in resolved_node.modules], names)

    def assertNames(self, bound_nodes, names):
        self.assertEqual([node.name for node in bound_nodes], names)

    def test_resolve_global_name_package(self):
        resolved = self.namespace.resolve_global_name("package")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, [])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "package")
        self.assertEqual(resolved.qualified_name(), "package")

    def test_resolve_global_name_submodule(self):
        resolved = self.namespace.resolve_global_name("package.module")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "module")
        self.assertEqual(resolved.qualified_name(), "package.module")

    def test_resolve_global_name_class(self):
        resolved = self.namespace.resolve_global_name("package.module.Class")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package", "module"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Class)
        self.assertEqual(resolved.name, "Class")
        self.assertEqual(resolved.qualified_name(), "package.module.Class")

    def test_resolve_global_name_method(self):
        resolved = self.namespace.resolve_global_name("package.module.Class.method")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package", "module"])
        self.assertNames(resolved.classes, ["Class"])
        self.assertIsInstance(resolved.node, Function)
        self.assertEqual(resolved.name, "method")
        self.assertEqual(resolved.qualified_name(), "package.module.Class.method")

    def test_resolve_global_name_nested_class(self):
        resolved = self.namespace.resolve_global_name(
            "package.module.Class.NestedClass"
        )
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package", "module"])
        self.assertNames(resolved.classes, ["Class"])
        self.assertIsInstance(resolved.node, Class)
        self.assertEqual(resolved.name, "NestedClass")
        self.assertEqual(resolved.qualified_name(), "package.module.Class.NestedClass")

    def test_resolve_global_name_nested_class_method(self):
        resolved = self.namespace.resolve_global_name(
            "package.module.Class.NestedClass.nested_method"
        )
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package", "module"])
        self.assertNames(resolved.classes, ["Class", "NestedClass"])
        self.assertIsInstance(resolved.node, Function)
        self.assertEqual(resolved.name, "nested_method")
        self.assertEqual(
            resolved.qualified_name(), "package.module.Class.NestedClass.nested_method"
        )

    def test_resolve_global_name_imports(self):
        resolved = self.namespace.resolve_global_name("package.imports.package.module")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "module")
        self.assertEqual(resolved.qualified_name(), "package.module")

        for name in ["package.imports.Class", "package.imports.Class2"]:
            resolved = self.namespace.resolve_global_name(name)
            self.assertIsInstance(resolved, ResolvedNode)
            self.assertNames(resolved.modules, ["package", "module"])
            self.assertNames(resolved.classes, [])
            self.assertIsInstance(resolved.node, Class)
            self.assertEqual(resolved.name, "Class")
            self.assertEqual(resolved.qualified_name(), "package.module.Class")

        resolved = self.namespace.resolve_global_name(
            "package.imports.ImportClass.module"
        )
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "module")
        self.assertEqual(resolved.qualified_name(), "package.module")

    def test_resolve_global_name_relative_imports(self):
        resolved = self.namespace.resolve_global_name("package.relativeimports.module")
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "module")
        self.assertEqual(resolved.qualified_name(), "package.module")

        resolved = self.namespace.resolve_global_name(
            "package.relativeimports.RelativeImportClass.module"
        )
        self.assertIsInstance(resolved, ResolvedNode)
        self.assertNames(resolved.modules, ["package"])
        self.assertNames(resolved.classes, [])
        self.assertIsInstance(resolved.node, Module)
        self.assertEqual(resolved.name, "module")
        self.assertEqual(resolved.qualified_name(), "package.module")

        self.assertEqual(
            self.namespace.resolve_global_name(
                "package.invalidrelativeimports.package"
            ),
            "package.invalidrelativeimports.package",
        )
        self.assertEqual(
            self.namespace.resolve_global_name("package.invalidrelativeimports.module"),
            "package.invalidrelativeimports.module",
        )

    def test_resolve_global_name_unresolved(self):
        self.assertEqual(self.namespace.resolve_global_name("foo"), "foo")
        self.assertEqual(
            self.namespace.resolve_global_name("package.foo"), "package.foo"
        )
        self.assertEqual(
            self.namespace.resolve_global_name("package.module.foo"),
            "package.module.foo",
        )
        self.assertEqual(
            self.namespace.resolve_global_name("package.module.Class.foo"),
            "package.module.Class.foo",
        )
        self.assertEqual(
            self.namespace.resolve_global_name("package.imports.package.foo"),
            "package.foo",
        )
        self.assertEqual(
            self.namespace.resolve_global_name("package.module.Class.method.foo"),
            "package.module.Class.method.foo",
        )
