from __future__ import annotations

from fractions import Fraction


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


def verify_null_lift_and_anomaly_preservation() -> None:
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
    print("WRRA-M 0.4 exact verification: PASS")


if __name__ == "__main__":
    main()
