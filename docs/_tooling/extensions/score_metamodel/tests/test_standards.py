# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************

from sphinx_needs.data import NeedsInfoType

from docs._tooling.extensions.score_metamodel.checks import standards
from docs._tooling.extensions.score_metamodel.tests import (
    fake_check_logger,
    verify_log_string,
)


class TestStandards:
    def test_check_all_standard_req_linked_item_via_the_compliance_req_positive(self):
        """
        Test if check all_standard_req_linked_item_via_the_compliance_req function will give a False value (check is valid) when giving a standar requirement which is linked to at least one of the list of items that have complies tag via the same tag.
        """

        need_1 = NeedsInfoType(
            target_id="Traceability of safety requirements",
            id="STD_REQ_ISO26262__rq-8-6432",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="GD_REQ__attribute_satisfies",
            tags="attribute",
            security="NO",
            type="gd_req",
            complies=[
                "STD_REQ_ISO26262__rq-8-6432",
                "STD_REQ_ISO26262__rq-8-6422",
            ],
            status="valid",
            satisfies=[
                "GD__create_maintain_requirements",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_all_standard_req_linked_item_via_the_compliance_req(
            needs, logger
        )
        assert not logger.has_warnings

    def test_check_standard_req_linked_item_via_the_compliance_req_negative(self):
        """
        Test if check all_standard_req_linked_item_via_the_compliance_req function will give a False value (check is invalid) when giving a standar requirement which is not linked to at least one of the list of items that have complies tag via the same tag.
        """

        need_1 = NeedsInfoType(
            target_id="Traceability of safety requirements",
            id="STD_REQ_ISO26262__rq-8-6432",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="GD_REQ__attribute_satisfies",
            type="gd_req",
            tags="attribute",
            security="NO",
            complies=[
                "STD_REQ_ISO26262__rq-8-0000",
                "STD_REQ_ISO26262__rq-8-1111",
            ],
            status="valid",
            satisfies=[
                "GD__create_maintain_requirements",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_all_standard_req_linked_item_via_the_compliance_req(
            needs, logger
        )
        assert logger.has_warnings
        verify_log_string(
            logger,
            f"Standard requirement `{need_1['id']}` is not linked to at least one item via the complies tag.",
            expect_location=False,
        )

    def test_check_all_standard_workproducts_linked_item_via_the_compliance_wp_positive(
        self,
    ):
        """
        Test if check all_standard_workproducts_linked_item_via_the_compliance_wp function will give a False value (check is valid) when giving a standar workproduct which is linked to at least one of the list of items that have complies tag via the same tag.
        """

        need_1 = NeedsInfoType(
            target_id="Organization-specific rules and processes for functional safety",
            id="STD_WP_ISO26262__WP-2-551",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="WP_POLICIES",
            id="WP_POLICIES",
            type="workproduct",
            status="draft",
            tags="requirements_management",
            relevant="PH_SPR_PLAN",
            complies=[
                "STD_WP_ISO26262__WP-2-551",
                "STD_REQ_ISO26262__WP-05-01",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_all_standard_workproducts_linked_item_via_the_compliance_wp(
            needs, logger
        )
        assert not logger.has_warnings

    def test_check_standard_workproducts_linked_item_via_the_compliance_wp_negative(
        self,
    ):
        """
        Test if check all_standard_workproducts_linked_item_via_the_compliance_wp function will give a True value (check is invalid) when giving a standar workproduct which is not linked to at least one of the list of items that have complies tag via the same tag.
        """

        need_1 = NeedsInfoType(
            target_id="Organization-specific rules and processes for functional safety",
            id="STD_WP_ISO26262__wp-2-551",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="WP_POLICIES",
            id="WP_POLICIES",
            type="workproduct",
            status="draft",
            complies=[
                "STD_WP_ISO26262__wp-2-777",
                "STD_REQ__iso21434__wp-05-88",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_all_standard_workproducts_linked_item_via_the_compliance_wp(
            needs, logger
        )

        verify_log_string(
            logger,
            f"Standard workproduct `{need_1['id']}` is not linked to at least one item via the complies tag.",
            expect_location=False,
        )

    def test_check_workproduct_uniqueness_over_workflows_positive(self):
        """
        Test if check check_workproduct_uniqueness_over_workflows function will give a False value (check is valid) when giving a workproduct which is linked exactly to one workflow least from the list of all workflows via output option.
        """
        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CR_MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_workproduct_uniqueness_over_workflows(needs, logger)
        assert not logger.has_warnings

    def test_check_workproduct_uniqueness_over_workflows_negative_wprkproduct_not_listed_in_any_workflow(
        self,
    ):
        """
        Test if check check_workproduct_uniqueness_over_workflows function will give a True value (check is invalid) when giving a workproduct which is linked exactly to no workflow from the list of all workflows via output option.
        """

        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            relevant="PH_SPR_PLAN",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CR_MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]

        logger = fake_check_logger()

        standards.check_workproduct_uniqueness_over_workflows(needs, logger)

        verify_log_string(
            logger,
            "is not contained in any workflow, which is incorrect.",
            expect_location=False,
        )

    def test_check_workproduct_uniqueness_over_workflows_negative_wprkproduct_listed_in_multiple_workflows(
        self,
    ):
        """
        Test if check check_workproduct_uniqueness_over_workflows function will give a True value (check is invalid) when giving a workproduct which is linked exactly to more then one workflow from the list of all workflows via output option.
        """

        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF__CR_MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        need_3 = NeedsInfoType(
            target_id="Review/Approve Contribution request",
            type="workflow",
            id="WF_RV_AP_ContrRequest",
            status="valid",
            input=["WP_CONT_REQUEST"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_CONT_REQUEST"],
            contains=[
                "STD_REQ_ISO26262__rq-8-8411",
                "STD_REQ__isoPAS8926__rq-4431",
                "STD_REQ__isoPAS8926__rq-44321",
                "STD_REQ__isoPAS8926__rq-44322",
                "STD_REQ__isoPAS8926__rq-4433",
                "STD_REQ__isoPAS8926__rq-44341",
                "STD_REQ__isoPAS8926__rq-44342",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2, need_3]

        logger = fake_check_logger()

        standards.check_workproduct_uniqueness_over_workflows(needs, logger)

        ids = [need_2["id"], need_3["id"]]
        workflows_str = ", ".join(f"`{id}`" for id in ids)
        verify_log_string(
            logger,
            f"is contained in {2} workflows: {workflows_str}, which is incorrect.",
            expect_location=False,
        )

    def test_my_pie_linked_standard_requirements(self):
        """
        Simulate results  for my_pie_linked_standard_requirements function and check if the result parameter after calling this function a special case will give the correct value.
        """
        needs = {}

        need_1 = NeedsInfoType(
            target_id="Traceability of safety requirements",
            id="STD_REQ_ISO26262__rq-8-6432",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Traceability",
            id="STD_REQ_ISO26262__rq-8-0000",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_3 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="GD_REQ__attribute_satisfies",
            tags="attribute",
            security="NO",
            type="gd_req",
            complies=[
                "STD_REQ_ISO26262__rq-8-6432",
                "STD_REQ_ISO26262__rq-8-6422",
            ],
            status="valid",
            satisfies=[
                "GD__create_maintain_requirements",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2, need_3]

        # Initialize results
        results = []

        # Call the function
        standards.my_pie_linked_standard_requirements(needs, results)

        # Check that results are [1, 1]
        assert results == [
            1,
            1,
        ], f"For function my_pie_linked_standard_requirements expected [1, 1] but got {
                results}"

    def test_my_pie_linked_standard_workproducts(self):
        """
        Simulate results  for test_my_pie_linked_standard_workproducts function and check if the result parameter after calling this function with a special case will give the correct value.
        """

        need_1 = NeedsInfoType(
            target_id="Organization-specific rules and processes for functional safety",
            id="STD_WP_ISO26262__wp-2-551",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="specific rules for processes",
            id="STD_WP_ISO26262__wp-2-0000",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_3 = NeedsInfoType(
            target_id="WP_POLICIES",
            id="WP_POLICIES",
            status="draft",
            type="workproduct",
            complies=[
                "STD_WP_ISO26262__wp-2-551",
                "STD_REQ__iso21434_wp-05-01",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2, need_3]

        # Initialize results
        results = []

        # Call the function
        standards.my_pie_linked_standard_workproducts(needs, results)

        # Check that results are [1, 1]
        assert results == [
            1,
            1,
        ], f"For function my_pie_linked_standard_workproducts expected [1, 1] but got {
                results}"

    def test_my_pie_workproducts_contained_in_exactly_one_workflow(self):
        """
        Simulate results  for test_my_pie_workproducts_contained_in_exactly_one_workflow function and check if the result parameter after calling this function with a special case will give the correct value.
        """

        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CR_MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        need_3 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_4 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_5 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CR_MT_SAFETY",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        need_6 = NeedsInfoType(
            target_id="Review/Approve Contribution request",
            type="workflow",
            id="WF_RV_AP_ContrRequest",
            status="valid",
            input=["WP_CONT_REQUEST"],
            output=["WP_MODULE_SAFETY", "WP_CONT_REQUEST"],
            contains=[
                "STD_REQ_ISO26262__rq-8-8411",
                "STD_REQ__isoPAS8926__rq-4431",
                "STD_REQ__isoPAS8926__rq-44321",
                "STD_REQ__isoPAS8926__rq-44322",
                "STD_REQ__isoPAS8926__rq-4433",
                "STD_REQ__isoPAS8926__rq-44341",
                "STD_REQ__isoPAS8926__rq-44342",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2, need_3, need_4, need_5, need_6]

        # Initialize results
        results = []

        # Call the function
        standards.my_pie_workproducts_contained_in_exactly_one_workflow(needs, results)

        # Check that results are [1, 1]
        assert (
            results == [1, 1, 1]
        ), f"For function my_pie_workproducts_contained_in_exactly_one_workflow expected [1, 1, 1] but got {
                results}"

    def test_get_standards_needs(self):
        """
        Test if get_standards_needs works as expected with a positive and negative test.
        """
        need_1 = NeedsInfoType(
            target_id="Traceability of safety requirements",
            id="STD_REQ_ISO26262__rq-8-6432",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Traceability of requirements",
            id="R_11111111",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_standards_needs(needs)

        assert need_1 in result.values()
        assert need_2 not in result.values()

    def test_get_standards_workproducts(self):
        """
        Test if get_standards_workproducts works as expected with a positive and negative test.
        """
        need_1 = NeedsInfoType(
            target_id="Organization-specific rules and processes for functional safety",
            id="STD_WP_ISO26262__wp-2-551",
            status="valid",
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Traceability of requirements",
            id="R_11111111",
            reqtype="Functional",
            status="valid",
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_standards_workproducts(needs)

        assert need_1 in result.values()
        assert need_2 not in result.values()

    def test_get_compliance_req_needs(self):
        """
        Test if get_compliance_req_needs works as expected with a positive and negative test.
        """

        need_1 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="GD_REQ__attribute_satisfies",
            type="workproduct",
            tags="attribute",
            security="NO",
            complies=[
                "STD_REQ_ISO26262__rq-8-6666",
                "STD_REQ_ISO26262__rq-8-6777",
            ],
            status="valid",
            satisfies=[
                "GD__create_maintain_requirements",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="GD_REQ__attribute_satisfies",
            type="gd_req",
            tags="attribute",
            security="NO",
            complies=[
                "STD_WP_ISO26262__wp-2-551",
                "STD_WP__iso21434_wp-05-01",
            ],
            status="valid",
            satisfies=[
                "GD__create_maintain_requirements",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_compliance_req_needs(needs)

        assert need_1.get("complies", [])[0] not in result
        assert need_2.get("complies", [])[0] in result

    def test_get_compliance_wp_needs(self):
        """
        Test if get_compliance_wp_needs works as expected with a positive and negative test.
        """

        need_1 = NeedsInfoType(
            target_id="Requirements attribute satisfies_1",
            id="GD_REQ__attribute_satisfies",
            type="gd_req",
            tags="attribute",
            security="NO",
            complies=[
                "STD_REQ_ISO26262__rq-8-6432",
                "STD_REQ_ISO26262__rq-8-6422",
            ],
            status="valid",
            satisfies=["GD__create_maintain_requirements"],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Requirements attribute satisfies",
            id="WP__attribute_satisfies_2",
            type="workproduct",
            tags="attribute",
            security="NO",
            complies=[
                "STD_WP_ISO26262__rq-8-6666",
                "STD_WP_ISO26262__rq-8-6777",
            ],
            status="valid",
            satisfies=["GD__create_maintain_requirements"],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_compliance_wp_needs(needs)

        assert need_1.get("complies", [])[0] not in result
        assert need_2.get("complies", [])[0] in result

    def test_get_workflows(self):
        """
        Test if get_workflows works as expected with a positive and negative test.
        """
        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CR_MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_workflows(needs)

        assert need_1 not in result.values()
        assert need_2 in result.values()

    def test_get_workproducts(self):
        """
        Test if get_workproducts works as expected with a positive and negative test.
        """

        need_1 = NeedsInfoType(
            target_id="Module Safety Plan",
            type="workproduct",
            id="WP_MODULE_SAFETY_PLAN",
            status="valid",
            complies=[
                "STD_WP_ISO26262__wp-2-653",
                "STD_WP_ISO26262__wp-8-853",
                "STD_WP_ISO26262__wp-8-1251",
                "STD_WP_ISO26262__wp-8-1252",
            ],
            docname=None,
            lineno=None,
        )

        need_2 = NeedsInfoType(
            target_id="Create/Maintain Safety Plan",
            type="workflow",
            id="WF_CSTD_REQ__MT_SAFETY_PLAN",
            status="draft",
            input=["WP_PLATFORM_MGMT", "WP_ISSUE_TRACK_SYSTEM"],
            output=["WP_MODULE_SAFETY_PLAN", "WP_PLATFORM_SAFETY_PLAN"],
            contains=[
                "STD_REQ_ISO26262__rq-2-6461",
                "STD_REQ_ISO26262__rq-2-6462",
                "STD_REQ_ISO26262__rq-2-6463",
                "STD_REQ_ISO26262__rq-2-6465",
                "STD_REQ_ISO26262__rq-2-6468",
            ],
            docname=None,
            lineno=None,
        )

        needs = [need_1, need_2]
        result = standards.get_workproducts(needs)

        assert need_1 in result.values()
        assert need_2 not in result.values()
