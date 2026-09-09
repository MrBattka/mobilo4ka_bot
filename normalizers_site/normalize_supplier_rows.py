from typing import Any, Callable

from normalizers_site.hi import normalize_hi_row
from normalizers_site.infinity import normalize_infinity_row
from normalizers_site.mihonor import normalize_mihonor_row
from normalizers_site.vsemi import normalize_vsemi_row
from normalizers_site.superprice import normalize_superprice_row
from normalizers_site.s5 import normalize_s5_row
from normalizers_site.racmag import normalize_racmag_row
from normalizers_site.arti import normalize_arti_row
from normalizers_site.resale import normalize_resale_row
from normalizers_site.f51 import normalize_f51_row
from normalizers_site.miopts import normalize_miopts_row
from normalizers_site.l27 import normalize_l27_row
from normalizers_site.sunrise import normalize_sunrise_row
from normalizers_site.likemob import normalize_likemob_row
from normalizers_site.rootopt import normalize_rootopt_row
from normalizers_site.bogatyr import normalize_bogatyr_row
from normalizers_site.amt import normalize_amt_row
from normalizers_site.unisale import normalize_unisale_row
from normalizers_site.base import normalize_base
from normalizers_site.garmin import (
    normalize_garmin_row,
    normalize_garmin_rows,
)
from normalizers_site.ban_words import row_has_banned_word


def normalize_default(row: list[Any]) -> list[Any]:
    return row


NORMALIZERS: dict[str, Callable[[list[Any]], list[Any]]] = {
    "hi": normalize_hi_row,
    "infinity": normalize_infinity_row,
    "mihonor": normalize_mihonor_row,
    "garmin": normalize_garmin_row,
    "vsemi": normalize_vsemi_row,
    "superprice": normalize_superprice_row,
    "s5": normalize_s5_row,
    "racmag": normalize_racmag_row,
    "arti": normalize_arti_row,
    "resale": normalize_resale_row,
    "f51": normalize_f51_row,
    "miopts": normalize_miopts_row,
    "l27": normalize_l27_row,
    "sunrise": normalize_sunrise_row,
    "likemob": normalize_likemob_row,
    "rootopt": normalize_rootopt_row,
    "bogatyr": normalize_bogatyr_row,
    "amt": normalize_amt_row,
    "unisale": normalize_unisale_row
}


def normalize_supplier_rows(
    normalizer_name: str,
    rows: list[list[Any]],
) -> list[list[Any]]:
    # Garmin обрабатывается целиком
    if normalizer_name == "garmin":
        return [
            row
            for row in normalize_garmin_rows(rows)
            if not row_has_banned_word(row)
        ]

    if normalizer_name == "base":
        result = []

        for row in rows:
            if row_has_banned_word(row):
                continue

            normalized = normalize_base(row)

            if normalized and not row_has_banned_word(normalized):
                result.append(normalized)

        return result

    normalizer = NORMALIZERS.get(normalizer_name, normalize_default)

    result = []

    for row in rows:
        # Проверка исходной строки, включая id
        if row_has_banned_word(row):
            continue

        normalized = normalizer(row)

        # Проверка результата нормализации
        if normalized and not row_has_banned_word(normalized):
            result.append(normalized)

    return result