"""Original two-dimensional algebra, not a denoiser or diffusion sampler."""
import math

def number(value, lower, upper, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not lower <= value <= upper or not math.isfinite(value):
        raise ValueError(field + ': expected a finite number in [' + str(lower) + ', ' + str(upper) + ']')
    return float(value)

def vector(value, field):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(field + ': expected exactly two components')
    return [number(v, -10, 10, field + '[' + str(i) + ']') for i, v in enumerate(value)]

def calculate(alpha_bar, x0, epsilon, estimate):
    a = number(alpha_bar, 0.01, 1, 'alpha_bar')
    x0, epsilon, estimate = vector(x0, 'x0'), vector(epsilon, 'epsilon'), vector(estimate, 'estimate')
    signal_coefficient, noise_coefficient = math.sqrt(a), math.sqrt(1-a)
    signal = [signal_coefficient * v for v in x0]
    noise = [noise_coefficient * v for v in epsilon]
    xt = [s+n for s, n in zip(signal, noise)]
    reconstruct = lambda e: [(z-noise_coefficient*v)/signal_coefficient for z,v in zip(xt,e)]
    oracle, predicted = reconstruct(epsilon), reconstruct(estimate)
    error = [p-v for p,v in zip(predicted,x0)]
    mse = sum(v*v for v in error)/2
    estimate_mse = sum((p-v)**2 for p,v in zip(estimate,epsilon))/2
    return dict(alpha_bar=a, x0=x0, epsilon=epsilon, estimate=estimate,
                signal_coefficient=signal_coefficient, noise_coefficient=noise_coefficient,
                signal=signal, noise=noise, xt=xt, oracle=oracle, predicted=predicted,
                error=error, mse=mse, estimate_mse=estimate_mse,
                amplification=math.sqrt((1-a)/a), expected_mse=(1-a)/a*estimate_mse)
