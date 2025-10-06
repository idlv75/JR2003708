from dragons_and_princesses import Dragon, Princess, get_journey_result


def run_test(name, func):
    try:
        func()
        print(f"[PASS] {name}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")


def test_not_killed_enough_dragons():
    cells = [
        Dragon(2, 5),
        Princess(3, 1),
        Dragon(4, 10),
        Princess(5, 2),
    ]
    gold, killed = get_journey_result(cells)
    if gold != -1:
        raise Exception(f"Expected -1, got {gold}")


def test_reached_last_princess():
    cells = [
        Dragon(2, 5),
        Princess(3, 3),
        Dragon(4, 10),
        Princess(5, 2),
    ]
    gold, killed = get_journey_result(cells)
    if gold != 15:
        raise Exception(f"Expected gold = 15, got {gold}")
    if killed != [2, 4]:
        raise Exception(f"Expected killed=[2,4], got {killed}")


def test_no_dragons():
    cells = [
        Princess(2, 1),
        Princess(3, 2),
    ]
    gold, killed = get_journey_result(cells)
    if gold != -1:
        raise Exception(f"Expected -1, got {gold}")


def test_exact_beauty_match():
    cells = [
        Dragon(2, 10),
        Dragon(3, 20),
        Princess(4, 2),
    ]
    gold, killed = get_journey_result(cells)
    if gold != 30:
        raise Exception(f"Expected gold=30, got {gold}")
    if killed != [2, 3]:
        raise Exception(f"Expected killed=[2,3], got {killed}")

def test_unreachable_final_princess():
    cells = [
        Dragon(2, 10),
        Dragon(3, 12),
        Princess(4, 2),
        Dragon(5, 1),
        Princess(6, 3),
    ]
    gold, killed = get_journey_result(cells)
    if gold != -1:
        raise Exception(f"Expected -1, got {gold}")



if __name__ == "__main__":
    run_test("not killed enough dragons", test_not_killed_enough_dragons)
    run_test("reached last princess", test_reached_last_princess)
    run_test("no dragons", test_no_dragons)
    run_test("exact beauty match", test_exact_beauty_match)
    run_test("unreachable final princess", test_unreachable_final_princess)

