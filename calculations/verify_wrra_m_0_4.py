from __future__ import annotations

from fractions import Fraction
import json


Vector = tuple[Fraction, ...]


def vec(*entries: int | Fraction) -> Vector:
    return tuple(Fraction(entry) for entry in entries)


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def sub(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def norm_sq(value: Vector) -> Fraction:
    return dot(value, value)


def compatibility(left: Vector, right: Vector) -> Fraction:
    return -norm_sq(sub(left, right))


def gap_direct(
    first_left: Vector,
    second_left: Vector,
    first_right: Vector,
    second_right: Vector,
) -> Fraction:
    return (
        compatibility(first_left, first_right)
        + compatibility(second_left, second_right)
        - compatibility(first_left, second_right)
        - compatibility(second_left, first_right)
    )


def gap_identity(
    first_left: Vector,
    second_left: Vector,
    first_right: Vector,
    second_right: Vector,
) -> Fraction:
    return 2 * dot(sub(first_left, second_left), sub(first_right, second_right))


def verify_general_identity() -> None:
    rational_cases = [
        (
            vec(1, 2, 3),
            vec(-2, 0, 5),
            vec(4, -1, 2),
            vec(0, 3, -3),
        ),
        (
            vec(Fraction(1, 3), Fraction(2, 5)),
            vec(Fraction(-4, 7), Fraction(3, 2)),
            vec(Fraction(9, 11), Fraction(-5, 13)),
            vec(Fraction(2, 17), Fraction(7, 19)),
        ),
    ]
    for case in rational_cases:
        assert gap_direct(*case) == gap_identity(*case)


def verify_finite_witness() -> None:
    triplet_a = vec(1, 0)
    triplet_b = vec(-1, 0)
    singlet_a = vec(1, 0)
    singlet_b = vec(-1, 0)

    antitriplet_a = vec(0, 1)
    antitriplet_b = vec(0, -1)
    null_singlet = vec(0, 1)
    invariant_singlet = vec(0, -1)

    left_direct = compatibility(triplet_a, singlet_a) + compatibility(triplet_b, singlet_b)
    left_swapped = compatibility(triplet_a, singlet_b) + compatibility(triplet_b, singlet_a)
    right_crossed = compatibility(antitriplet_a, null_singlet) + compatibility(
        antitriplet_b, invariant_singlet
    )
    right_direct = compatibility(antitriplet_a, invariant_singlet) + compatibility(
        antitriplet_b, null_singlet
    )

    delta_left = left_direct - left_swapped
    delta_right = right_crossed - right_direct
    assert delta_left == 8
    assert delta_right == 8

    scores = {
        "F_DX": left_direct + right_crossed,
        "F_XX": left_swapped + right_crossed,
        "F_DD": left_direct + right_direct,
        "F_XD": left_swapped + right_direct,
    }
    assert scores == {
        "F_DX": Fraction(0),
        "F_XX": Fraction(-8),
        "F_DD": Fraction(-8),
        "F_XD": Fraction(-16),
    }
    assert max(scores, key=scores.get) == "F_DX"


def matrix_rank(matrix) -> int:
    rows = [list(map(Fraction, row)) for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [x/divisor for x in rows[rank]]
        for i in range(rank+1, len(rows)):
            factor = rows[i][column]
            rows[i] = [x-factor*y for x,y in zip(rows[i],rows[rank],strict=True)]
        rank += 1
        if rank == len(rows):
            break
    return rank


def verify_null_lift_and_anomaly_preservation() -> None:
    # Calculate rank directly; the two-dimensional pairing witness is separate.
    identity = tuple(tuple(Fraction(int(i == j)) for j in range(16)) for i in range(16))
    assert matrix_rank(identity) == 16
    singular_control = list(identity)
    singular_control[-1] = tuple(Fraction(0) for _ in range(16))
    assert matrix_rank(singular_control) == 15
    # The sixteenth basis vector has unit carrier norm under G_16 = I_16.
    neutral_channel = tuple(Fraction(int(index == 15)) for index in range(16))
    assert norm_sq(neutral_channel) == 1

    # A gauge-neutral singlet contributes zero to the anomaly polynomials.
    hypercharge = Fraction(0)
    color_index = Fraction(0)
    weak_index = Fraction(0)
    contributions = {
        "U1_cubed": hypercharge**3,
        "gravity_U1": hypercharge,
        "SU3_squared_U1": color_index * hypercharge,
        "SU2_squared_U1": weak_index * hypercharge,
        "SU3_cubed": color_index,
        "SU2_global_doublets": weak_index,
    }
    assert all(value == 0 for value in contributions.values())


def main() -> None:
    verify_general_identity()
    verify_finite_witness()
    verify_null_lift_and_anomaly_preservation()
    print(json.dumps({'version':'0.4-r1','status':'PASS',
        'constructed_gaps':[8,8],'scores':[0,-8,-8,-16],
        'computed_identity_rank':16,'computed_singular_control_rank':15,
        'neutral_channel_norm_squared':1,
        'rank_scope':'separate transport Gram example, not the 2D response witness'},indent=2))


if __name__ == "__main__":
    main()
