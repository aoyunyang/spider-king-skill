from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSPORT_FIXTURE = ROOT / "references" / "experience-fixtures" / "transport-admission-matrix.json"
PAGE_LOCAL_FIXTURE = ROOT / "references" / "experience-fixtures" / "page-local-exception-matrix.json"
CONCAT_FIXTURE = ROOT / "references" / "experience-fixtures" / "standard-primitive-concat-matrix.json"
STUB_FIXTURE = ROOT / "references" / "experience-fixtures" / "signer-egress-stub-matrix.json"
CLOCK_FIXTURE = ROOT / "references" / "experience-fixtures" / "server-clock-observed-writer-matrix.json"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import experience_fixture_check  # noqa: E402


class ExperienceFixtureTests(unittest.TestCase):
    def test_transport_matrix_has_positive_and_negative_business_oracles(self) -> None:
        document = json.loads(TRANSPORT_FIXTURE.read_text(encoding="utf-8"))
        result = experience_fixture_check.evaluate(document)
        self.assertTrue(result["positiveOracle"])
        self.assertTrue(result["negativeControl"])
        self.assertTrue(result["routeLocal"])

    def test_broken_negative_control_is_rejected(self) -> None:
        document = json.loads(TRANSPORT_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][0]["result"]["businessOracle"] = True
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "plain-client"):
            experience_fixture_check.evaluate(document)

    def test_page_local_matrix_has_typed_oracle_and_sibling_control(self) -> None:
        document = json.loads(PAGE_LOCAL_FIXTURE.read_text(encoding="utf-8"))
        result = experience_fixture_check.evaluate(document)
        self.assertTrue(result["positiveOracle"])
        self.assertTrue(result["negativeControl"])
        self.assertTrue(result["typeStrict"])
        self.assertTrue(result["siblingPreserved"])
        self.assertTrue(result["routeLocal"])

    def test_page_local_broken_negative_control_is_rejected(self) -> None:
        document = json.loads(PAGE_LOCAL_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][0]["result"]["businessOracle"] = True
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "ordinary-request"):
            experience_fixture_check.evaluate(document)

    def test_page_local_http_success_without_typed_payload_is_rejected(self) -> None:
        document = json.loads(PAGE_LOCAL_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][1]["result"]["payloadClass"] = "hint-or-string-array"
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "typed-business-array"):
            experience_fixture_check.evaluate(document)


    def test_concat_matrix_requires_unsalted_miss_and_suffix_hit(self) -> None:
        document = json.loads(CONCAT_FIXTURE.read_text(encoding="utf-8"))
        result = experience_fixture_check.evaluate(document)
        self.assertTrue(result["positiveOracle"])
        self.assertTrue(result["negativeControl"])
        self.assertTrue(result["concatMatched"])
        self.assertTrue(result["unsaltedMissed"])
        self.assertTrue(result["joinOrderSensitive"])
        self.assertTrue(result["routeLocal"])

    def test_concat_broken_unsalted_control_is_rejected(self) -> None:
        document = json.loads(CONCAT_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][0]["digestMatchesCaptured"] = True
        document["rows"][0]["oracle"] = True
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "digestMatchesCaptured|unsalted"):
            experience_fixture_check.evaluate(document)

    def test_concat_wrong_captured_digest_is_rejected(self) -> None:
        document = json.loads(CONCAT_FIXTURE.read_text(encoding="utf-8"))
        document["capturedDigest"] = "0" * 32
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "caller-plus-suffix"):
            experience_fixture_check.evaluate(document)

    def test_signer_egress_stub_requires_callsite_and_continuation(self) -> None:
        document = json.loads(STUB_FIXTURE.read_text(encoding="utf-8"))
        result = experience_fixture_check.evaluate(document)
        self.assertTrue(result["positiveOracle"])
        self.assertTrue(result["negativeControl"])
        self.assertTrue(result["callsiteMatched"])
        self.assertTrue(result["continuationRequired"])
        self.assertTrue(result["returnedExportRejected"])
        self.assertTrue(result["routeLocal"])

    def test_signer_egress_xhr_only_oracle_is_rejected(self) -> None:
        document = json.loads(STUB_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][0]["oracle"] = True
        with self.assertRaisesRegex(experience_fixture_check.FixtureError, "oracle must follow|xhr-send-only"):
            experience_fixture_check.evaluate(document)

    def test_signer_egress_success_without_complete_is_rejected(self) -> None:
        document = json.loads(STUB_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][1]["secondPageHarvested"] = True
        with self.assertRaisesRegex(
            experience_fixture_check.FixtureError,
            "second page without the observed continuation",
        ):
            experience_fixture_check.evaluate(document)

    def test_signer_egress_returned_export_oracle_is_rejected(self) -> None:
        document = json.loads(STUB_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][3]["oracle"] = True
        with self.assertRaisesRegex(
            experience_fixture_check.FixtureError,
            "oracle must follow|returned-export-instead-of-ajax-harvest",
        ):
            experience_fixture_check.evaluate(document)

    def test_signer_egress_missing_returned_export_row_is_rejected(self) -> None:
        document = json.loads(STUB_FIXTURE.read_text(encoding="utf-8"))
        document["rows"] = document["rows"][:3]
        with self.assertRaisesRegex(
            experience_fixture_check.FixtureError,
            "at least four rows|returned-export-instead-of-ajax-harvest",
        ):
            experience_fixture_check.evaluate(document)

    def test_server_clock_matrix_requires_observed_writer_inject(self) -> None:
        document = json.loads(CLOCK_FIXTURE.read_text(encoding="utf-8"))
        result = experience_fixture_check.evaluate(document)
        self.assertTrue(result["positiveOracle"])
        self.assertTrue(result["negativeControl"])
        self.assertTrue(result["injectsObservedWriter"])
        self.assertTrue(result["requestClockBound"])
        self.assertTrue(result["routeLocal"])

    def test_server_clock_date_now_freeze_only_oracle_is_rejected(self) -> None:
        document = json.loads(CLOCK_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][0]["oracle"] = True
        with self.assertRaisesRegex(
            experience_fixture_check.FixtureError,
            "oracle must follow|date-now-freeze-only",
        ):
            experience_fixture_check.evaluate(document)

    def test_server_clock_bind_without_observed_writer_is_rejected(self) -> None:
        document = json.loads(CLOCK_FIXTURE.read_text(encoding="utf-8"))
        document["rows"][1]["injectsObservedWriter"] = False
        document["rows"][1]["requestClockBound"] = True
        document["rows"][1]["oracle"] = True
        with self.assertRaisesRegex(
            experience_fixture_check.FixtureError,
            "oracle must follow|without the observed writer",
        ):
            experience_fixture_check.evaluate(document)

    def test_fixtures_are_secret_free_and_have_stop_conditions(self) -> None:
        for path in (TRANSPORT_FIXTURE, PAGE_LOCAL_FIXTURE, CONCAT_FIXTURE, STUB_FIXTURE, CLOCK_FIXTURE):
            text = path.read_text(encoding="utf-8")
            lowered = text.casefold()
            self.assertNotIn("sessionid=", lowered)
            self.assertNotIn("authorization", lowered)
            self.assertNotIn("set-cookie", lowered)
            self.assertNotIn("bearer ", lowered)
            self.assertGreaterEqual(len(json.loads(text)["scopeBoundary"]["stopsWhen"]), 2)


if __name__ == "__main__":
    unittest.main()
