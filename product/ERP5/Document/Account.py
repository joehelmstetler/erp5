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

from Globals import InitializeClass, PersistentMapping
from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLObject import XMLObject

#from Products.ERP5.Core.MetaNode import MetaNode


#class Account(MetaNode, XMLObject):
class Account(XMLObject):
    """
      An account is an abstract metanode which holds
      currencies. Accounting is implemented through
      categories. For example, a sales movement may be
      written:

        Resource: EUR
        Amount: 200
        source/compte/produit
        destination/compte/client
        client/auchan
        section/coramy

      A purchase movement is written:

        Resource: EUR
        Amount: 200
        source/compte/charge
        destination/compte/fournisseur
        fournisseur/coramy
        section/auchan

      Sections allow to implement simple analytical accounting.
      (at the present stage, category membership is boolean logics.
      at some point, category membership should become fuzzy logics)
    """

    meta_type = 'ERP5 Account'
    portal_type = 'Account'
    add_permission = Permissions.AddPortalContent
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      , PropertySheet.Account
                      , PropertySheet.Arrow
                      )

