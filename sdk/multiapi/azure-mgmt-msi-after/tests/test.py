#!/usr/bin/env python

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

def test_simple():
    from azure.mgmt.msi import ManagedServiceIdentityClient
    from azure.identity import DefaultAzureCredential
    client = ManagedServiceIdentityClient(credential=DefaultAzureCredential(), api_version="2018-11-30")
    client.operations.list()
    #
    # client = ManagedServiceIdentityClient(credential=DefaultAzureCredential(), api_version="2021-09-30-preview")
    # client.operations.list()
    #
    # client = ManagedServiceIdentityClient(credential=DefaultAzureCredential(), api_version="2022-01-31-preview")
    # client.operations.list()

