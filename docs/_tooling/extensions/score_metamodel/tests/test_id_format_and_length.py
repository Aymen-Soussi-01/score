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
from unittest.mock import Mock

from sphinx.application import Sphinx
from sphinx_needs.data import NeedsInfoType

from docs._tooling.extensions.score_metamodel.checks.id_format_and_length import (
    check_description,
    check_id_format,
    check_id_length,
    check_id_title_summary,
)
from docs._tooling.extensions.score_metamodel.tests import (
    fake_check_logger,
)


class TestId:
    def test_check_id_format_positive(self):
        """
        Test check_id_length function with a positive case.
        """

        need = NeedsInfoType(
            id="gd_req__attribute_satisfies",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_format(app, need, logger)
        assert not logger.has_warnings

    def test_check_id_format_two_mendatory_substrings_parts_negative(self):
        """
        Test check_id_length function with a negative case.
        """

        need = NeedsInfoType(
            id="gd_req_attribute_satisfies",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_format(app, need, logger)

        logger.assert_warning(
            "expected to consisting of one of these 2 formats:`<Req Type>__<Abbreviations>` or `<Req Type>__<Abbreviations>__<Architectural Element>`.",
            expect_location=False,
        )

    def test_check_id_format_three_mendatory_substrings_parts_negative(self):
        """
        Test check_id_length function with a negative case.
        """

        need = NeedsInfoType(
            id="feat_req__1",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_format(app, need, logger)

        logger.assert_warning(
            "expected to consisting of this format: `<Req Type>__<Abbreviations>__<Architectural Element>`.",
            expect_location=False,
        )

    def test_check_id_length_positive(self):
        """
        Test check_id_length function with a positive case.
        """

        need = NeedsInfoType(
            id="std_req__iso26262__rq_8_6432",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_length(app, need, logger)
        assert not logger.has_warnings

    def test_check_id_length_negative(self):
        """
        Test check_id_length function with a negative case.
        """

        need = NeedsInfoType(
            id="std_req__iso26262__rq_8_6432_0000000000000000000000",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_length(app, need, logger)
        logger.assert_warning(
            f'exceeds the maximum allowed length of 45 characters (current length: {len(need['id'])}).',
            expect_location=False,
        )

    def test_check_id_title_summary_positive(self):
        """
        Test check_id_title_summary function with a positive case.
        """

        need = NeedsInfoType(
            id="std_req__iso26262__rq_8_6432",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_title_summary(app, need, logger)
        assert not logger.has_warnings

    def test_check_id_title_summary_negative(self):
        """
        Test check_id_title_summary function with a negative case.
        """

        need = NeedsInfoType(
            id="gd_req__doc_shall_approver",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_id_title_summary(app, need, logger)
        logger.assert_warning(
            "contains a prohibited word: `shall`. Please revise the ID.",
            expect_location=False,
        )

    def test_check_description_positive(self):
        """
        Test check_description function with a positive case.
        """

        need = NeedsInfoType(
            id="std_req__iso26262__rq_8_6432",
            description="This is the description of the requirement",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_description(app, need, logger)
        assert not logger.has_warnings

    def test_check_description_negative(self):
        """
        Test check_description function with a negative case.
        """

        need = NeedsInfoType(
            id="gd_req__doc_shall_approver",
            description="This is just the description of the requirement",
        )

        logger = fake_check_logger()
        app = Mock(spec=Sphinx)

        check_description(app, need, logger)
        logger.assert_warning(
            "contains a weak word: `just`. Please revise the description.",
            expect_location=False,
        )
