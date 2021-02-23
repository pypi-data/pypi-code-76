#!/usr/bin/env python3

import sys, re, os, uuid, hashlib

from datetime import *

from GoldenChild.xpath import *
from Perdy.pretty import *


#________________________________________________________________
def generateID(text=None):
	"""
	todo: cache uuid based on package path Namespac
	"""
	if text:
		m = hashlib.md5()
		m.update(text.encode('utf8'))
		gobildeegook = m.hexdigest().upper()
	else:
		gobildeegook = uuid.uuid4()
	return f'EDDO_{gobildeegook}'


#________________________________________________________________
class XMI:

	def __init__(self, name=None):
		self.exporter = '$HeadURL: git@github.com:eddo888/Tools/xmi.py $'
		self.version = '$Revision: 11983 $'
		self.timestamp = '%Y-%m-%d %H:%M:%S'

		self.classDiagramStyle = {
			'ShowPrivate': '1',
			'ShowProtected': '1',
			'ShowPublic': '1',
			'HideRelationships': '0',
			'Locked': '0',
			'Border': '1',
			'HighlightForeign': '1',
			'PackageContents': '1',
			'SequenceNotes': '0',
			'ScalePrintImage': '1',
			'PPgs.cx': '1',
			'PPgs.cy': '1',
			'DocSize.cx': '1000',
			'DocSize.cy': '1000',
			'ShowDetails': '0',
			'Orientation': 'P',
			'Zoom': '100',
			'ShowTags': '0',
			'OpParams': '1',
			'VisibleAttributeDetail': '0',
			'ShowOpRetType': '1',
			'ShowIcons': '1',
			'CollabNums': '1',
			'HideProps': '1',
			'ShowReqs': '0',
			'ShowCons': '0',
			'PaperSize': '1',
			'HideParents': '1',
			'UseAlias': '0',
			'HideAtts': '0',
			'HideOps': '0',
			'HideStereo': '0',
			'HideElemStereo': '0',
			'ShowTests': '0',
			'ShowMaint': '0',
			'ConnectorNotation': 'UML 2.1',
			'ExplicitNavigability': '0',
			'AdvancedElementProps': '1',
			'AdvancedFeatureProps': '1',
			'AdvancedConnectorProps': '1',
			'ShowNotes': '0',
			'SuppressBrackets': '0',
			'SuppConnectorLabels': '0',
			'PrintPageHeadFoot': '0',
			'ShowAsList': '0',
		}

		self.activityDiagramStyle = {
			'ShowPrivate': '1',
			'ShowProtected': '1',
			'ShowPublic': '1',
			'HideRelationships': '0',
			'Locked': '0',
			'Border': '1',
			'HighlightForeign': '1',
			'PackageContents': '1',
			'SequenceNotes': '0',
			'ScalePrintImage': '0',
			'PPgs.cx': '1',
			'PPgs.cy': '1',
			'DocSize.cx': '850',
			'DocSize.cy': '1098',
			'ShowDetails': '0',
			'Orientation': 'P',
			'Zoom': '100',
			'ShowTags': '0',
			'OpParams': '1',
			'VisibleAttributeDetail': '0',
			'ShowOpRetType': '1',
			'ShowIcons': '1',
			'CollabNums': '0',
			'HideProps': '0',
			'ShowReqs': '0',
			'ShowCons': '0',
			'PaperSize': '1',
			'HideParents': '0',
			'UseAlias': '0',
			'HideAtts': '0',
			'HideOps': '0',
			'HideStereo': '0',
			'HideElemStereo': '0',
			'ShowTests': '0',
			'ShowMaint': '0',
			'ConnectorNotation': 'UML 2.1',
			'ExplicitNavigability': '0',
			'AdvancedElementProps': '1',
			'AdvancedFeatureProps': '1',
			'AdvancedConnectorProps': '1',
			'ShowNotes': '0',
			'SuppressBrackets': '0',
			'SuppConnectorLabels': '0',
			'PrintPageHeadFoot': '0',
			'ShowAsList': '0',
		}

		self.requirementsDiagramStyle = {
			'ShowPrivate': '1',
			'ShowProtected': '1',
			'ShowPublic': '1',
			'HideRelationships': '0',
			'Locked': '0',
			'Border': '1',
			'HighlightForeign': '1',
			'PackageContents': '1',
			'SequenceNotes': '0',
			'ScalePrintImage': '0',
			'PPgs.cx': '1',
			'PPgs.cy': '1',
			'DocSize.cx': '815',
			'DocSize.cy': '1067',
			'ShowDetails': '0',
			'Orientation': 'P',
			'Zoom': '100',
			'ShowTags': '0',
			'OpParams': '1',
			'VisibleAttributeDetail': '0',
			'ShowOpRetType': '1',
			'ShowIcons': '1',
			'CollabNums': '0',
			'HideProps': '0',
			'ShowReqs': '0',
			'ShowCons': '0',
			'PaperSize': '32512',
			'HideParents': '0',
			'UseAlias': '0',
			'HideAtts': '0',
			'HideOps': '0',
			'HideStereo': '0',
			'HideElemStereo': '0',
			'ShowTests': '0',
			'ShowMaint': '0',
			'ConnectorNotation': 'UML 2.1',
			'ExplicitNavigability': '0',
			'AdvancedElementProps': '1',
			'AdvancedFeatureProps': '1',
			'AdvancedConnectorProps': '1',
			'ShowNotes': '0',
			'SuppressBrackets': '0',
			'SuppConnectorLabels': '0',
			'PrintPageHeadFoot': '0',
			'ShowAsList': '1',
		}

		self.namespaces = {'UML': 'omg.org/UML1.3'}

		self.now = datetime.now()
		self.makeDocument()
		self.makeModel(name)
		self.makeExtensions()
		self.stereotypes = {}
		return

	def makeDocument(self):
		(self.doc, self.ctx, self.nsp) = getContextFromString('<XMI/>')
		for prefix in list(self.namespaces.keys()):
			self.ctx.xpathRegisterNs(prefix, self.namespaces[prefix])
		# version
		self.root = self.doc.getRootElement()
		for prefix in list(self.namespaces.keys()):
			self.root.setProp('xmlns:%s' % prefix, self.namespaces[prefix])
		self.root.setProp('xmi.version', '1.1')
		# timestamp
		self.root.setProp('timestamp', self.now.strftime(self.timestamp))
		# header
		header = addElement(self.doc, 'XMI.header', self.root)
		# documentation
		doco = addElement(self.doc, 'XMI.documentation', header)
		addElementText(self.doc, 'XMI.exporter', self.exporter, doco)
		addElementText(self.doc, 'XMI.exporterVersion', self.version, doco)
		# metamodel
		meta = addElement(self.doc, 'XMI.metamodel', header)
		meta.setProp('xmi.name', 'UML')
		meta.setProp('xmi.version', '1.4')
		return

	def makeModel(self, name=None):
		self.content = addElement(self.doc, 'XMI.content', self.root)
		model = addElement(self.doc, 'UML:Model', self.content)
		model.setProp('isAbstract', 'false')
		model.setProp('isLeaf', 'false')
		model.setProp('isRoot', 'true')
		model.setProp('isSpecification', 'false')
		model.setProp('name', name or self.now.strftime(self.timestamp))
		model.setProp('visibility', 'public')
		model.setProp('xmi.id', generateID(name))
		self.modelNS = addElement(self.doc, 'UML:Namespace.ownedElement', model)
		#self.rootClass = self.makeClass('EARootClass',self.modelNS)
		#self.rootClass.parent.setProp('isRoot','true')
		return

	def makeExtensions(self):
		self.extensions = addElement(self.doc, 'XMI.extensions')
		self.extensions.setProp('xmi.extender', 'Enterprise Architect 2.5')
		self.files = addElement(self.doc, 'EAModel.file', self.extensions)
		return

	def makePackage(self, name, parent, uid=None):
		package = addElement(self.doc, 'UML:Package', parent)
		package.setProp('isAbstract', 'false')
		package.setProp('isLeaf', 'false')
		package.setProp('isRoot', 'true')
		package.setProp('isSpecification', 'false')
		package.setProp('name', name)
		package.setProp('visibility', 'public')
		package.setProp('xmi.id', generateID(uid or name))
		element = addElement(self.doc, 'UML:Namespace.ownedElement', package)
		return element

	def getPackage(self, name, parent, uid=None):
		package = getElement(self.ctx, '*[@name="%s"]' % name, parent)
		if package == None:
			package = self.makePackage(name, parent, uid=uid)
		return package

	def makeCollaboration(self, name, parent, uid=None):
		uid = generateID(uid or name)
		collaboration = addElement(self.doc, 'UML:Collaboration', parent)
		collaboration.setProp('name', name)
		collaboration.setProp('xmi.id', uid)
		return addElement(self.doc, 'UML:Namespace.ownedElement', collaboration)

	def makeRequirement(self, name, parent, uid=None):
		uid = generateID(uid or name)
		requirement = addElement(self.doc, 'UML:ClassifierRole', parent)
		requirement.setProp('isAbstract', 'false')
		requirement.setProp('isLeaf', 'false')
		requirement.setProp('isRoot', 'true')
		requirement.setProp('isSpecification', 'false')
		requirement.setProp('name', name)
		requirement.setProp('visibility', 'public')
		requirement.setProp('xmi.id', uid)
		self.makeLocalTag('stereotype', 'Functional', requirement)
		self.makeLocalTag('ea_eleType', 'element', requirement)
		self.makeLocalTag('ea_stype', 'Requirement', requirement)
		self.makeLocalTag('ea_ntype', '0', requirement)
		return addElement(self.doc, 'UML:Classifier.feature', requirement)

	def makeActor(self, name, parent, uid=None):
		uid = generateID(uid or name)
		actor = addElement(self.doc, 'UML:Actor', parent)
		actor.setProp('isAbstract', 'false')
		actor.setProp('isLeaf', 'false')
		actor.setProp('isRoot', 'true')
		actor.setProp('isSpecification', 'false')
		actor.setProp('name', name)
		actor.setProp('visibility', 'public')
		actor.setProp('xmi.id', uid)
		self.makeLocalTag('ea_eleType', 'element', actor)
		self.makeLocalTag('ea_stype', 'Actor', actor)
		self.makeLocalTag('ea_ntype', '0', actor)
		return addElement(self.doc, 'UML:Classifier.feature', actor)

	def makeUseCase(self, name, parent, uid=None):
		uid = generateID(uid or name)
		useCase = addElement(self.doc, 'UML:UseCase', parent)
		useCase.setProp('isAbstract', 'false')
		useCase.setProp('isLeaf', 'false')
		useCase.setProp('isRoot', 'true')
		useCase.setProp('isSpecification', 'false')
		useCase.setProp('name', name)
		useCase.setProp('visibility', 'public')
		useCase.setProp('xmi.id', uid)
		self.makeLocalTag('ea_eleType', 'element', useCase)
		self.makeLocalTag('ea_stype', 'UseCase', useCase)
		self.makeLocalTag('ea_ntype', '0', useCase)
		return addElement(self.doc, 'UML:Classifier.feature', useCase)

	def makeComponent(self, name, parent, uid=None):
		uid = generateID(uid or name)
		system = addElement(self.doc, 'UML:Component', parent)
		system.setProp('isAbstract', 'false')
		system.setProp('isLeaf', 'false')
		system.setProp('isRoot', 'true')
		system.setProp('isSpecification', 'false')
		system.setProp('name', name)
		system.setProp('visibility', 'public')
		system.setProp('xmi.id', uid)
		self.makeLocalTag('complexity', '1', system)
		self.makeLocalTag('ea_eleType', 'element', system)
		self.makeLocalTag('ea_stype', 'Component', system)
		self.makeLocalTag('ea_ntype', '0', system)
		return addElement(self.doc, 'UML:Classifier.feature', system)

	def makeClass(self, name, parent, uid=None):
		uid = generateID(uid or name)
		clasz = addElement(self.doc, 'UML:Class', parent)
		clasz.setProp('isAbstract', 'false')
		clasz.setProp('isLeaf', 'false')
		clasz.setProp('isRoot', 'true')
		clasz.setProp('isSpecification', 'false')
		clasz.setProp('name', name)
		clasz.setProp('visibility', 'public')
		clasz.setProp('xmi.id', uid)
		self.makeLocalTag('ea_eleType', 'element', clasz)
		return addElement(self.doc, 'UML:Classifier.feature', clasz)

	def assignBaseClass(self, subtype, supertype, parent, uid=None):
		uid = generateID(uid)
		generalized = addElement(self.doc, 'UML:Generalization', parent)
		generalized.setProp('subtype', supertype.parent.prop('xmi.id'))
		generalized.setProp('supertype', subtype.parent.prop('xmi.id'))
		generalized.setProp('visibility', 'public')
		generalized.setProp('xmi.id', uid)
		return

	def makeAttribute(self, name, type, value, parent, tid=None, array=False):
		attribute = addElement(self.doc, 'UML:Attribute', parent)
		attribute.setProp('name', name)
		attribute.setProp('visibility', 'private')
		if array:
			self.makeLocalTag('collection', 'true', attribute)
			self.makeLocalTag('container', '[]', attribute)
		if type:
			tid = type.parent.prop('xmi.id')
		if tid:
			sf = addElement(self.doc, 'UML:StructuralFeature.type', attribute)
			classifier = addElement(self.doc, 'UML:Classifier', sf)
			classifier.setProp('xmi.idref', tid)
		if value:
			av = addElement(self.doc, 'UML:Attribute.initialValue', attribute)
			ue = addElement(self.doc, 'UML:Expression', av)
			ue.setProp('body', value)
		return attribute

	def makeOperation(self, name, parameters, returns, parent, pids={}, rid=None):
		operation = addElement(self.doc, 'UML:Operation', parent)
		operation.setProp('name', name)
		operation.setProp('visibility', 'public')
		bf = addElement(self.doc, 'UML:BehavioralFeature.parameter', operation)
		if parameters:
			pids = {}
			for p in list(parameters.keys()):
				pids[p] = parameters[p].parent.prop('xmi.id')
		for p in list(pids.keys()):
			self.makeParameter(p, None, 'in', bf, tid=pids[p])
		self.makeParameter('return', returns, 'return', bf, tid=rid)
		return

	def makeParameter(self, name, type, kind, parent, tid=None):
		if type:
			tid = type.parent.prop('xmi.id')
		if not tid:
			return
		parameterP = addElement(self.doc, 'UML:Parameter', parent)
		parameterP.setProp('xmi.id', generateID(name))
		parameterP.setProp('name', name)
		parameterP.setProp('kind', kind)
		parameterT = addElement(self.doc, 'UML:Parameter.type', parameterP)
		parameterC = addElement(self.doc, 'UML:Class', parameterT)
		parameterC.setProp('xmi.idref', tid)
		return

	def makeAssociation(self, name, source, target, parent, sid=None, tid=None, array=False):
		if source:
			sid = source.parent.prop('xmi.id')
		if target:
			tid = target.parent.prop('xmi.id')
		association = addElement(self.doc, 'UML:Association', parent)
		association.setProp('name', name)
		association.setProp('xmi.id', generateID())
		association.setProp('visibility', 'public')
		association.setProp('isAbstract', 'false')
		association.setProp('isLeaf', 'false')
		association.setProp('isRoot', 'false')
		# connect em
		connection = addElement(self.doc, 'UML:Association.connection', association)
		# source
		sourceEnd = addElement(self.doc, 'UML:AssociationEnd', connection)
		sourceEnd.setProp('aggregation', 'none')
		sourceEnd.setProp('isNavigable', 'false')
		sourceEnd.setProp('xmi.id', generateID())
		sourceParticipant = addElement(self.doc, 'UML:AssociationEnd.participant',
																																	sourceEnd)
		sourceClass = addElement(self.doc, 'UML:Class', sourceParticipant)
		sourceClass.setProp('xmi.idref', sid)
		#target
		targetEnd = addElement(self.doc, 'UML:AssociationEnd', connection)
		targetEnd.setProp('aggregation', 'none')
		targetEnd.setProp('isNavigable', 'true')
		targetEnd.setProp('xmi.id', generateID())
		if array:
			targetEndMulti = addElement(self.doc, 'UML:AssociationEnd.multiplicity',
																															targetEnd)
			multi = addElement(self.doc, 'UML:Multiplicity', targetEndMulti)
			multi.setProp('xmi.id', generateID())
			multiRangeP = addElement(self.doc, 'UML:Multiplicity.range', multi)
			multiRangeC = addElement(self.doc, 'UML:MultiplicityRange', multiRangeP)
			multiRangeC.setProp('xmi.id', generateID())
			multiRangeC.setProp('lower', '0')
			multiRangeC.setProp('upper', '-1')
		targetParticipant = addElement(self.doc, 'UML:AssociationEnd.participant',
																																	targetEnd)
		targetClass = addElement(self.doc, 'UML:Class', targetParticipant)
		targetClass.setProp('xmi.idref', tid)
		return association

	def makeUsage(self, name, source, target, parent, sid=None, tid=None, array=False):
		if source:
			sid = source.parent.prop('xmi.id')
		if target:
			tid = target.parent.prop('xmi.id')
		association = addElement(self.doc, 'UML:Association', parent)
		association.setProp('name', name)
		association.setProp('xmi.id', generateID())
		association.setProp('visibility', 'public')
		association.setProp('isAbstract', 'false')
		association.setProp('isLeaf', 'false')
		association.setProp('isRoot', 'false')
		self.makeLocalTag('ea_type', 'Usage', association)

		# connect em
		connection = addElement(self.doc, 'UML:Association.connection', association)
		# source
		sourceEnd = addElement(self.doc, 'UML:AssociationEnd', connection)
		sourceEnd.setProp('aggregation', 'none')
		sourceEnd.setProp('isNavigable', 'false')
		sourceEnd.setProp('type', sid)
		self.makeLocalTag('ea_end', 'source', sourceEnd)
		#target
		targetEnd = addElement(self.doc, 'UML:AssociationEnd', connection)
		targetEnd.setProp('aggregation', 'none')
		targetEnd.setProp('isNavigable', 'true')
		targetEnd.setProp('type', tid)
		self.makeLocalTag('ea_end', 'target', targetEnd)
		return association

	def makeObject(self, name, type, parent):
		cr = addElement(self.doc, 'UML:ClassifierRole', parent)
		cr.setProp('name', name)
		cr.setProp('visibility', 'public')
		cr.setProp('xmi.id', generateID(name))
		#cr.setProp('base',self.rootClass.parent.prop('xmi.id'))
		self.makeLocalTag('classifier', type.parent.prop('xmi.id'), cr)
		self.makeLocalTag('classname', type.parent.prop('name'), cr)
		self.makeLocalTag('ea_stype', 'Object', cr)
		return cr

	def makeComment(self, text, parent):
		return

	def makeEAFile(self, path, type, parent):
		flement = addElement(self.doc, 'EAFile', self.files)
		flement.setProp('name', path)
		flement.setProp('type', type)
		flement.setProp('subject', parent.prop('xmi.id'))
		if type == 'Web Address':
			return
		if type == 'Local File':
			self.makeLocalTag('filesize', '%d' % os.path.getsize(path), flement)
			modified = datetime.fromtimestamp(os.path.getmtime(path))
			self.makeLocalTag('timestamp', modified.strftime(self.timestamp), flement)
		return

	def addDocumentation(self, text, parent):
		self.makeLocalTag('documentation', text, parent.parent)

	def makeLocalTag(self, name, value, parent):
		tags = getElement(
			self.ctx, '*[contains(local-name(),"taggedValue")]', parent) or addElement(
				self.doc, 'UML:ModelElement.taggedValue', parent)
		tag = getElement(self.ctx, '*[@tag="%s"]' % name, tags) or addElement(
			self.doc, 'UML:TaggedValue', tags)
		tag.setProp('tag', name)
		tag.setProp('value', value)
		return

	def makeContentTag(self, name, value, parent):
		tag = addElement(self.doc, 'UML:TaggedValue', self.content)
		tag.setProp('xmi.id', generateID())
		tag.setProp('tag', name)
		tag.setProp('value', value)
		tag.setProp('modelElement', parent.parent.prop('xmi.id'))
		return

	def makeStereotype(self, name, parent):
		if not name in list(self.stereotypes.keys()):
			ust = addElement(self.doc, 'UML:Stereotype', self.modelNS)
			ust.setProp('name', name)
			ust.setProp('xmi.id', generateID(name))
			self.stereotypes[name] = ust
		mes = addElement(self.doc, 'UML:ModelElement.stereotype', parent.parent)
		stereotype = addElement(self.doc, 'UML:Stereotype', mes)
		stereotype.setProp('xmi.idref', self.stereotypes[name].prop('xmi.id'))
		return

	def makeActivityModel(self, name, parent):
		model = addElement(self.doc, 'UML:ActivityGraph', parent)
		model.setProp('name', name)
		model.setProp('xmi.id', generateID(name))
		return model

	def makeTransition(self, source, target, parent, name=None):
		transitions = getElement(self.ctx, '*[contains(local-name(),"transitions")]', parent)
		if transitions is None:
			transitions = addElement(self.doc, 'UML:StateMachine.transitions', parent)
		transition = addElement(self.doc, 'UML:Transition', transitions)
		transition.setProp('xmi.id', generateID())
		if name != None:
			transition.setProp('name', name)

		sourceT = addElement(self.doc, 'UML:Transition.source', transition)
		sourceS = addElement(self.doc, source.name, sourceT)
		sourceS.setProp('xmi.idref', source.prop('xmi.id'))

		targetT = addElement(self.doc, 'UML:Transition.target', transition)
		targetS = addElement(self.doc, target.name, targetT)
		targetS.setProp('xmi.idref', target.prop('xmi.id'))

		return transition

	def makeActivitySwimLane(self, name, parent):
		partitions = getElement(self.ctx, '*[contains(local-name(),"partition")]', parent)
		if partitions is None:
			partitions = addElement(self.doc, 'UML:ActivityGraph.partition', parent)
		partition = addElement(self.doc, 'UML:Partition', partitions)
		partition.setProp('name', name)
		partition.setProp('xmi.id', generateID(name))
		return partition

	def addActivityToLane(self, state, parent):
		contents = getElement(self.ctx, '*[contains(local-name(),"contents")]', parent)
		if contents is None:
			contents = addElement(self.doc, 'UML:Partition.contents', parent)
		content = addElement(self.doc, state.name, contents)
		content.setProp('xmi.idref', state.prop('xmi.id'))
		self.makeLocalTag('owner', parent.prop('xmi.id'), state)
		return content

	def makeActivityStartState(self, name, parent, kind=None):
		state = self.makeActivityState(name, 'Pseudostate', parent)
		state.setProp('kind', 'initial')
		return state

	def makeActivityNodeState(self, name, parent):
		state = self.makeActivityState(name, 'ActionState', parent)
		self.makeLocalTag('ea_stype', 'StateNode', state)
		return state

	def makeActivitySwitchState(self, name, parent):
		state = self.makeActivityState(name, 'ActionState', parent)
		state.setProp('kind', 'branch')
		self.makeLocalTag('ea_stype', 'Decision', state)
		return state

	def makeActivityFinishState(self, name, parent, kind=None):
		state = self.makeActivityState(name, 'FinalState', parent)
		return state

	def makeActivityState(self, name, type, parent):
		types = {
			'Pseudostate': 'StateNode',
			'ActionState': 'Action',
			'FinalState': 'Final'
		}
		if type not in list(types.keys()):
			raise Exception('type=%s not in %s' % (type, list(types.keys())))

		top = getElement(self.ctx, '*[contains(local-name(),"top")]', parent)
		if top is None:
			top = addElement(self.doc, 'UML:StateMachine.top', parent)

		cs = getElement(self.ctx, '*[contains(local-name(),"CompositeState")]', top)
		if cs is None:
			cs = addElement(self.doc, 'UML:CompositeState', top)
			cs.setProp('name', 'top')
			cs.setProp('xmi.id', generateID())

		sub = getElement(self.ctx, '*[contains(local-name(),"subvertex")]', cs)
		if sub is None:
			sub = addElement(self.doc, 'UML:CompositeState.subvertex', cs)

		state = addElement(self.doc, 'UML:%s' % type, sub)
		state.setProp('name', name)
		state.setProp('xmi.id', generateID(name))

		return state

	def makeComponentDiagram(self, name, parent):
		diagram = self.makeDiagram(name, parent)
		diagram.parent.setProp('diagramType', 'ComponentDiagram')
		self.makeLocalTag('type', 'Logical', diagram.parent)
		self.makeLocalTag('EAStyle', self.makeStyle(self.classDiagramStyle), diagram.parent)
		return diagram

	def makeClassDiagram(self, name, parent):
		diagram = self.makeDiagram(name, parent)
		diagram.parent.setProp('diagramType', 'ClassDiagram')
		self.makeLocalTag('type', 'Logical', diagram.parent)
		self.makeLocalTag('EAStyle', self.makeStyle(self.classDiagramStyle), diagram.parent)
		return diagram

	def makeActivityDiagram(self, name, parent):
		diagram = self.makeDiagram(name, parent)
		diagram.parent.setProp('diagramType', 'ActivityDiagram')
		self.makeLocalTag('type', 'Activity', diagram.parent)
		self.makeLocalTag('EAStyle', self.makeStyle(self.activityDiagramStyle), diagram.parent)
		return diagram

	def makeRequirementsDiagram(self, name, parent):
		diagram = self.makeDiagram(name, parent)
		diagram.parent.setProp('diagramType', 'CustomDiagram')
		self.makeLocalTag('type', 'Custom', diagram.parent)
		self.makeLocalTag('EAStyle', self.makeStyle(self.requirementsDiagramStyle), diagram.parent)
		return diagram

	def makeUseCaseDiagram(self, name, parent):
		diagram = self.makeDiagram(name, parent)
		diagram.parent.setProp('diagramType', 'UseCaseDiagram')
		self.makeLocalTag('type', 'Logical', diagram.parent)
		self.makeLocalTag('EAStyle', self.makeStyle(self.classDiagramStyle), diagram.parent)
		return diagram

	def makeDiagram(self, name, parent):
		diagram = addElement(self.doc, 'UML:Diagram', self.content)
		diagram.setProp('name', name)
		diagram.setProp('toolName', 'Enterprise Architect 2.5')
		diagram.setProp('xmi.id', generateID())
		diagram.setProp('owner', parent.parent.prop('xmi.id'))
		self.makeLocalTag('package', parent.parent.prop('xmi.id'), diagram)
		elements = addElement(self.doc, 'UML:Diagram.element', diagram)
		return elements

	def addDiagramClass(self, element, parent, geometry=None, style=None):
		self.addDiagramElement(element.parent, parent, geometry, style)

	def addDiagramState(self, element, parent, geometry=None, style=None):
		self.addDiagramElement(element, parent, geometry, style)

	def addDiagramElement(self, element, parent, geometry=None, style=None):
		child = addElement(self.doc, 'UML:DiagramElement', parent)
		child.setProp('subject', element.prop('xmi.id'))
		if geometry != None:
			child.setProp('geometry', geometry)
		if style != None:
			child.setProp('style', style)
		return child

	def makeStyle(self, types):
		style = ''.join(['%s=%s;' % (x, types[x]) for x in list(types.keys())])
		return style


