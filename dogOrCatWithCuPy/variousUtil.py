import cupy as cp

def lossDiffSquared(out, target):
    out = cp.asarray(out, dtype=cp.float32)
    target = cp.asarray(target, dtype=cp.float32)
    return float(cp.sum((out - target) ** 2))
