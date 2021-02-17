import codecs
import jedi
import json
import os
import sys

from jedi.inference import InferenceState
from jedi.api import helpers
from jedi.inference.gradual.conversion import convert_names
from jedi.api import classes

_virtualFilePath = 'virtual_file.py'

# Srctrail Constants
DEFINITION_IMPLICIT = 0
DEFINITION_EXPLICIT = 8

SYMBOL_TYPE = 0
SYMBOL_BUILTIN_TYPE = 1
SYMBOL_MODULE = 2
SYMBOL_NAMESPACE = 3
SYMBOL_PACKAGE = 4
SYMBOL_STRUCT = 5
SYMBOL_CLASS = 6
SYMBOL_INTERFACE = 7
SYMBOL_ANNOTATION = 8
SYMBOL_GLOBAL_VARIABLE = 9
SYMBOL_FIELD = 10
SYMBOL_FUNCTION = 11
SYMBOL_METHOD = 12
SYMBOL_ENUM = 13
SYMBOL_ENUM_CONSTANT = 14
SYMBOL_TYPEDEF = 15
SYMBOL_TYPE_PARAMETER = 16
SYMBOL_FILE = 17
SYMBOL_MACRO = 18
SYMBOL_UNION = 19

REFERENCE_TYPE_USAGE = 0
REFERENCE_USAGE = 1
REFERENCE_CALL = 2
REFERENCE_INHERITANCE = 3
REFERENCE_OVERRIDE = 4
REFERENCE_TYPE_ARGUMENT = 5
REFERENCE_TEMPLATE_SPECIALIZATION = 6
REFERENCE_INCLUDE = 7
REFERENCE_IMPORT = 8
REFERENCE_MACRO_USAGE = 9
REFERENCE_ANNOTATION_USAGE = 10


class SourcetrailScript(jedi.Script):
	def __init__(self, source=None, line=None, column=None, path=None,
				encoding='utf-8', sys_path=None, environment=None,
				_project=None):
		jedi.Script.__init__(self, source, line, column, path, encoding, sys_path, environment, _project)

	def _goto(self, line, column, follow_imports=False, follow_builtin_imports=False,
				only_stubs=False, prefer_stubs=False, follow_override=False):
		if follow_override:
			return super()._goto(line, column, follow_imports=follow_imports, follow_builtin_imports=follow_builtin_imports, only_stubs=only_stubs, prefer_stubs=prefer_stubs)
		tree_name = self._module_node.get_name_of_position((line, column))
		if tree_name is None:
			# Without a name we really just want to jump to the result e.g.
			# executed by `foo()`, if we the cursor is after `)`.
			return self.infer(line, column, only_stubs=only_stubs, prefer_stubs=prefer_stubs)
		name = self._get_module_context().create_name(tree_name)

		names = list(name.goto())

		if follow_imports:
			names = helpers.filter_follow_imports(names, follow_builtin_imports)
		names = convert_names(
			names,
			only_stubs=only_stubs,
			prefer_stubs=prefer_stubs,
		)

		defs = [classes.Name(self._inference_state, d) for d in set(names)]
		return list(set(helpers.sorted_definitions(defs)))

def start_indexer(file_path, sourceCode, environmentPath = None, sysPath = None, verbose = False):
    workingDirectory = os.getcwd()

    astVisitorClient = TestAstVisitorClient()

    indexSourceCode(
        file_path,
        sourceCode,
        workingDirectory,
        astVisitorClient,
        verbose,
        environmentPath,
        sysPath
    )

    astVisitorClient.updateReadableOutput()
    return astVisitorClient

def isValidEnvironment(environmentPath):
	try:
		environment = jedi.create_environment(environmentPath, False)
		environment._get_subprocess() # check if this environment is really functional
	except Exception as e:
		if os.name == 'nt' and os.path.isdir(environmentPath):
			try:
				environment = jedi.create_environment(os.path.join(environmentPath, "python.exe"), False)
				environment._get_subprocess() # check if this environment is really functional
				return ''
			except Exception:
				pass
		return str(e)
	return ''

def getEnvironment(environmentPath = None):
	if environmentPath is not None:
		try:
			environment = jedi.create_environment(environmentPath, False)
			environment._get_subprocess() # check if this environment is really functional
			return environment
		except Exception as e:
			if os.name == 'nt' and os.path.isdir(environmentPath):
				try:
					environment = jedi.create_environment(os.path.join(environmentPath, "python.exe"), False)
					environment._get_subprocess() # check if this environment is really functional
					return environment
				except Exception:
					pass
			print('WARNING: The provided environment path "' + environmentPath + '" does not specify a functional Python '
				'environment (details: "' + str(e) + '"). Using fallback environment instead.')

	try:
		environment = jedi.get_default_environment()
		environment._get_subprocess() # check if this environment is really functional
		return environment
	except Exception:
		pass

	try:
		for environment in jedi.find_system_environments():
			return environment
	except Exception:
		pass

	if os.name == 'nt': # this is just a workaround and shall be removed once Jedi is fixed (Pull request https://github.com/davidhalter/jedi/pull/1282)
		for version in jedi.api.environment._SUPPORTED_PYTHONS:
			for exe in jedi.api.environment._get_executables_from_windows_registry(version):
				try:
					return jedi.api.environment.Environment(exe)
				except jedi.InvalidPythonEnvironment:
					pass

	raise jedi.InvalidPythonEnvironment("Unable to find an executable Python environment.")

def indexSourceCode(file_path, sourceCode, workingDirectory, astVisitorClient, isVerbose = False, environmentPath = None, sysPath = None):

	environment = getEnvironment(environmentPath)

	project = jedi.api.project.Project(workingDirectory, environment_path = environment.path)

	evaluator = InferenceState(
		project,
		environment=environment,
		script_path=workingDirectory
	)

	module_node = evaluator.parse(
		code=sourceCode,
		path=workingDirectory,
		cache=False,
		diff_cache=False
	)

	_virtualFilePath = file_path

	astVisitor = AstVisitor(astVisitorClient, evaluator, file_path, sourceCode, sysPath)

	astVisitor.traverseNode(module_node)

