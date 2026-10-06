def cost_totals(arch):
    """Totals per kind, computed in code (never by the image model)."""
    return {kind: sum(c.usd for c in arch.costs if c.kind == kind) for kind in ("consulting", "aws_monthly")}

totals = cost_totals(arch)
print(f"Consulting (one-time): USD {totals['consulting']:,.0f}")
print(f"AWS (monthly, illustrative estimate): USD {totals['aws_monthly']:,.0f}")
pd.DataFrame([c.model_dump() for c in arch.costs])
