# -*- coding: utf-8 -*-
#
#  File: __init__.py
#  Module: ons_productivity_scan_bvr
#
#  Created by cyp@open-net.ch
#  Original code by Nicolas Bessi and Vincent Renaville
#  Copyright (c) 2009 CamptoCamp. All rights reserved.
#
##############################################################################
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
{
    'name' : 'Open-Net productivity: Scan BVR for Invoice',
    'version' : '1.7.02',
    'author' : 'Open Net Sarl',
    'category' : 'Open-Net customizations',
    'description' : """
More for your OpenERP accounting, by Open Net
---------------------------------------------

The 'productivity' modules is a complete family of modules offering improvement for OpenERP.
These modules are maintained by Open Net, Swiss Partner of OpenERP.
These modules are included in our hosting solutions.

**Features list :**
    - This module Will work with C-channel or other OCR scanner
    - It will help you to create an invoice directly from the BVR Code, at this time it works with BVR and BVR+

**Author :** Open Net Sàrl   Industrie 59  1030 Bussigny  Suisse  http://www.open-net.ch

**Contact :** info@open-net.ch

**History :**

V1.x: 2009/Nicolas Bessi and Vincent Renaville (CamptoCamp)

V1.7: 2013-09-23/Cyp
    - Ported to OE V7

    """,
    'website': 'http://www.open-net.ch',
    'images' : [],
    'depends' : ['l10n_ch'],
    'data': [
        'wizard/scan_bvr_view.xml',
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