class AstVisitor:

	def __init__(self, client, evaluator, sourceFilePath, sourceFileContent = None, sysPath = None):

		self.client = client
		self.environment = evaluator.environment

		self.sourceFilePath = sourceFilePath
		if sourceFilePath != _virtualFilePath:
			self.sourceFilePath = os.path.abspath(self.sourceFilePath)

		self.sourceFileName = os.path.split(self.sourceFilePath)[-1]
		self.sourceFileContent = sourceFileContent

		packageRootPath = os.path.dirname(self.sourceFilePath)
		while os.path.exists(os.path.join(packageRootPath, '__init__.py')):
			packageRootPath =  os.path.dirname(packageRootPath)
		self.sysPath = [packageRootPath]

		if sysPath is not None:
			self.sysPath.extend(sysPath)
		else:
			baseSysPath = evaluator.environment.get_sys_path()
			baseSysPath.sort(reverse=True)
			self.sysPath.extend(baseSysPath)
		self.sysPath = list(filter(None, self.sysPath))

		self.contextStack = []

		fileId = self.client.recordFile(self.sourceFilePath)
		# if fileId == 0:
		# 	print('ERROR: ' + srctrl.getLastError())
		self.client.recordFileLanguage(fileId, 'python')
		self.contextStack.append(ContextInfo(fileId, self.sourceFilePath, None))

		moduleNameHierarchy = self.getNameHierarchyFromModuleFilePath(self.sourceFilePath)
		if moduleNameHierarchy is not None:
			moduleId = self.client.recordSymbol(moduleNameHierarchy)
			self.client.recordSymbolDefinitionKind(moduleId, DEFINITION_EXPLICIT)
			self.client.recordSymbolKind(moduleId, SYMBOL_MODULE)
			self.contextStack.append(ContextInfo(moduleId, moduleNameHierarchy.getDisplayString(), None))


	def traverseNode(self, node):
		if node is None:
			return

		if node.type == 'classdef':
			self.beginVisitClassdef(node)
		elif node.type == 'funcdef':
			self.beginVisitFuncdef(node)
		if node.type == 'import_from':
			self.beginVisitImportFrom(node)
		if node.type == 'import_name':
			self.beginVisitImportName(node)
		elif node.type == 'name':
			self.beginVisitName(node)
		elif node.type == 'string':
			self.beginVisitString(node)
		elif node.type == 'error_leaf':
			self.beginVisitErrorLeaf(node)

		if hasattr(node, 'children'):
			for c in node.children:
				self.traverseNode(c)

		if node.type == 'classdef':
			self.endVisitClassdef(node)
		elif node.type == 'funcdef':
			self.endVisitFuncdef(node)
		if node.type == 'import_from':
			self.endVisitImportFrom(node)
		if node.type == 'import_name':
			self.endVisitImportName(node)
		elif node.type == 'name':
			self.endVisitName(node)
		elif node.type == 'string':
			self.endVisitString(node)
		elif node.type == 'error_leaf':
			self.endVisitErrorLeaf(node)


	def beginVisitClassdef(self, node):
		nameNode = getFirstDirectChildWithType(node, 'name')

		symbolNameHierarchy = self.getNameHierarchyOfNode(nameNode, self.sourceFilePath)
		if symbolNameHierarchy is None:
			symbolNameHierarchy = getNameHierarchyForUnsolvedSymbol()

		symbolId = self.client.recordSymbol(symbolNameHierarchy)
		self.client.recordSymbolDefinitionKind(symbolId, DEFINITION_EXPLICIT)
		self.client.recordSymbolKind(symbolId, SYMBOL_CLASS)
		self.client.recordSymbolLocation(symbolId, getSourceRangeOfNode(nameNode))
		self.client.recordSymbolScopeLocation(symbolId, getSourceRangeOfNode(node))
		self.contextStack.append(ContextInfo(symbolId, symbolNameHierarchy.getDisplayString(), node))


	def endVisitClassdef(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitFuncdef(self, node):
		nameNode = getFirstDirectChildWithType(node, 'name')

		symbolNameHierarchy = self.getNameHierarchyOfNode(nameNode, self.sourceFilePath)
		if symbolNameHierarchy is None:
			symbolNameHierarchy = getNameHierarchyForUnsolvedSymbol()

		symbolId = self.client.recordSymbol(symbolNameHierarchy)
		self.client.recordSymbolDefinitionKind(symbolId, DEFINITION_EXPLICIT)
		self.client.recordSymbolKind(symbolId, SYMBOL_FUNCTION)
		self.client.recordSymbolLocation(symbolId, getSourceRangeOfNode(nameNode))
		self.client.recordSymbolScopeLocation(symbolId, getSourceRangeOfNode(node))
		self.contextStack.append(ContextInfo(symbolId, symbolNameHierarchy.getDisplayString(), node))

		self.recordFunctionOverrideEdge(nameNode)


	def recordFunctionOverrideEdge(self, functionNameNode):
		try:
			functionNameHierarchy = self.getNameHierarchyOfNode(functionNameNode, self.sourceFilePath)
			if functionNameHierarchy is None:
				return
			functionSymbolId = self.client.recordSymbol(functionNameHierarchy)

			(startLine, startColumn) = functionNameNode.start_pos
			script = self.createScript(self.sourceFilePath)
			for definition in script.goto(line=startLine, column=startColumn, follow_imports=True, follow_override=True):
				if definition is None:
					continue

				overriddenNameNode = definition._name.tree_name

				if functionNameNode.start_pos == overriddenNameNode.start_pos:
					continue

				overriddenNameHierarchy = self.getNameHierarchyOfNode(overriddenNameNode, self.sourceFilePath)
				if overriddenNameHierarchy is None:
					continue
				overriddenSymbolId = self.client.recordSymbol(overriddenNameHierarchy)

				referenceId = self.client.recordReference(
					functionSymbolId,
					overriddenSymbolId,
					REFERENCE_OVERRIDE
				)

				self.client.recordReferenceLocation(referenceId, getSourceRangeOfNode(overriddenNameNode))
		except Exception:
			pass


	def endVisitFuncdef(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitImportName(self, node):
		self.recordErrorsForUnsolvedImports(node)


	def endVisitImportName(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitImportFrom(self, node):
		self.recordErrorsForUnsolvedImports(node)


	def endVisitImportFrom(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitName(self, node):
		if len(self.contextStack) == 0:
			return

		if node.value in ['True', 'False', 'None']: # these are not parsed as "keywords" in Python 2
			return

		referenceIsUnsolved = True
		for definition in self.getDefinitionsOfNode(node, self.sourceFilePath):
			if definition is None:
				continue

			try:
				if definition.type == 'instance':
					if definition.line is None and definition.column is None:
						if self.recordInstanceReference(node, definition):
							referenceIsUnsolved = False

				elif definition.type == 'module':
					if self.recordModuleReference(node, definition):
						referenceIsUnsolved = False

				elif definition.type in ['class', 'function']:
					(startLine, startColumn) = node.start_pos
					if definition.line == startLine and definition.column == startColumn:
						# Early exit. We don't record references for locations of classes or functions that are definitions
						return

					if definition.type == 'class':
						if self.recordClassReference(node, definition):
							referenceIsUnsolved = False

					elif definition.type == 'function':
						if self.recordFunctionReference(node, definition):
							referenceIsUnsolved = False

				elif definition.type == 'param':
					if definition.line is None or definition.column is None:
						# Early skip and try next definition. For now we don't record references for names that don't have a valid definition location
						continue

					if self.recordParamReference(node, definition):
						referenceIsUnsolved = False

				elif definition.type == 'statement':
					if definition.line is None or definition.column is None:
						# Early skip and try next definition. For now we don't record references for names that don't have a valid definition location
						continue

					if self.recordStatementReference(node, definition):
						referenceIsUnsolved = False
			except Exception as e:
				pass
				# print('ERROR: Encountered exception "' + e.__repr__() + '" while trying to solve the definition of node "' + node.value + '" at ' + getSourceRangeOfNode(node).toString() + '.')

		if referenceIsUnsolved:
			self.client.recordReferenceToUnsolvedSymhol(self.contextStack[-1].id, REFERENCE_USAGE, getSourceRangeOfNode(node))


	def endVisitName(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitString(self, node):
		sourceRange = getSourceRangeOfNode(node)
		if sourceRange.startLine != sourceRange.endLine:
			self.client.recordAtomicSourceRange(sourceRange)


	def endVisitString(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def beginVisitErrorLeaf(self, node):
		self.client.recordError('Unexpected token of type "' + node.token_type + '" encountered.', False, getSourceRangeOfNode(node))


	def endVisitErrorLeaf(self, node):
		if len(self.contextStack) > 0:
			contextNode = self.contextStack[-1].node
			if node == contextNode:
				self.contextStack.pop()


	def recordErrorsForUnsolvedImports(self, node):
		if node.type == 'import_from':
			for c in node.children:
				if self.recordErrorsForUnsolvedImports(c) is False:
					return False
		elif node.type == 'import_as_names':
			for c in node.children:
				self.recordErrorsForUnsolvedImports(c)
		elif node.type == 'import_as_name':
			for c in node.children:
				if c.type == 'keyword': # we just the children (usually only one) until we hit the "as" keyword
					break
				self.recordErrorsForUnsolvedImports(c)
		elif node.type == 'import_name':
			for c in node.children:
				self.recordErrorsForUnsolvedImports(c)
		elif node.type == 'dotted_as_names':
			for c in node.children:
				self.recordErrorsForUnsolvedImports(c)
		elif node.type == 'dotted_as_name':
			for c in node.children:
				if c.type == 'keyword': # we just the children (usually only one) until we hit the "as" keyword
					break
				self.recordErrorsForUnsolvedImports(c)
		elif node.type == 'dotted_name':
			for c in node.children:
				if self.recordErrorsForUnsolvedImports(c) is False:
					return False
		elif node.type == 'name':
			if len(self.getDefinitionsOfNode(node, self.sourceFilePath)) == 0:
				self.client.recordError('Imported symbol named "' + node.value + '" has not been found.', False, getSourceRangeOfNode(node))
				return False
		return True


	def recordInstanceReference(self, node, definition):
		nameHierarchy = self.getNameHierarchyFromFullNameOfDefinition(definition)
		if nameHierarchy is not None:
			referencedSymbolId = self.client.recordSymbol(nameHierarchy)
			self.client.recordSymbolKind(referencedSymbolId, SYMBOL_GLOBAL_VARIABLE)

			referenceKind = REFERENCE_USAGE
			if getParentWithType(node, 'import_from') is not None:
				# this would be the case for "from foo import f as my_f"
				#                                             ^    ^
				referenceKind = REFERENCE_IMPORT

			referenceId = self.client.recordReference(
				self.contextStack[-1].id,
				referencedSymbolId,
				referenceKind
			)
			self.client.recordReferenceLocation(referenceId, getSourceRangeOfNode(node))
			return True
		return False


	def recordModuleReference(self, node, definition):
		referencedNameHierarchy = self.getNameHierarchyFromModulePathOfDefinition(definition)
		if referencedNameHierarchy is None:
			referencedNameHierarchy = self.getNameHierarchyFromFullNameOfDefinition(definition)
		if referencedNameHierarchy is None:
			return False

		referencedSymbolId = self.client.recordSymbol(referencedNameHierarchy)

		# Record symbol kind. If the used type is within indexed code, we already have this info. In any other case, this is valuable info!
		self.client.recordSymbolKind(referencedSymbolId, SYMBOL_MODULE)

		if isQualifierNode(node):
			self.client.recordQualifierLocation(referencedSymbolId, getSourceRangeOfNode(node))
		else:
			referenceKind = REFERENCE_USAGE
			if getParentWithType(node, 'import_name') is not None:
				# this would be the case for "import foo"
				#                                    ^
				referenceKind = REFERENCE_IMPORT

			referenceId = self.client.recordReference(
				self.contextStack[-1].id,
				referencedSymbolId,
				referenceKind
			)

			self.client.recordReferenceLocation(referenceId, getSourceRangeOfNode(node))
		return True


	def recordClassReference(self, node, definition):
		referencedNameHierarchy = self.getNameHierarchyOfClassOrFunctionDefinition(definition)
		if referencedNameHierarchy is None:
			return False

		referencedSymbolId = self.client.recordSymbol(referencedNameHierarchy)

		# Record symbol kind. If the used type is within indexed code, we already have this info. In any other case, this is valuable info!
		self.client.recordSymbolKind(referencedSymbolId, SYMBOL_CLASS)

		if isQualifierNode(node):
			self.client.recordQualifierLocation(referencedSymbolId, getSourceRangeOfNode(node))
		else:
			referenceKind = REFERENCE_TYPE_USAGE
			if node.parent is not None:
				if node.parent.type == 'classdef':
					# this would be the case for "class Foo(Bar)"
					#                                       ^
					referenceKind = REFERENCE_INHERITANCE
				elif node.parent.type in ['arglist', 'testlist'] and node.parent.parent is not None and node.parent.parent.type == 'classdef':
					# this would be the case for "class Foo(Bar, Baz)"
					#                                       ^    ^
					referenceKind = REFERENCE_INHERITANCE
				elif getParentWithType(node, 'import_from') is not None:
					# this would be the case for "from foo import Foo as F"
					#                                             ^      ^
					referenceKind = REFERENCE_IMPORT

			referenceId = self.client.recordReference(
				self.contextStack[-1].id,
				referencedSymbolId,
				referenceKind
			)
			self.client.recordReferenceLocation(referenceId, getSourceRangeOfNode(node))

			if referenceKind == REFERENCE_TYPE_USAGE and isCallNode(node):
				constructorNameHierarchy = referencedNameHierarchy.copy()
				constructorNameHierarchy.nameElements.append(NameElement('__init__'))
				constructorSymbolId = self.client.recordSymbol(constructorNameHierarchy)
				self.client.recordSymbolKind(constructorSymbolId, SYMBOL_METHOD)
				callReferenceId = self.client.recordReference(
					self.contextStack[-1].id,
					constructorSymbolId,
					REFERENCE_CALL
				)
				self.client.recordReferenceLocation(callReferenceId, getSourceRangeOfNode(node))

		return True


	def recordFunctionReference(self, node, definition):
		referencedNameHierarchy = self.getNameHierarchyOfClassOrFunctionDefinition(definition)
		if referencedNameHierarchy is None:
			return False

		referencedSymbolId = self.client.recordSymbol(referencedNameHierarchy)

		# Record symbol kind. If the called function is within indexed code, we already have this info. In any other case, this is valuable info!
		self.client.recordSymbolKind(referencedSymbolId, SYMBOL_FUNCTION)

		referenceKind = -1
		if isCallNode(node):
			referenceKind = REFERENCE_CALL
		elif getParentWithType(node, 'import_from'):
			referenceKind = REFERENCE_IMPORT

		if referenceKind is -1:
			return False

		referenceId = self.client.recordReference(
			self.contextStack[-1].id,
			referencedSymbolId,
			referenceKind
		)

		self.client.recordReferenceLocation(referenceId, getSourceRangeOfNode(node))
		return True


	def recordParamReference(self, node, definition):
		localSymbolId = self.client.recordLocalSymbol(self.getLocalSymbolName(definition))
		self.client.recordLocalSymbolLocation(localSymbolId, getSourceRangeOfNode(node))
		return True


	def recordStatementReference(self, node, definition):
		definitionModulePath = definition.module_path
		if definitionModulePath is None:
			if self.sourceFilePath == _virtualFilePath:
				definitionModulePath = self.sourceFilePath
			else:
				return False

		symbolKind = None
		referenceKind = None
		definitionKind = None

		definitionNameNode = definition._name.tree_name
		namedDefinitionParentNode = getParentWithTypeInList(definitionNameNode, ['classdef', 'funcdef'])
		if namedDefinitionParentNode is not None:
			if namedDefinitionParentNode.type in ['classdef']:
				if getNamedParentNode(definitionNameNode) == namedDefinitionParentNode:
					# definition is not local to some other field instantiation but instead it is a static member variable
					if definitionNameNode.start_pos == node.start_pos and definitionNameNode.end_pos == node.end_pos:
						# node is the definition of the static member variable
						symbolKind = SYMBOL_FIELD
						definitionKind = DEFINITION_EXPLICIT
					else:
						# node is a usage of the static member variable
						referenceKind = REFERENCE_USAGE
			elif namedDefinitionParentNode.type in ['funcdef']:
				# definition may be a non-static member variable
				if definitionNameNode.parent is not None and definitionNameNode.parent.type == 'trailer':
					potentialParamNode = getNamedParentNode(definitionNameNode)
					if potentialParamNode is not None:
						for potentialParamDefinition in self.getDefinitionsOfNode(potentialParamNode, definitionModulePath):
							if potentialParamDefinition is not None and potentialParamDefinition.type == 'param':
								paramDefinitionNameNode = potentialParamDefinition._name.tree_name
								potentialFuncdefNode = getNamedParentNode(paramDefinitionNameNode)
								if potentialFuncdefNode is not None and potentialFuncdefNode.type == 'funcdef':
									potentialClassdefNode = getNamedParentNode(potentialFuncdefNode)
									if potentialClassdefNode is not None and potentialClassdefNode.type == 'classdef':
										preceedingNode = paramDefinitionNameNode.parent.get_previous_sibling()
										if preceedingNode is not None and preceedingNode.type != 'param':
											# 'paramDefinitionNameNode' is the first parameter of a member function (aka. 'self')
											referenceKind = REFERENCE_USAGE
											if definitionNameNode.start_pos == node.start_pos and definitionNameNode.end_pos == node.end_pos:
												symbolKind = SYMBOL_FIELD
												definitionKind = DEFINITION_EXPLICIT
		else:
			symbolKind = SYMBOL_GLOBAL_VARIABLE
			if definitionNameNode.start_pos == node.start_pos and definitionNameNode.end_pos == node.end_pos:
				# node is the definition of a global variable
				definitionKind = DEFINITION_EXPLICIT
			elif getParentWithType(node, 'import_from') is not None:
				# this would be the case for "from foo import f as my_f"
				#                                             ^    ^
				referenceKind = REFERENCE_IMPORT
			else:
				referenceKind = REFERENCE_USAGE

		sourceRange = getSourceRangeOfNode(node)

		if symbolKind is not None or referenceKind is not None:
			symbolNameHierarchy = self.getNameHierarchyOfNode(definitionNameNode, definitionModulePath)
			if symbolNameHierarchy is None:
				return False

			symbolId = self.client.recordSymbol(symbolNameHierarchy)

			if symbolKind is not None:
				self.client.recordSymbolKind(symbolId, symbolKind)

			if definitionKind is not None:
				self.client.recordSymbolDefinitionKind(symbolId, definitionKind)
				self.client.recordSymbolLocation(symbolId, sourceRange)

			if referenceKind is not None:
				referenceId = self.client.recordReference(
					self.contextStack[-1].id,
					symbolId,
					referenceKind
				)
				self.client.recordReferenceLocation(referenceId, sourceRange)
		else:
			localSymbolId = self.client.recordLocalSymbol(self.getLocalSymbolName(definition))
			self.client.recordLocalSymbolLocation(localSymbolId, sourceRange)
		return True


	def getLocalSymbolName(self, definition):
		definitionNameNode = definition._name.tree_name

		definitionModulePath = definition.module_path
		if definitionModulePath is None:
			if self.sourceFilePath == _virtualFilePath:
				definitionModulePath = self.sourceFilePath

		contextName = ''
		if definitionModulePath is not None:
			parentFuncdef = getParentWithType(definitionNameNode, 'funcdef')
			if parentFuncdef is not None:
				parentFuncdefNameNode = getFirstDirectChildWithType(parentFuncdef, 'name')
				if parentFuncdefNameNode is not None:
					parentFuncdefNameHierarchy = self.getNameHierarchyOfNode(parentFuncdefNameNode, definitionModulePath)
					if parentFuncdefNameHierarchy is not None:
						contextName = parentFuncdefNameHierarchy.getDisplayString()

		if len(contextName) == 0:
			contextName = str(self.contextStack[-1].name)

		return contextName + '<' + definitionNameNode.value + '>'


	def getNameHierarchyFromModuleFilePath(self, filePath):
		if filePath is None:
			return None

		if filePath == _virtualFilePath:
			return NameHierarchy(NameElement(os.path.splitext(_virtualFilePath)[0]), '.')

		filePath = os.path.abspath(filePath)
		filePath = os.path.splitext(filePath)[0]

		sysPath = []

		jediPath = os.path.dirname(jedi.__file__)
		major = self.environment.version_info.major
		minor = self.environment.version_info.minor
		if major == 2:
			sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/2'))
		if major == 2 or major == 3:
			sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/2and3'))
		if major == 3:
			sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/3'))
			if minor == 5:
				sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/3.5'))
			if minor == 6:
				sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/3.6'))
			if minor == 7:
				sysPath.append(os.path.abspath(jediPath + '/third_party/typeshed/stdlib/3.7'))

		sysPath.extend(self.sysPath)

		for p in sysPath:
			if filePath.startswith(p):
				rest = filePath[len(p):]
				if rest.startswith(os.path.sep):
					# Remove a slash in cases it's still there.
					rest = rest[1:]
				if rest:
					split = rest.split(os.path.sep)
					for string in split:
						if not string:
							return None

					if split[-1] == '__init__':
						split = split[:-1]
					if split[-1] == '__builtin__':
						split = split[:-1]
						split.insert(0, 'builtins')

					nameHierarchy = None
					for namePart in split:
						if nameHierarchy is None:
							nameHierarchy = NameHierarchy(NameElement(namePart), '.')
						else:
							nameHierarchy.nameElements.append(NameElement(namePart))
					return nameHierarchy

		return None


	def getNameHierarchyFromModulePathOfDefinition(self, definition):
		nameHierarchy = self.getNameHierarchyFromModuleFilePath(definition.module_path)
		if nameHierarchy is not None:
			if nameHierarchy.nameElements[-1].name != definition.name:
				nameHierarchy.nameElements.append(NameElement(definition.name))
		return nameHierarchy


	def getNameHierarchyFromFullNameOfDefinition(self, definition):
		nameHierarchy = None
		for namePart in definition.full_name.split('.'):
			if nameHierarchy is None:
				nameHierarchy = NameHierarchy(NameElement(namePart), '.')
			else:
				nameHierarchy.nameElements.append(NameElement(namePart))
		return nameHierarchy


	def getNameHierarchyOfClassOrFunctionDefinition(self, definition):
		if definition is None:
			return None

		if definition.line is None and definition.column is None:
			if definition.module_name in ['builtins', '__builtin__']:
				nameHierarchy = NameHierarchy(NameElement('builtins'), '.')
				if definition.full_name is not None:
					for namePart in definition.full_name.split('.'):
						nameHierarchy.nameElements.append(NameElement(namePart))
				else:
					for namePart in definition.name.split('.'):
						nameHierarchy.nameElements.append(NameElement(namePart))
				return nameHierarchy
			else:
				return self.getNameHierarchyFromFullNameOfDefinition(definition)

		else:
			if definition._name is None or definition._name.tree_name is None:
				return None

			definitionModulePath = definition.module_path
			if definitionModulePath is None:
				if self.sourceFilePath == _virtualFilePath:
					definitionModulePath = self.sourceFilePath
				else:
					return None

			return self.getNameHierarchyOfNode(definition._name.tree_name, definitionModulePath)


	def getDefinitionsOfNode(self, node, nodeSourceFilePath):
		try:
			(startLine, startColumn) = node.start_pos
			script = self.createScript(nodeSourceFilePath)
			return script.goto(line=startLine, column=startColumn, follow_imports=True)

		except Exception:
			return []


	def getNameHierarchyOfNode(self, node, nodeSourceFilePath):
		if node is None:
			return None

		if node.type == 'name':
			nameNode = node
		else:
			nameNode = getFirstDirectChildWithType(node, 'name')

		if nameNode is None:
			return None

		# we derive the name for the canonical node (e.g. the node's definition)
		for definition in self.getDefinitionsOfNode(nameNode, nodeSourceFilePath):
			if definition is None:
				continue

			definitionModulePath = definition.module_path
			if definitionModulePath is None:
				if self.sourceFilePath == _virtualFilePath:
					definitionModulePath = self.sourceFilePath
				else:
					continue

			definitionNameNode = definition._name.tree_name
			if definitionNameNode is None:
				continue

			parentNode = getParentWithTypeInList(definitionNameNode.parent, ['classdef', 'funcdef'])
			potentialSelfNode = getNamedParentNode(definitionNameNode)
			# if the node is defines as a non-static member variable, we remove the "function_name.self" from the
			# name hierarchy (e.g. "Foo.__init__.self.bar" gets shortened to "Foo.bar")
			if potentialSelfNode is not None:
				potentialSelfNameNode = getFirstDirectChildWithType(potentialSelfNode, 'name')
				if potentialSelfNameNode is not None:
					for potentialSelfDefinition in self.getDefinitionsOfNode(potentialSelfNameNode, definitionModulePath):
						if potentialSelfDefinition is None or potentialSelfDefinition.type != 'param':
							continue

						potentialSelfDefinitionNameNode = potentialSelfDefinition._name.tree_name

						potentialFuncdefNode = getNamedParentNode(potentialSelfDefinitionNameNode)
						if potentialFuncdefNode is None or potentialFuncdefNode.type != 'funcdef':
							continue

						potentialClassdefNode = getNamedParentNode(potentialFuncdefNode)
						if potentialClassdefNode is None or potentialClassdefNode.type != 'classdef':
							continue

						preceedingNode = potentialSelfDefinitionNameNode.parent.get_previous_sibling()
						if preceedingNode is not None and preceedingNode.type != 'param':
							# 'node' is the first parameter of a member function (aka. 'self')
							parentNode =  potentialClassdefNode

			nameElement = NameElement(definitionNameNode.value)

			if parentNode is not None:
				parentNodeNameHierarchy = self.getNameHierarchyOfNode(parentNode, definitionModulePath)
				if parentNodeNameHierarchy is None:
					return None
				parentNodeNameHierarchy.nameElements.append(nameElement)
				return parentNodeNameHierarchy

			nameHierarchy = self.getNameHierarchyFromModuleFilePath(nodeSourceFilePath)
			if nameHierarchy is None:
				return None
			nameHierarchy.nameElements.append(nameElement)
			return nameHierarchy

		return None


	def createScript(self, sourceFilePath):
		if sourceFilePath == _virtualFilePath: # we are indexing a provided code snippet
			return SourcetrailScript(
				source = self.sourceFileContent,
				environment = self.environment,
				sys_path = self.sysPath
			)
		else: # we are indexing a real file
			return SourcetrailScript(
				source = None,
				path = sourceFilePath,
				environment = self.environment,
				sys_path = self.sysPath
			)

class SourceRange:

	def __init__(self, startLine, startColumn, endLine, endColumn):
		self.startLine = startLine
		self.startColumn = startColumn
		self.endLine = endLine
		self.endColumn = endColumn


	def toString(self):
		return '[' + str(self.startLine) + ':' + str(self.startColumn) + '|' + str(self.endLine) + ':' + str(self.endColumn) + ']'

class NameHierarchy():

	unsolvedSymbolName = 'unsolved symbol' # this name should not collide with normal symbol name, because they cannot contain space characters

	def __init__(self, nameElement, delimiter):
		self.nameElements = []
		if nameElement is not None:
			self.nameElements.append(nameElement)
		self.delimiter = delimiter

	def copy(self):
		ret = NameHierarchy(None, self.delimiter)
		for nameElement in self.nameElements:
			ret.nameElements.append(NameElement(nameElement.name, nameElement.prefix, nameElement.postfix))
		return ret


	def serialize(self):
		return json.dumps(self, cls=NameHierarchyEncoder)


	def getDisplayString(self):
		displayString = ''
		isFirst = True
		for nameElement in self.nameElements:
			if not isFirst:
				displayString += self.delimiter
			isFirst = False
			if len(nameElement.prefix) > 0:
				displayString += nameElement.prefix + ' '
			displayString += nameElement.name
			if len(nameElement.postfix) > 0:
				displayString += nameElement.postfix
		return displayString

class NameElement:

	def __init__(self, name, prefix = '', postfix = ''):
		self.name = name
		self.prefix = prefix
		self.postfix = postfix

class NameHierarchyEncoder(json.JSONEncoder):

	def default(self, obj):
		if isinstance(obj, NameHierarchy):
			return {
				'name_delimiter': obj.delimiter,
				'name_elements': [nameElement.__dict__ for nameElement in obj.nameElements]
			}
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)

class ContextInfo:

	def __init__(self, id, name, node):
		self.id = id
		self.name = name
		self.node = node

def getNameHierarchyForUnsolvedSymbol():
	return NameHierarchy(NameElement(NameHierarchy.unsolvedSymbolName), '')

def isQualifierNode(node):
	nextNode = getNext(node)
	if nextNode is not None and nextNode.type == 'trailer':
		nextNode = getNext(nextNode)
	if nextNode is not None and nextNode.type == 'operator' and nextNode.value == '.':
		return True
	return False

def isCallNode(node):
	nextNode = getNext(node)
	if nextNode is not None and nextNode.type == 'trailer':
		if len(nextNode.children) >= 2 and nextNode.children[0].value == '(' and nextNode.children[-1].value == ')':
			return True
	return False

def getSourceRangeOfNode(node):
	startLine, startColumn = node.start_pos
	endLine, endColumn = node.end_pos
	return SourceRange(startLine, startColumn + 1, endLine, endColumn)

def getNamedParentNode(node):
	if node is None:
		return None

	parentNode = node.parent

	if node.type == 'name' and parentNode is not None:
		parentNode = parentNode.parent

	while parentNode is not None:
		if getFirstDirectChildWithType(parentNode, 'name') is not None:
			return parentNode
		parentNode = parentNode.parent

	return None

def getParentWithType(node, type):
	if node == None:
		return None
	parentNode = node.parent
	if parentNode == None:
		return None
	if parentNode.type == type:
		return parentNode
	return getParentWithType(parentNode, type)

def getParentWithTypeInList(node, typeList):
	if node == None:
		return None
	parentNode = node.parent
	if parentNode == None:
		return None
	if parentNode.type in typeList:
		return parentNode
	return getParentWithTypeInList(parentNode, typeList)

def getFirstDirectChildWithType(node, type):
	for c in node.children:
		if c.type == type:
			return c
	return None

def getDirectChildrenWithType(node, type):
	children = []
	for c in node.children:
		if c.type == type:
			children.append(c)
	return children

def getNext(node):
	if hasattr(node, 'children'):
		for c in node.children:
			return c

	siblingSource = node
	while siblingSource is not None and siblingSource.parent is not None:
		sibling = siblingSource.get_next_sibling()
		if sibling is not None:
			return sibling
		siblingSource = siblingSource.parent

	return None

class TestAstVisitorClient():

	def __init__(self):
		self.symbols = []
		self.localSymbols = []
		self.references = []
		self.qualifiers = []
		self.atomicSourceRanges = []
		self.errors = []

		self.serializedSymbolsToIds = {}
		self.symbolIdsToData = {}
		self.serializedLocalSymbolsToIds = {}
		self.localSymbolIdsToData = {}
		self.serializedReferencesToIds = {}
		self.referenceIdsToData = {}
		self.qualifierIdsToData = {}

		self.nextSymbolId = 1


	def updateReadableOutput(self):
		self.symbols = []
		for key in self.symbolIdsToData:
			symbolString = ''

			if 'definition_kind' in self.symbolIdsToData[key]:
				symbolString += self.symbolIdsToData[key]['definition_kind'] + ' '
			else:
				symbolString += 'NON-INDEXED '

			if 'symbol_kind' in self.symbolIdsToData[key]:
				symbolString += self.symbolIdsToData[key]['symbol_kind'] + ': '
			else:
				symbolString += 'SYMBOL: '

			if 'name' in self.symbolIdsToData[key]:
				symbolString += self.symbolIdsToData[key]['name']

			if 'symbol_location' in self.symbolIdsToData[key]:
				symbolString += ' at ' + self.symbolIdsToData[key]['symbol_location']

			if 'scope_location' in self.symbolIdsToData[key]:
				symbolString += ' with scope ' + self.symbolIdsToData[key]['scope_location']

			if 'signature_location' in self.symbolIdsToData[key]:
				symbolString += ' with signature ' + self.symbolIdsToData[key]['signature_location']

			symbolString = symbolString.strip()

			if symbolString:
				self.symbols.append(symbolString)

		self.localSymbols = []
		for key in self.localSymbolIdsToData:
			localSymbolString = ''

			if 'name' in self.localSymbolIdsToData[key]:
				localSymbolString += self.localSymbolIdsToData[key]['name']

			if localSymbolString and 'local_symbol_locations' in self.localSymbolIdsToData[key]:
				for location in self.localSymbolIdsToData[key]['local_symbol_locations']:
					self.localSymbols.append(localSymbolString + ' at ' + location)

		self.references = []
		for key in self.referenceIdsToData:
			if 'reference_location' not in self.referenceIdsToData[key] or len(self.referenceIdsToData[key]['reference_location']) == 0:
				self.referenceIdsToData[key]['reference_location'].append('')

			for referenceLocation in self.referenceIdsToData[key]['reference_location']:
				referenceString = ''

				if 'reference_kind' in self.referenceIdsToData[key]:
					referenceString += self.referenceIdsToData[key]['reference_kind'] + ': '
				else:
					referenceString += 'UNKNOWN REFERENCE: '

				if 'context_symbol_id' in self.referenceIdsToData[key] and self.referenceIdsToData[key]['context_symbol_id'] in self.symbolIdsToData:
					referenceString += self.symbolIdsToData[self.referenceIdsToData[key]['context_symbol_id']]['name']
				else:
					referenceString += 'UNKNOWN SYMBOL'

				referenceString += ' -> '

				if 'referenced_symbol_id' in self.referenceIdsToData[key] and self.referenceIdsToData[key]['referenced_symbol_id'] in self.symbolIdsToData:
					referenceString += self.symbolIdsToData[self.referenceIdsToData[key]['referenced_symbol_id']]['name']
				else:
					referenceString += 'UNKNOWN SYMBOL'

				if referenceLocation:
					referenceString += ' at ' + referenceLocation

				referenceString = referenceString.strip()

				if referenceString:
					self.references.append(referenceString)

		self.qualifiers = []
		for key in self.qualifierIdsToData:
			symbolName = 'UNKNOWN SYMBOL'
			if 'id' in self.qualifierIdsToData[key] and self.qualifierIdsToData[key]['id'] in self.symbolIdsToData:
				symbolName = self.symbolIdsToData[self.qualifierIdsToData[key]['id']]['name']

			for qualifierLocation in self.qualifierIdsToData[key]['qualifier_locations']:
				qualifierString = symbolName

				if qualifierLocation:
					qualifierString += ' at ' + qualifierLocation

				if qualifierString:
					self.qualifiers.append(qualifierString)


	def getNextElementId(self):
		id = self.nextSymbolId
		self.nextSymbolId += 1
		return id


	def recordSymbol(self, nameHierarchy):
		serialized = nameHierarchy.serialize()

		if serialized in self.serializedSymbolsToIds:
			return self.serializedSymbolsToIds[serialized]

		symbolId = self.getNextElementId()
		self.serializedSymbolsToIds[serialized] = symbolId
		self.symbolIdsToData[symbolId] = {
			'id': symbolId,
			'name': nameHierarchy.getDisplayString()
		}
		return symbolId


	def recordSymbolDefinitionKind(self, symbolId, symbolDefinitionKind):
		if symbolId in self.symbolIdsToData:
			self.symbolIdsToData[symbolId]['definition_kind'] = symbolDefinitionKindToString(symbolDefinitionKind)


	def recordSymbolKind(self, symbolId, symbolKind):
		if symbolId in self.symbolIdsToData:
			self.symbolIdsToData[symbolId]['symbol_kind'] = symbolKindToString(symbolKind)


	def recordSymbolLocation(self, symbolId, sourceRange):
		if symbolId in self.symbolIdsToData:
			self.symbolIdsToData[symbolId]['symbol_location'] = sourceRange.toString()


	def recordSymbolScopeLocation(self, symbolId, sourceRange):
		if symbolId in self.symbolIdsToData:
			self.symbolIdsToData[symbolId]['scope_location'] = sourceRange.toString()


	def recordSymbolSignatureLocation(self, symbolId, sourceRange):
		if symbolId in self.symbolIdsToData:
			self.symbolIdsToData[symbolId]['signature_location'] = sourceRange.toString()


	def recordReference(self, contextSymbolId, referencedSymbolId, referenceKind):
		serialized = str(contextSymbolId) + ' -> ' + str(referencedSymbolId) + '[' + str(referenceKind) + ']'
		if serialized in self.serializedReferencesToIds:
			return self.serializedReferencesToIds[serialized]

		referenceId = self.getNextElementId()
		self.serializedReferencesToIds[serialized] = referenceId
		self.referenceIdsToData[referenceId] = {
			'id': referenceId,
			'context_symbol_id': contextSymbolId,
			'referenced_symbol_id': referencedSymbolId,
			'reference_kind': referenceKindToString(referenceKind),
			'reference_location': []
		}
		return referenceId


	def recordReferenceLocation(self, referenceId, sourceRange):
		if referenceId in self.referenceIdsToData:
			self.referenceIdsToData[referenceId]['reference_location'].append(sourceRange.toString())


	def recordReferenceIsAmbiguous(self, referenceId):
		raise NotImplementedError


	def recordReferenceToUnsolvedSymhol(self, contextSymbolId, referenceKind, sourceRange):
		referencedSymbolId = self.recordSymbol(getNameHierarchyForUnsolvedSymbol())
		referenceId = self.recordReference(contextSymbolId, referencedSymbolId, referenceKind)
		self.recordReferenceLocation(referenceId, sourceRange)
		return referenceId


	def recordQualifierLocation(self, referencedSymbolId, sourceRange):
		if referencedSymbolId not in self.qualifierIdsToData:
			self.qualifierIdsToData[referencedSymbolId] = {
				'id': referencedSymbolId,
				'qualifier_locations': []
			}
		self.qualifierIdsToData[referencedSymbolId]['qualifier_locations'].append(sourceRange.toString())


	def recordFile(self, filePath):
		serialized = filePath

		if serialized in self.serializedSymbolsToIds:
			return self.serializedSymbolsToIds[serialized]

		fileId = self.getNextElementId()
		self.serializedSymbolsToIds[serialized] = fileId
		self.symbolIdsToData[fileId] = {
			'id': fileId,
			'name': filePath,
			'symbol_kind': 'FILE',
			'definition_kind': 'INDEXED'
		}
		return fileId


	def recordFileLanguage(self, fileId, languageIdentifier):
		# FIXME: implement this one!
		return


	def recordLocalSymbol(self, name):
		if name in self.serializedLocalSymbolsToIds:
			return self.serializedLocalSymbolsToIds[name]

		localSymbolId = self.getNextElementId()
		self.serializedLocalSymbolsToIds[name] = localSymbolId
		self.localSymbolIdsToData[localSymbolId] = {
			'id': localSymbolId,
			'name': name,
			'local_symbol_locations': []
		}
		return localSymbolId


	def recordLocalSymbolLocation(self, localSymbolId, sourceRange):
		if localSymbolId in self.localSymbolIdsToData:
			self.localSymbolIdsToData[localSymbolId]['local_symbol_locations'].append(sourceRange.toString())


	def recordAtomicSourceRange(self, sourceRange):
		self.atomicSourceRanges.append('ATOMIC SOURCE RANGE: ' + sourceRange.toString())
		return


	def recordError(self, message, fatal, sourceRange):
		errorString = ''
		if fatal:
			errorString += 'FATAL '
		errorString += 'ERROR: "' + message + '" at ' + sourceRange.toString()
		self.errors.append(errorString)
		return

def symbolDefinitionKindToString(symbolDefinitionKind):
	if symbolDefinitionKind == SYMBOL_ANNOTATION:
		return 'EXPLICIT'
	if symbolDefinitionKind == DEFINITION_IMPLICIT:
		return 'IMPLICIT'
	return ''

def symbolKindToString(symbolKind):
	if symbolKind == SYMBOL_TYPE:
		return 'TYPE'
	if symbolKind == SYMBOL_BUILTIN_TYPE:
		return 'BUILTIN_TYPE'
	if symbolKind == SYMBOL_MODULE:
		return 'MODULE'
	if symbolKind == SYMBOL_NAMESPACE:
		return 'NAMESPACE'
	if symbolKind == SYMBOL_PACKAGE:
		return 'PACKAGE'
	if symbolKind == SYMBOL_STRUCT:
		return 'STRUCT'
	if symbolKind == SYMBOL_CLASS:
		return 'CLASS'
	if symbolKind == SYMBOL_INTERFACE:
		return 'INTERFACE'
	if symbolKind == SYMBOL_ANNOTATION:
		return 'ANNOTATION'
	if symbolKind == SYMBOL_GLOBAL_VARIABLE:
		return 'GLOBAL_VARIABLE'
	if symbolKind == SYMBOL_FIELD:
		return 'FIELD'
	if symbolKind == SYMBOL_FUNCTION:
		return 'FUNCTION'
	if symbolKind == SYMBOL_METHOD:
		return 'METHOD'
	if symbolKind == SYMBOL_ENUM:
		return 'ENUM'
	if symbolKind == SYMBOL_ENUM_CONSTANT:
		return 'ENUM_CONSTANT'
	if symbolKind == SYMBOL_TYPEDEF:
		return 'TYPEDEF'
	if symbolKind == SYMBOL_TYPE_PARAMETER:
		return 'TYPE_PARAMETER'
	if symbolKind == SYMBOL_FILE:
		return 'FILE'
	if symbolKind == SYMBOL_MACRO:
		return 'MACRO'
	if symbolKind == SYMBOL_UNION:
		return 'UNION'
	return ''

def referenceKindToString(referenceKind):
	if referenceKind == REFERENCE_TYPE_USAGE:
		return 'TYPE_USAGE'
	if referenceKind == REFERENCE_USAGE:
		return 'USAGE'
	if referenceKind == REFERENCE_CALL:
		return 'CALL'
	if referenceKind == REFERENCE_INHERITANCE:
		return 'INHERITANCE'
	if referenceKind == REFERENCE_OVERRIDE:
		return 'OVERRIDE'
	if referenceKind == REFERENCE_TYPE_ARGUMENT:
		return 'TYPE_ARGUMENT'
	if referenceKind == REFERENCE_TEMPLATE_SPECIALIZATION:
		return 'TEMPLATE_SPECIALIZATION'
	if referenceKind == REFERENCE_INCLUDE:
		return 'INCLUDE'
	if referenceKind == REFERENCE_IMPORT:
		return 'IMPORT'
	if referenceKind == REFERENCE_MACRO_USAGE:
		return 'MACRO_USAGE'
	if referenceKind == REFERENCE_ANNOTATION_USAGE:
		return 'ANNOTATION_USAGE'
	return ''
