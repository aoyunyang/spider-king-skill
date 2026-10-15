#!/usr/bin/env python3
"""Evaluate secret-free protocol fixtures and their negative controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _bounded_input import BoundedInputError, parse_json_text, read_utf8_text  # noqa: E402


class FixtureError(ValueError):
    pass


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FixtureError(f"{label} must be an object")
    return value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise FixtureError(f"{label} must be a non-empty string")
    return value


def _transport_key(row: dict[str, Any]) -> tuple[str, str]:
    transport = _require_dict(row.get("transport"), "row.transport")
    version = transport.get("httpVersion")
    alpn = transport.get("alpn")
    if not isinstance(version, str) or not version:
        raise FixtureError("row.transport.httpVersion must be a non-empty string")
    if not isinstance(alpn, str) or not alpn:
        raise FixtureError("row.transport.alpn must be a non-empty string")
    return version, alpn


def _business_oracle(row: dict[str, Any], label: str = "row.result") -> bool:
    result = _require_dict(row.get("result"), label)
    value = result.get("businessOracle")
    if not isinstance(value, bool):
        raise FixtureError(f"{label}.businessOracle must be boolean")
    return value


def _payload_class(row: dict[str, Any], label: str) -> str:
    result = _require_dict(row.get("result"), label)
    return _require_text(result.get("payloadClass"), f"{label}.payloadClass")


def _http_status_class(row: dict[str, Any], label: str) -> str:
    result = _require_dict(row.get("result"), label)
    return _require_text(result.get("httpStatusClass"), f"{label}.httpStatusClass")


def _scope_boundary(root: dict[str, Any]) -> None:
    boundary = _require_dict(root.get("scopeBoundary"), "scopeBoundary")
    stops_when = boundary.get("stopsWhen")
    if boundary.get("routeLocal") is not True:
        raise FixtureError("scopeBoundary.routeLocal must be true")
    if not isinstance(stops_when, list) or len(stops_when) < 2:
        raise FixtureError("scopeBoundary.stopsWhen needs at least two conditions")
    if any(not isinstance(item, str) or not item for item in stops_when):
        raise FixtureError("scopeBoundary.stopsWhen items must be non-empty strings")


def evaluate_transport_admission(root: dict[str, Any]) -> dict[str, Any]:
    rows = root.get("rows")
    if not isinstance(rows, list) or len(rows) < 2:
        raise FixtureError("fixture.rows must contain at least two rows")
    typed_rows = [_require_dict(row, f"rows[{index}]") for index, row in enumerate(rows)]
    by_profile: dict[str, dict[str, Any]] = {}
    by_transport: dict[tuple[str, str], dict[str, Any]] = {}
    for row in typed_rows:
        profile = row.get("profile")
        if not isinstance(profile, str) or not profile:
            raise FixtureError("each row.profile must be a non-empty string")
        if profile in by_profile:
            raise FixtureError(f"duplicate profile: {profile}")
        key = _transport_key(row)
        if key in by_transport:
            raise FixtureError(f"duplicate transport profile: {key}")
        by_profile[profile] = row
        by_transport[key] = row

    try:
        plain = by_profile["plain-client"]
        admitted = by_profile["admitted-client"]
    except KeyError as exc:
        raise FixtureError("plain-client and admitted-client rows are required") from exc
    if _business_oracle(plain):
        raise FixtureError("plain-client must fail the business oracle")
    if not _business_oracle(admitted):
        raise FixtureError("admitted-client must pass the business oracle")
    if _transport_key(plain) == _transport_key(admitted):
        raise FixtureError("positive and negative rows must use different transports")

    mutated_key = _transport_key(plain)
    mutated_result = by_transport[mutated_key]
    if _business_oracle(mutated_result):
        raise FixtureError("negative transport mutation did not fail the business oracle")

    _scope_boundary(root)
    return {
        "ok": True,
        "positiveOracle": True,
        "negativeControl": True,
        "admittedTransport": list(_transport_key(admitted)),
        "rejectedTransport": list(mutated_key),
        "routeLocal": True,
    }


def evaluate_page_local_exception(root: dict[str, Any]) -> dict[str, Any]:
    rows = root.get("rows")
    if not isinstance(rows, list) or len(rows) < 2:
        raise FixtureError("fixture.rows must contain at least two rows")
    typed_rows = [_require_dict(row, f"rows[{index}]") for index, row in enumerate(rows)]
    by_profile: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(typed_rows):
        profile = _require_text(row.get("profile"), f"rows[{index}].profile")
        if profile in by_profile:
            raise FixtureError(f"duplicate profile: {profile}")
        _require_text(row.get("pagePredicate"), f"rows[{index}].pagePredicate")
        _require_text(row.get("requestProfile"), f"rows[{index}].requestProfile")
        by_profile[profile] = row

    try:
        ordinary = by_profile["ordinary-request"]
        exception = by_profile["exception-request"]
    except KeyError as exc:
        raise FixtureError("ordinary-request and exception-request rows are required") from exc

    ordinary_page = ordinary.get("pagePredicate")
    exception_page = exception.get("pagePredicate")
    if ordinary_page != exception_page:
        raise FixtureError("ordinary and exception rows must share pagePredicate")
    if ordinary_page == "earlier-page":
        raise FixtureError("exception pagePredicate must not be earlier-page")
    if ordinary.get("requestProfile") == exception.get("requestProfile"):
        raise FixtureError("ordinary and exception rows must use different request profiles")

    if _http_status_class(ordinary, "ordinary-request.result") != "success":
        raise FixtureError("ordinary-request must be an HTTP success-class trap")
    if _http_status_class(exception, "exception-request.result") != "success":
        raise FixtureError("exception-request must be an HTTP success-class accept")
    if _payload_class(ordinary, "ordinary-request.result") != "hint-or-string-array":
        raise FixtureError("ordinary-request payloadClass must be hint-or-string-array")
    if _payload_class(exception, "exception-request.result") != "typed-business-array":
        raise FixtureError("exception-request payloadClass must be typed-business-array")
    if _business_oracle(ordinary, "ordinary-request.result"):
        raise FixtureError("ordinary-request must fail the typed business oracle")
    if not _business_oracle(exception, "exception-request.result"):
        raise FixtureError("exception-request must pass the typed business oracle")

    sibling = _require_dict(root.get("siblingControl"), "siblingControl")
    if sibling.get("pagePredicate") != "earlier-page":
        raise FixtureError("siblingControl.pagePredicate must be earlier-page")
    if sibling.get("requestProfile") != ordinary.get("requestProfile"):
        raise FixtureError("siblingControl must keep the ordinary request profile")
    if _http_status_class(sibling, "siblingControl.result") != "success":
        raise FixtureError("siblingControl must be HTTP success-class")
    if _payload_class(sibling, "siblingControl.result") != "typed-business-array":
        raise FixtureError("siblingControl payloadClass must be typed-business-array")
    if not _business_oracle(sibling, "siblingControl.result"):
        raise FixtureError("siblingControl must pass the typed business oracle")

    if _business_oracle(ordinary, "ordinary-request.result"):
        raise FixtureError("negative page-local mutation did not fail the business oracle")

    _scope_boundary(root)
    return {
        "ok": True,
        "positiveOracle": True,
        "negativeControl": True,
        "routeLocal": True,
        "typeStrict": True,
        "siblingPreserved": True,
    }



JOIN_BUILDERS = {
    "caller": lambda caller, suffix: caller,
    "caller+suffix": lambda caller, suffix: caller + suffix,
    "suffix+caller": lambda caller, suffix: suffix + caller,
}


def evaluate_standard_primitive_concat(root: dict[str, Any]) -> dict[str, Any]:
    primitive = _require_text(root.get("primitive"), "primitive")
    if primitive != "md5":
        raise FixtureError("primitive must be md5 for this fixture family")
    caller = _require_text(root.get("caller"), "caller")
    suffix = _require_text(root.get("constantPoolSuffix"), "constantPoolSuffix")
    captured = _require_text(root.get("capturedDigest"), "capturedDigest")
    if len(captured) != 32 or any(character not in "0123456789abcdef" for character in captured):
        raise FixtureError("capturedDigest must be 32 lowercase hex characters")

    def digest(text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    unsalted = digest(caller)
    concat = digest(caller + suffix)
    if unsalted == captured:
        raise FixtureError("unsalted caller must miss the captured digest")
    if concat != captured:
        raise FixtureError("caller-plus-suffix must match the captured digest")

    rows = root.get("rows")
    if not isinstance(rows, list) or len(rows) < 2:
        raise FixtureError("fixture.rows must contain at least two rows")
    by_profile: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        typed = _require_dict(row, f"rows[{index}]")
        profile = _require_text(typed.get("profile"), f"rows[{index}].profile")
        if profile in by_profile:
            raise FixtureError(f"duplicate profile: {profile}")
        join = _require_text(typed.get("join"), f"rows[{index}].join")
        if join not in JOIN_BUILDERS:
            raise FixtureError(f"rows[{index}].join must be one of {sorted(JOIN_BUILDERS)}")
        matched = typed.get("digestMatchesCaptured")
        oracle = typed.get("oracle")
        if not isinstance(matched, bool):
            raise FixtureError(f"rows[{index}].digestMatchesCaptured must be boolean")
        if not isinstance(oracle, bool):
            raise FixtureError(f"rows[{index}].oracle must be boolean")
        actual = digest(JOIN_BUILDERS[join](caller, suffix)) == captured
        if matched is not actual:
            raise FixtureError(f"rows[{index}] digestMatchesCaptured does not match hashlib")
        if oracle is not actual:
            raise FixtureError(f"rows[{index}] oracle must follow digestMatchesCaptured")
        by_profile[profile] = typed

    try:
        unsalted_row = by_profile["unsalted-caller"]
        concat_row = by_profile["caller-plus-suffix"]
    except KeyError as exc:
        raise FixtureError("unsalted-caller and caller-plus-suffix rows are required") from exc
    if unsalted_row.get("join") != "caller" or unsalted_row.get("digestMatchesCaptured") is not False:
        raise FixtureError("unsalted-caller must miss the captured digest")
    if concat_row.get("join") != "caller+suffix" or concat_row.get("digestMatchesCaptured") is not True:
        raise FixtureError("caller-plus-suffix must match the captured digest")
    if concat_row.get("oracle") is not True or unsalted_row.get("oracle") is not False:
        raise FixtureError("concat row must be the only positive oracle among required rows")

    reversed_row = by_profile.get("suffix-plus-caller")
    if reversed_row is not None:
        if reversed_row.get("join") != "suffix+caller" or reversed_row.get("digestMatchesCaptured") is not False:
            raise FixtureError("suffix-plus-caller must miss unless that join is the captured preimage")

    _scope_boundary(root)
    return {
        "ok": True,
        "positiveOracle": True,
        "negativeControl": True,
        "concatMatched": True,
        "unsaltedMissed": True,
        "joinOrderSensitive": reversed_row is not None,
        "routeLocal": True,
    }




def _require_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise FixtureError(f"{label} must be boolean")
    return value


def evaluate_signer_egress_stub(root: dict[str, Any]) -> dict[str, Any]:
    observed = _require_text(root.get("observedCallsite"), "observedCallsite")
    if observed != "library-ajax":
        raise FixtureError("observedCallsite must be library-ajax for this fixture family")
    continuation = _require_text(root.get("observedContinuation"), "observedContinuation")
    if continuation != "success-and-complete":
        raise FixtureError("observedContinuation must be success-and-complete for this fixture family")

    rows = root.get("rows")
    if not isinstance(rows, list) or len(rows) < 4:
        raise FixtureError("fixture.rows must contain at least four rows")
    by_profile: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        typed = _require_dict(row, f"rows[{index}]")
        profile = _require_text(typed.get("profile"), f"rows[{index}].profile")
        if profile in by_profile:
            raise FixtureError(f"duplicate profile: {profile}")
        wraps = _require_bool(typed.get("wrapsObservedCallsite"), f"rows[{index}].wrapsObservedCallsite")
        fires = _require_bool(typed.get("firesObservedContinuation"), f"rows[{index}].firesObservedContinuation")
        follow = _require_bool(typed.get("followUpIssued"), f"rows[{index}].followUpIssued")
        second = _require_bool(typed.get("secondPageHarvested"), f"rows[{index}].secondPageHarvested")
        oracle = _require_bool(typed.get("oracle"), f"rows[{index}].oracle")
        expected_oracle = wraps and fires and follow and second
        if oracle is not expected_oracle:
            raise FixtureError(
                f"rows[{index}] oracle must follow wraps, continuation, follow-up, and second-page harvest"
            )
        if not wraps and follow:
            raise FixtureError(f"rows[{index}] cannot issue the observed follow-up from a different callsite")
        if wraps and not fires and second:
            raise FixtureError(f"rows[{index}] cannot harvest the second page without the observed continuation")
        by_profile[profile] = typed

    try:
        xhr = by_profile["xhr-send-only"]
        missing = by_profile["ajax-success-without-complete"]
        complete = by_profile["ajax-success-and-complete"]
        returned = by_profile["returned-export-instead-of-ajax-harvest"]
    except KeyError as exc:
        raise FixtureError(
            "xhr-send-only, ajax-success-without-complete, ajax-success-and-complete, "
            "and returned-export-instead-of-ajax-harvest rows are required"
        ) from exc

    if xhr.get("wrapsObservedCallsite") is not False or xhr.get("oracle") is not False:
        raise FixtureError("xhr-send-only must miss the observed callsite and fail the oracle")
    if missing.get("wrapsObservedCallsite") is not True or missing.get("firesObservedContinuation") is not False:
        raise FixtureError("ajax-success-without-complete must wrap the callsite and miss the continuation")
    if missing.get("followUpIssued") is not True or missing.get("oracle") is not False:
        raise FixtureError("ajax-success-without-complete must issue a follow-up and fail the oracle")
    if (
        complete.get("wrapsObservedCallsite") is not True
        or complete.get("firesObservedContinuation") is not True
        or complete.get("followUpIssued") is not True
        or complete.get("secondPageHarvested") is not True
        or complete.get("oracle") is not True
    ):
        raise FixtureError(
            "ajax-success-and-complete must wrap, continue, harvest the second page, and pass the oracle"
        )
    if (
        returned.get("wrapsObservedCallsite") is not False
        or returned.get("firesObservedContinuation") is not False
        or returned.get("followUpIssued") is not False
        or returned.get("secondPageHarvested") is not False
        or returned.get("oracle") is not False
    ):
        raise FixtureError(
            "returned-export-instead-of-ajax-harvest must miss the observed ajax harvest and fail the oracle"
        )

    _scope_boundary(root)
    return {
        "ok": True,
        "positiveOracle": True,
        "negativeControl": True,
        "callsiteMatched": True,
        "continuationRequired": True,
        "returnedExportRejected": True,
        "routeLocal": True,
    }



def evaluate_server_clock_observed_writer(root: dict[str, Any]) -> dict[str, Any]:
    observed = _require_text(root.get("observedWriter"), "observedWriter")
    if observed != "ajax-success":
        raise FixtureError("observedWriter must be ajax-success for this fixture family")

    rows = root.get("rows")
    if not isinstance(rows, list) or len(rows) < 2:
        raise FixtureError("fixture.rows must contain at least two rows")
    by_profile: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        typed = _require_dict(row, f"rows[{index}]")
        profile = _require_text(typed.get("profile"), f"rows[{index}].profile")
        if profile in by_profile:
            raise FixtureError(f"duplicate profile: {profile}")
        injects = _require_bool(typed.get("injectsObservedWriter"), f"rows[{index}].injectsObservedWriter")
        bound = _require_bool(typed.get("requestClockBound"), f"rows[{index}].requestClockBound")
        oracle = _require_bool(typed.get("oracle"), f"rows[{index}].oracle")
        expected_oracle = injects and bound
        if oracle is not expected_oracle:
            raise FixtureError(
                f"rows[{index}] oracle must follow observed-writer inject and request-clock bind"
            )
        if not injects and bound:
            raise FixtureError(f"rows[{index}] cannot bind the request clock without the observed writer")
        by_profile[profile] = typed

    try:
        freeze_only = by_profile["date-now-freeze-only"]
        inject = by_profile["ajax-success-clock-inject"]
    except KeyError as exc:
        raise FixtureError("date-now-freeze-only and ajax-success-clock-inject rows are required") from exc

    if freeze_only.get("injectsObservedWriter") is not False or freeze_only.get("oracle") is not False:
        raise FixtureError("date-now-freeze-only must miss the observed writer and fail the oracle")
    if (
        inject.get("injectsObservedWriter") is not True
        or inject.get("requestClockBound") is not True
        or inject.get("oracle") is not True
    ):
        raise FixtureError(
            "ajax-success-clock-inject must inject the observed writer, bind the request clock, and pass the oracle"
        )

    _scope_boundary(root)
    return {
        "ok": True,
        "positiveOracle": True,
        "negativeControl": True,
        "injectsObservedWriter": True,
        "requestClockBound": True,
        "routeLocal": True,
    }


def evaluate(document: Any) -> dict[str, Any]:
    root = _require_dict(document, "fixture")
    kind = root.get("kind")
    if kind == "transport-admission-matrix":
        return evaluate_transport_admission(root)
    if kind == "page-local-exception-matrix":
        return evaluate_page_local_exception(root)
    if kind == "standard-primitive-concat-matrix":
        return evaluate_standard_primitive_concat(root)
    if kind == "signer-egress-stub-matrix":
        return evaluate_signer_egress_stub(root)
    if kind == "server-clock-observed-writer-matrix":
        return evaluate_server_clock_observed_writer(root)
    raise FixtureError("unsupported fixture.kind")


def _page_local_self_test_fixture() -> dict[str, Any]:
    return {
        "kind": "page-local-exception-matrix",
        "rows": [
            {
                "profile": "ordinary-request",
                "pagePredicate": "exceptional-page",
                "requestProfile": "ordinary",
                "result": {
                    "httpStatusClass": "success",
                    "payloadClass": "hint-or-string-array",
                    "businessOracle": False,
                },
            },
            {
                "profile": "exception-request",
                "pagePredicate": "exceptional-page",
                "requestProfile": "page-local-exception",
                "result": {
                    "httpStatusClass": "success",
                    "payloadClass": "typed-business-array",
                    "businessOracle": True,
                },
            },
        ],
        "siblingControl": {
            "pagePredicate": "earlier-page",
            "requestProfile": "ordinary",
            "result": {
                "httpStatusClass": "success",
                "payloadClass": "typed-business-array",
                "businessOracle": True,
            },
        },
        "scopeBoundary": {"routeLocal": True, "stopsWhen": ["one", "two"]},
    }



def _signer_egress_self_test_fixture() -> dict[str, Any]:
    return {
        "kind": "signer-egress-stub-matrix",
        "observedCallsite": "library-ajax",
        "observedContinuation": "success-and-complete",
        "rows": [
            {
                "profile": "xhr-send-only",
                "wrapsObservedCallsite": False,
                "firesObservedContinuation": False,
                "followUpIssued": False,
                "secondPageHarvested": False,
                "oracle": False,
            },
            {
                "profile": "ajax-success-without-complete",
                "wrapsObservedCallsite": True,
                "firesObservedContinuation": False,
                "followUpIssued": True,
                "secondPageHarvested": False,
                "oracle": False,
            },
            {
                "profile": "ajax-success-and-complete",
                "wrapsObservedCallsite": True,
                "firesObservedContinuation": True,
                "followUpIssued": True,
                "secondPageHarvested": True,
                "oracle": True,
            },
            {
                "profile": "returned-export-instead-of-ajax-harvest",
                "wrapsObservedCallsite": False,
                "firesObservedContinuation": False,
                "followUpIssued": False,
                "secondPageHarvested": False,
                "oracle": False,
            },
        ],
        "scopeBoundary": {"routeLocal": True, "stopsWhen": ["one", "two"]},
    }



def _server_clock_self_test_fixture() -> dict[str, Any]:
    return {
        "kind": "server-clock-observed-writer-matrix",
        "observedWriter": "ajax-success",
        "rows": [
            {
                "profile": "date-now-freeze-only",
                "injectsObservedWriter": False,
                "requestClockBound": False,
                "oracle": False,
            },
            {
                "profile": "ajax-success-clock-inject",
                "injectsObservedWriter": True,
                "requestClockBound": True,
                "oracle": True,
            },
        ],
        "scopeBoundary": {"routeLocal": True, "stopsWhen": ["one", "two"]},
    }


def self_test() -> None:
    transport = {
        "kind": "transport-admission-matrix",
        "rows": [
            {
                "profile": "plain-client",
                "transport": {"httpVersion": "A", "alpn": "a"},
                "result": {"businessOracle": False},
            },
            {
                "profile": "admitted-client",
                "transport": {"httpVersion": "B", "alpn": "b"},
                "result": {"businessOracle": True},
            },
        ],
        "scopeBoundary": {"routeLocal": True, "stopsWhen": ["one", "two"]},
    }
    result = evaluate(transport)
    if not result["positiveOracle"] or not result["negativeControl"]:
        raise RuntimeError("transport positive or negative oracle failed")
    broken_transport = json.loads(json.dumps(transport))
    broken_transport["rows"][0]["result"]["businessOracle"] = True
    try:
        evaluate(broken_transport)
    except FixtureError:
        pass
    else:
        raise RuntimeError("broken transport negative control was accepted")

    page_local = _page_local_self_test_fixture()
    page_result = evaluate(page_local)
    if not page_result["typeStrict"] or not page_result["siblingPreserved"]:
        raise RuntimeError("page-local oracles failed")
    broken_page = json.loads(json.dumps(page_local))
    broken_page["rows"][0]["result"]["businessOracle"] = True
    try:
        evaluate(broken_page)
    except FixtureError:
        pass
    else:
        raise RuntimeError("broken page-local negative control was accepted")
    untyped_accept = json.loads(json.dumps(page_local))
    untyped_accept["rows"][1]["result"]["payloadClass"] = "hint-or-string-array"
    try:
        evaluate(untyped_accept)
    except FixtureError:
        pass
    else:
        raise RuntimeError("HTTP success without typed payload was accepted")
    concat = {
        "kind": "standard-primitive-concat-matrix",
        "primitive": "md5",
        "caller": "abc",
        "constantPoolSuffix": "POOL",
        "capturedDigest": hashlib.md5(b"abcPOOL").hexdigest(),
        "rows": [
            {"profile": "unsalted-caller", "join": "caller", "digestMatchesCaptured": False, "oracle": False},
            {"profile": "caller-plus-suffix", "join": "caller+suffix", "digestMatchesCaptured": True, "oracle": True},
            {"profile": "suffix-plus-caller", "join": "suffix+caller", "digestMatchesCaptured": False, "oracle": False},
        ],
        "scopeBoundary": {"routeLocal": True, "stopsWhen": ["one", "two"]},
    }
    concat_result = evaluate(concat)
    if not concat_result["concatMatched"] or not concat_result["unsaltedMissed"]:
        raise RuntimeError("concat oracles failed")
    broken_concat = json.loads(json.dumps(concat))
    broken_concat["rows"][0]["digestMatchesCaptured"] = True
    broken_concat["rows"][0]["oracle"] = True
    try:
        evaluate(broken_concat)
    except FixtureError:
        pass
    else:
        raise RuntimeError("broken unsalted concat control was accepted")

    stub = _signer_egress_self_test_fixture()
    stub_result = evaluate(stub)
    if (
        not stub_result["callsiteMatched"]
        or not stub_result["continuationRequired"]
        or not stub_result["returnedExportRejected"]
    ):
        raise RuntimeError("signer-egress stub oracles failed")
    broken_stub = json.loads(json.dumps(stub))
    broken_stub["rows"][0]["oracle"] = True
    try:
        evaluate(broken_stub)
    except FixtureError:
        pass
    else:
        raise RuntimeError("broken xhr-send-only oracle was accepted")
    missing_complete = json.loads(json.dumps(stub))
    missing_complete["rows"][1]["secondPageHarvested"] = True
    missing_complete["rows"][1]["oracle"] = True
    try:
        evaluate(missing_complete)
    except FixtureError:
        pass
    else:
        raise RuntimeError("ajax success without complete was accepted")
    broken_returned = json.loads(json.dumps(stub))
    broken_returned["rows"][3]["oracle"] = True
    try:
        evaluate(broken_returned)
    except FixtureError:
        pass
    else:
        raise RuntimeError("returned export harvest was accepted")
    clock = _server_clock_self_test_fixture()
    clock_result = evaluate(clock)
    if not clock_result["injectsObservedWriter"] or not clock_result["requestClockBound"]:
        raise RuntimeError("server-clock observed-writer oracles failed")
    broken_clock = json.loads(json.dumps(clock))
    broken_clock["rows"][0]["oracle"] = True
    try:
        evaluate(broken_clock)
    except FixtureError:
        pass
    else:
        raise RuntimeError("Date.now freeze-only oracle was accepted")
    unbound_clock = json.loads(json.dumps(clock))
    unbound_clock["rows"][1]["injectsObservedWriter"] = False
    unbound_clock["rows"][1]["requestClockBound"] = True
    unbound_clock["rows"][1]["oracle"] = True
    try:
        evaluate(unbound_clock)
    except FixtureError:
        pass
    else:
        raise RuntimeError("request clock bound without observed writer was accepted")
    print("experience_fixture_self_test=PASS")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.fixture is None:
        print("error: fixture path is required", file=sys.stderr)
        return 2
    try:
        document = parse_json_text(read_utf8_text(args.fixture), label=str(args.fixture))
        result = evaluate(document)
    except (BoundedInputError, FixtureError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
