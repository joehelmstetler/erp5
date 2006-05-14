##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLObject import XMLObject
from Products.ERP5.Document.Predicate import Predicate
from Acquisition import aq_base, aq_parent, aq_inner, aq_acquire


class Rule(XMLObject, Predicate):
    """
      Rule objects implement the simulation algorithm
      (expand, solve)

      Example of rules

      - Stock rule (checks stocks)

      - Order rule (copies movements from an order)

      - Capacity rule (makes sure stocks / sources are possible)

      - Transformation rule (expands transformations)

      - Template rule (creates submovements with a template system)
        used in Invoice rule, Paysheet rule, etc.

      Rules are called one by one at the global level (the rules folder)
      and at the local level (applied rules in the simulation folder)

      The simulation_tool includes rules which are parametrized by the sysadmin
      The simulation_tool does the logics of checking, calling, etc.

      simulation_tool is a subclass of Folder & Tool
    """

    # CMF Type Definition
    meta_type = 'ERP5 Rule'
    portal_type = 'Rule'
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)
    
    __implements__ = ( Interface.Predicate,
                       Interface.Rule )

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      )
    
    security.declareProtected(Permissions.AccessContentsInformation,
                              'isAccountable')
    def isAccountable(self, movement):
      """Tells wether generated movement needs to be accounted or not.
      
      Only account movements which are not associated to a delivery;
      Whenever delivery is there, delivery has priority
      """
      return movement.getDeliveryValue() is None

    security.declareProtected(Permissions.ModifyPortalContent,
                              'constructNewAppliedRule')
    def constructNewAppliedRule(self, context, id=None,**kw):
      """
        Creates a new applied rule which points to self
      """
      portal_types = getToolByName(self, 'portal_types')
      if id is None:
        id = context.generateNewId()
      if getattr(aq_base(context), id, None) is None:
        context.newContent(id=id,
                           portal_type='Applied Rule',
                           specialise_value=self,
                           **kw)
      return context.get(id)

    # Simulation workflow
    security.declareProtected(Permissions.ModifyPortalContent, 'expand')
    def expand(self, applied_rule, **kw):
      """
        Expands the current movement downward.

        An applied rule can be expanded only if its parent movement
        is expanded.
      """
      for o in applied_rule.objectValues():
        o.expand(**kw)

    security.declareProtected(Permissions.ModifyPortalContent, 'solve')
    def solve(self, applied_rule, solution_list):
      """
        Solve inconsitency according to a certain number of solutions
        templates. This updates the

        -> new status -> solved

        This applies a solution to an applied rule. Once
        the solution is applied, the parent movement is checked.
        If it does not diverge, the rule is reexpanded. If not,
        diverge is called on the parent movement.
      """

    def test(self, movement):
      """
        Tests if the rule (still) applies to a movement
      """
      return 0

    security.declareProtected(Permissions.ModifyPortalContent, 'diverge')
    def diverge(self, applied_rule):
      """
        -> new status -> diverged

        This basically sets the rule to "diverged"
        and blocks expansion process
      """

    # Solvers
    security.declareProtected(Permissions.View, 'isDivergent')
    def isDivergent(self, applied_rule):
      """
        Returns 1 if divergent rule
      """

    security.declareProtected(Permissions.View, 'getDivergenceList')
    def getDivergenceList(self, applied_rule):
      """
        Returns a list Divergence descriptors
      """

    security.declareProtected(Permissions.View, 'getSolverList')
    def getSolverList(self, applied_rule):
      """
        Returns a list Divergence solvers
      """

    # Deliverability / orderability
    def isOrderable(self, m):
      return 0

    def isDeliverable(self, m):
      return 0

