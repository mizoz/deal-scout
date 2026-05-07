from deal_scout.extract import infer_prices


def test_infer_percent_and_price():
    price, original, percent = infer_prices("Code Vein II - Deluxe Edition - $11.99 (90% Off)")
    assert price == 11.99
    assert original is None
    assert percent == 90


def test_infer_two_prices():
    price, original, percent = infer_prices("Armaf Club De Nuit $75.00 CAD $29.35 CAD")
    assert price == 29.35
    assert original == 75.00
    assert round(percent or 0) == 61


def test_plain_numbers_are_not_prices():
    price, original, percent = infer_prices("Guess seductive Men 1 review $48.00 CAD $19.95 CAD")
    assert price == 19.95
    assert original == 48.00
    assert round(percent or 0) == 58


def test_cents_are_prices():
    price, original, percent = infer_prices("N95 masks 89 cents each")
    assert price == 0.89
    assert original is None
    assert percent is None


def test_percent_full_is_not_discount():
    price, original, percent = infer_prices("Mancera 120ML EDP preowned 95% full unboxed $116.69 CAD")
    assert price == 116.69
    assert original is None
    assert percent is None
