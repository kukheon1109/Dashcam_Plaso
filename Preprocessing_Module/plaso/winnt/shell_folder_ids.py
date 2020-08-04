# -*- coding: utf-8 -*-
"""This file contains the Windows NT shell folder identifier definitions."""

from __future__ import unicode_literals


# For now ignore the line too long errors.
# pylint: disable=line-too-long

# For now copied from:
# https://code.google.com/p/libfwsi/wiki/ShellFolderIdentifiers

# TODO: store these in a database or equiv.

DESCRIPTIONS = {
    '00020d75-0000-0000-c000-000000000046': 'Inbox',
    '00020d76-0000-0000-c000-000000000046': 'Inbox',
    '00c6d95f-329c-409a-81d7-c46c66ea7f33': 'Default Location',
    '0142e4d0-fb7a-11dc-ba4a-000ffe7ab428': 'Biometric Devices (Biometrics)',
    '025a5937-a6be-4686-a844-36fe4bec8b6d': 'Power Options',
    '031e4825-7b94-4dc3-b131-e946b44c8dd5': 'Users Libraries',
    '04731b67-d933-450a-90e6-4acd2e9408fe': 'Search Folder',
    '05d7b0f4-2121-4eff-bf6b-ed3f69b894d9': 'Taskbar (Notification Area Icons)',
    '0afaced1-e828-11d1-9187-b532f1e9575d': 'Folder Shortcut',
    '0cd7a5c0-9f37-11ce-ae65-08002b2e1262': 'Cabinet File',
    '0df44eaa-ff21-4412-828e-260a8728e7f1': 'Taskbar and Start Menu',
    '11016101-e366-4d22-bc06-4ada335c892b': 'Internet Explorer History and Feeds Shell Data Source for Windows Search',
    '1206f5f1-0569-412c-8fec-3204630dfb70': 'Credential Manager',
    '13e7f612-f261-4391-bea2-39df4f3fa311': 'Windows Desktop Search',
    '15eae92e-f17a-4431-9f28-805e482dafd4': 'Install New Programs (Get Programs)',
    '1723d66a-7a12-443e-88c7-05e1bfe79983': 'Previous Versions Delegate Folder',
    '17cd9488-1228-4b2f-88ce-4298e93e0966': 'Default Programs (Set User Defaults)',
    '1a9ba3a0-143a-11cf-8350-444553540000': 'Shell Favorite Folder',
    '1d2680c9-0e2a-469d-b787-065558bc7d43': 'Fusion Cache',
    '1f3427c8-5c10-4210-aa03-2ee45287d668': 'User Pinned',
    '1f43a58c-ea28-43e6-9ec4-34574a16ebb7': 'Windows Desktop Search MAPI Namespace Extension Class',
    '1f4de370-d627-11d1-ba4f-00a0c91eedba': 'Search Results - Computers (Computer Search Results Folder, Network Computers)',
    '1fa9085f-25a2-489b-85d4-86326eedcd87': 'Manage Wireless Networks',
    '208d2c60-3aea-1069-a2d7-08002b30309d': 'My Network Places',
    '20d04fe0-3aea-1069-a2d8-08002b30309d': 'My Computer',
    '21ec2020-3aea-1069-a2dd-08002b30309d': 'Control Panel',
    '2227a280-3aea-1069-a2de-08002b30309d': 'Printers and Faxes',
    '241d7c96-f8bf-4f85-b01f-e2b043341a4b': 'Workspaces Center (Remote Application and Desktop Connections)',
    '2559a1f0-21d7-11d4-bdaf-00c04f60b9f0': 'Search',
    '2559a1f1-21d7-11d4-bdaf-00c04f60b9f0': 'Help and Support',
    '2559a1f2-21d7-11d4-bdaf-00c04f60b9f0': 'Windows Security',
    '2559a1f3-21d7-11d4-bdaf-00c04f60b9f0': 'Run...',
    '2559a1f4-21d7-11d4-bdaf-00c04f60b9f0': 'Internet',
    '2559a1f5-21d7-11d4-bdaf-00c04f60b9f0': 'E-mail',
    '2559a1f7-21d7-11d4-bdaf-00c04f60b9f0': 'Set Program Access and Defaults',
    '267cf8a9-f4e3-41e6-95b1-af881be130ff': 'Location Folder',
    '26ee0668-a00a-44d7-9371-beb064c98683': 'Control Panel',
    '2728520d-1ec8-4c68-a551-316b684c4ea7': 'Network Setup Wizard',
    '28803f59-3a75-4058-995f-4ee5503b023c': 'Bluetooth Devices',
    '289978ac-a101-4341-a817-21eba7fd046d': 'Sync Center Conflict Folder',
    '289af617-1cc3-42a6-926c-e6a863f0e3ba': 'DLNA Media Servers Data Source',
    '2965e715-eb66-4719-b53f-1672673bbefa': 'Results Folder',
    '2e9e59c0-b437-4981-a647-9c34b9b90891': 'Sync Setup Folder',
    '2f6ce85c-f9ee-43ca-90c7-8a9bd53a2467': 'File History Data Source',
    '3080f90d-d7ad-11d9-bd98-0000947b0257': 'Show Desktop',
    '3080f90e-d7ad-11d9-bd98-0000947b0257': 'Window Switcher',
    '323ca680-c24d-4099-b94d-446dd2d7249e': 'Common Places',
    '328b0346-7eaf-4bbe-a479-7cb88a095f5b': 'Layout Folder',
    '335a31dd-f04b-4d76-a925-d6b47cf360df': 'Backup and Restore Center',
    '35786d3c-b075-49b9-88dd-029876e11c01': 'Portable Devices',
    '36eef7db-88ad-4e81-ad49-0e313f0c35f8': 'Windows Update',
    '3c5c43a3-9ce9-4a9b-9699-2ac0cf6cc4bf': 'Configure Wireless Network',
    '3f6bc534-dfa1-4ab4-ae54-ef25a74e0107': 'System Restore',
    '4026492f-2f69-46b8-b9bf-5654fc07e423': 'Windows Firewall',
    '418c8b64-5463-461d-88e0-75e2afa3c6fa': 'Explorer Browser Results Folder',
    '4234d49b-0245-4df3-b780-3893943456e1': 'Applications',
    '437ff9c0-a07f-4fa0-af80-84b6c6440a16': 'Command Folder',
    '450d8fba-ad25-11d0-98a8-0800361b1103': 'My Documents',
    '48e7caab-b918-4e58-a94d-505519c795dc': 'Start Menu Folder',
    '5399e694-6ce5-4d6c-8fce-1d8870fdcba0': 'Control Panel command object for Start menu and desktop',
    '58e3c745-d971-4081-9034-86e34b30836a': 'Speech Recognition Options',
    '59031a47-3f72-44a7-89c5-5595fe6b30ee': 'Shared Documents Folder (Users Files)',
    '5ea4f148-308c-46d7-98a9-49041b1dd468': 'Mobility Center Control Panel',
    '60632754-c523-4b62-b45c-4172da012619': 'User Accounts',
    '63da6ec0-2e98-11cf-8d82-444553540000': 'Microsoft FTP Folder',
    '640167b4-59b0-47a6-b335-a6b3c0695aea': 'Portable Media Devices',
    '645ff040-5081-101b-9f08-00aa002f954e': 'Recycle Bin',
    '64693913-1c21-4f30-a98f-4e52906d3b56': 'CLSID_AppInstanceFolder',
    '67718415-c450-4f3c-bf8a-b487642dc39b': 'Windows Features',
    '6785bfac-9d2d-4be5-b7e2-59937e8fb80a': 'Other Users Folder',
    '67ca7650-96e6-4fdd-bb43-a8e774f73a57': 'Home Group Control Panel (Home Group)',
    '692f0339-cbaa-47e6-b5b5-3b84db604e87': 'Extensions Manager Folder',
    '6dfd7c5c-2451-11d3-a299-00c04f8ef6af': 'Folder Options',
    '7007acc7-3202-11d1-aad2-00805fc1270e': 'Network Connections (Network and Dial-up Connections)',
    '708e1662-b832-42a8-bbe1-0a77121e3908': 'Tree property value folder',
    '71d99464-3b6b-475c-b241-e15883207529': 'Sync Results Folder',
    '72b36e70-8700-42d6-a7f7-c9ab3323ee51': 'Search Connector Folder',
    '78f3955e-3b90-4184-bd14-5397c15f1efc': 'Performance Information and Tools',
    '7a9d77bd-5403-11d2-8785-2e0420524153': 'User Accounts (Users and Passwords)',
    '7b81be6a-ce2b-4676-a29e-eb907a5126c5': 'Programs and Features',
    '7bd29e00-76c1-11cf-9dd0-00a0c9034933': 'Temporary Internet Files',
    '7bd29e01-76c1-11cf-9dd0-00a0c9034933': 'Temporary Internet Files',
    '7be9d83c-a729-4d97-b5a7-1b7313c39e0a': 'Programs Folder',
    '8060b2e3-c9d7-4a5d-8c6b-ce8eba111328': 'Proximity CPL',
    '8343457c-8703-410f-ba8b-8b026e431743': 'Feedback Tool',
    '85bbd920-42a0-1069-a2e4-08002b30309d': 'Briefcase',
    '863aa9fd-42df-457b-8e4d-0de1b8015c60': 'Remote Printers',
    '865e5e76-ad83-4dca-a109-50dc2113ce9a': 'Programs Folder and Fast Items',
    '871c5380-42a0-1069-a2ea-08002b30309d': 'Internet Explorer (Homepage)',
    '87630419-6216-4ff8-a1f0-143562d16d5c': 'Mobile Broadband Profile Settings Editor',
    '877ca5ac-cb41-4842-9c69-9136e42d47e2': 'File Backup Index',
    '88c6c381-2e85-11d0-94de-444553540000': 'ActiveX Cache Folder',
    '896664f7-12e1-490f-8782-c0835afd98fc': 'Libraries delegate folder that appears in Users Files Folder',
    '8e908fc9-becc-40f6-915b-f4ca0e70d03d': 'Network and Sharing Center',
    '8fd8b88d-30e1-4f25-ac2b-553d3d65f0ea': 'DXP',
    '9113a02d-00a3-46b9-bc5f-9c04daddd5d7': 'Enhanced Storage Data Source',
    '93412589-74d4-4e4e-ad0e-e0cb621440fd': 'Font Settings',
    '9343812e-1c37-4a49-a12e-4b2d810d956b': 'Search Home',
    '96437431-5a90-4658-a77c-25478734f03e': 'Server Manager',
    '96ae8d84-a250-4520-95a5-a47a7e3c548b': 'Parental Controls',
    '98d99750-0b8a-4c59-9151-589053683d73': 'Windows Search Service Media Center Namespace Extension Handler',
    '98f275b4-4fff-11e0-89e2-7b86dfd72085': 'CLSID_StartMenuLauncherProviderFolder',
    '992cffa0-f557-101a-88ec-00dd010ccc48': 'Network Connections (Network and Dial-up Connections)',
    '9a096bb5-9dc3-4d1c-8526-c3cbf991ea4e': 'Internet Explorer RSS Feeds Folder',
    '9c60de1e-e5fc-40f4-a487-460851a8d915': 'AutoPlay',
    '9c73f5e5-7ae7-4e32-a8e8-8d23b85255bf': 'Sync Center Folder',
    '9db7a13c-f208-4981-8353-73cc61ae2783': 'Previous Versions',
    '9f433b7c-5f96-4ce1-ac28-aeaa1cc04d7c': 'Security Center',
    '9fe63afd-59cf-4419-9775-abcc3849f861': 'System Recovery (Recovery)',
    'a00ee528-ebd9-48b8-944a-8942113d46ac': 'CLSID_StartMenuCommandingProviderFolder',
    'a3c3d402-e56c-4033-95f7-4885e80b0111': 'Previous Versions Results Delegate Folder',
    'a5a3563a-5755-4a6f-854e-afa3230b199f': 'Library Folder',
    'a5e46e3a-8849-11d1-9d8c-00c04fc99d61': 'Microsoft Browser Architecture',
    'a6482830-08eb-41e2-84c1-73920c2badb9': 'Removable Storage Devices',
    'a8a91a66-3a7d-4424-8d24-04e180695c7a': 'Device Center (Devices and Printers)',
    'aee2420f-d50e-405c-8784-363c582bf45a': 'Device Pairing Folder',
    'afdb1f70-2a4c-11d2-9039-00c04f8eeb3e': 'Offline Files Folder',
    'b155bdf8-02f0-451e-9a26-ae317cfd7779': 'Delegate folder that appears in Computer',
    'b2952b16-0e07-4e5a-b993-58c52cb94cae': 'DB Folder',
    'b4fb3f98-c1ea-428d-a78a-d1f5659cba93': 'Other Users Folder',
    'b98a2bea-7d42-4558-8bd1-832f41bac6fd': 'Backup And Restore (Backup and Restore Center)',
    'bb06c0e4-d293-4f75-8a90-cb05b6477eee': 'System',
    'bb64f8a7-bee7-4e1a-ab8d-7d8273f7fdb6': 'Action Center Control Panel',
    'bc476f4c-d9d7-4100-8d4e-e043f6dec409': 'Microsoft Browser Architecture',
    'bc48b32f-5910-47f5-8570-5074a8a5636a': 'Sync Results Delegate Folder',
    'bd84b380-8ca2-1069-ab1d-08000948f534': 'Microsoft Windows Font Folder',
    'bdeadf00-c265-11d0-bced-00a0c90ab50f': 'Web Folders',
    'be122a0e-4503-11da-8bde-f66bad1e3f3a': 'Windows Anytime Upgrade',
    'bf782cc9-5a52-4a17-806c-2a894ffeeac5': 'Language Settings',
    'c291a080-b400-4e34-ae3f-3d2b9637d56c': 'UNCFATShellFolder Class',
    'c2b136e2-d50e-405c-8784-363c582bf43e': 'Device Center Initialization',
    'c555438b-3c23-4769-a71f-b6d3d9b6053a': 'Display',
    'c57a6066-66a3-4d91-9eb9-41532179f0a5': 'Application Suggested Locations',
    'c58c4893-3be0-4b45-abb5-a63e4b8c8651': 'Troubleshooting',
    'cb1b7f8c-c50a-4176-b604-9e24dee8d4d1': 'Welcome Center (Getting Started)',
    'd2035edf-75cb-4ef1-95a7-410d9ee17170': 'DLNA Content Directory Data Source',
    'd20ea4e1-3957-11d2-a40b-0c5020524152': 'Fonts',
    'd20ea4e1-3957-11d2-a40b-0c5020524153': 'Administrative Tools',
    'd34a6ca6-62c2-4c34-8a7c-14709c1ad938': 'Common Places FS Folder',
    'd426cfd0-87fc-4906-98d9-a23f5d515d61': 'Windows Search Service Outlook Express Protocol Handler',
    'd4480a50-ba28-11d1-8e75-00c04fa31a86': 'Add Network Place',
    'd450a8a1-9568-45c7-9c0e-b4f9fb4537bd': 'Installed Updates',
    'd555645e-d4f8-4c29-a827-d93c859c4f2a': 'Ease of Access (Ease of Access Center)',
    'd5b1944e-db4e-482e-b3f1-db05827f0978': 'Softex OmniPass Encrypted Folder',
    'd6277990-4c6a-11cf-8d87-00aa0060f5bf': 'Scheduled Tasks',
    'd8559eb9-20c0-410e-beda-7ed416aecc2a': 'Windows Defender',
    'd9ef8727-cac2-4e60-809e-86f80a666c91': 'Secure Startup (BitLocker Drive Encryption)',
    'daf95313-e44d-46af-be1b-cbacea2c3065': 'CLSID_StartMenuProviderFolder',
    'dffacdc5-679f-4156-8947-c5c76bc0b67f': 'Delegate folder that appears in Users Files Folder',
    'e17d4fc0-5564-11d1-83f2-00a0c90dc849': 'Search Results Folder',
    'e211b736-43fd-11d1-9efb-0000f8757fcd': 'Scanners and Cameras',
    'e345f35f-9397-435c-8f95-4e922c26259e': 'CLSID_StartMenuPathCompleteProviderFolder',
    'e413d040-6788-4c22-957e-175d1c513a34': 'Sync Center Conflict Delegate Folder',
    'e773f1af-3a65-4866-857d-846fc9c4598a': 'Shell Storage Folder Viewer',
    'e7de9b1a-7533-4556-9484-b26fb486475e': 'Network Map',
    'e7e4bc40-e76a-11ce-a9bb-00aa004ae837': 'Shell DocObject Viewer',
    'e88dcce0-b7b3-11d1-a9f0-00aa0060fa31': 'Compressed Folder',
    'e95a4861-d57a-4be1-ad0f-35267e261739': 'Windows SideShow',
    'e9950154-c418-419e-a90a-20c5287ae24b': 'Sensors (Location and Other Sensors)',
    'ed50fc29-b964-48a9-afb3-15ebb9b97f36': 'PrintHood delegate folder',
    'ed7ba470-8e54-465e-825c-99712043e01c': 'All Tasks',
    'ed834ed6-4b5a-4bfe-8f11-a626dcb6a921': 'Personalization Control Panel',
    'edc978d6-4d53-4b2f-a265-5805674be568': 'Stream Backed Folder',
    'f02c1a0d-be21-4350-88b0-7367fc96ef3c': 'Computers and Devices',
    'f1390a9a-a3f4-4e5d-9c5f-98f3bd8d935c': 'Sync Setup Delegate Folder',
    'f3f5824c-ad58-4728-af59-a1ebe3392799': 'Sticky Notes Namespace Extension for Windows Desktop Search',
    'f5175861-2688-11d0-9c5e-00aa00a45957': 'Subscription Folder',
    'f6b6e965-e9b2-444b-9286-10c9152edbc5': 'History Vault',
    'f8c2ab3b-17bc-41da-9758-339d7dbf2d88': 'Previous Versions Results Folder',
    'f90c627b-7280-45db-bc26-cce7bdd620a4': 'All Tasks',
    'f942c606-0914-47ab-be56-1321b8035096': 'Storage Spaces',
    'fb0c9c8a-6c50-11d1-9f1d-0000f8757fcd': 'Scanners & Cameras',
    'fbf23b42-e3f0-101b-8488-00aa003e56f8': 'Internet Explorer',
    'fe1290f0-cfbd-11cf-a330-00aa00c16e65': 'Directory',
    'ff393560-c2a7-11cf-bff4-444553540000': 'History',
}