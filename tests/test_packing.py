import json
from string import printable

from hypothesis import assume, given
from hypothesis.strategies import (
    booleans,
    dictionaries,
    floats,
    lists,
    none,
    recursive,
    text,
)

from kropotkin import pack, unpack

json_fixture = recursive(
    none() | booleans() | floats(width=32, allow_nan=False) | text(printable),
    lambda children: lists(children, min_size=1, max_size=4)
    | dictionaries(text(printable), children, min_size=1, max_size=4),
)


@given(json_fixture)
def test_unpack_inverts_pack(j):
    assert unpack(pack(j)) == j


@given(json_fixture)
def test_pack_smaller_than_json_serialise(j):
    packed = pack(j)
    as_json = json.dumps(j)
    # Forgive where pack actually bloats in small cases
    # There is a known issue where if 0.0 64-bit float is used, Python msgpack
    # bloats that to b'\xcb\x00\x00\x00\x00\x00\x00\x00\x00' full IEEE double
    # precision even though converting to int 0 would be equivalent for JSON
    # Clearly, we or msgback can afford to throw away some precision, but for
    # now just tolerate bloat for these edge cases
    assert len(packed) <= len(as_json) or len(packed) - len(as_json) <= 12


@given(json_fixture)
def test_pack_small_for_reasonable_structures(j):
    # About half what IE allows?
    assert len(pack(j)) <= 1024


@given(json_fixture)
def test_appending_to_arrays(j):
    assume(isinstance(j, list))
    # Imagine we previously sent a user to a URL with j encoded
    packed = pack(j)
    # Then the user fetches that URL so we unserialise j back as fresh state data
    data = unpack(packed)
    # Then our service wants to offer a URL to another state with an item appended
    assume("potato" not in data)
    afforded_state = data + ["potato"]

    assert "potato" in unpack(pack(afforded_state))
