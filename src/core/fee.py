from src.constants.fees import REGULAR_FEES , VIP_FEES

def get_fee_rate(tier: str, role: str) -> float:
    tier = tier.lower()
    role = role.lower()

    if tier in REGULAR_FEES:
        return REGULAR_FEES[tier][role]
    elif tier in VIP_FEES:
        return VIP_FEES[tier][role]
    else:
        raise ValueError(f"Unknown fee tier: {tier}")

def calculate_fee(quantity_usd: float, role: str, tier: str) -> float:
    fee_rate = get_fee_rate(tier, role)
    return quantity_usd * fee_rate
