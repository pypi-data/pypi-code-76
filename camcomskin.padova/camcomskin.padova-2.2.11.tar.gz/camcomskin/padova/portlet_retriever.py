# -*- coding: utf-8 -*-

from plone.portlets.retriever import PortletRetriever as BasePortletRetriever

class PortletRetriever(BasePortletRetriever):

    def getPortlets(self):
        assignments = super(PortletRetriever, self).getPortlets()
        context = self.context.aq_inner
        path = '/'.join(context.getPhysicalPath())
        context_assignments = []
        new_assignments = []
        for assignment in assignments:
            if assignment.get('category') != 'context':
                new_assignments.append(assignment)
            else:
                if assignment.get('key') == path:
                    context_assignments.append(assignment)
                else:
                    new_assignments.append(assignment)
        new_assignments.extend(context_assignments)
        return new_assignments
