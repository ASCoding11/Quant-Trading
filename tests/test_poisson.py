"""The Poisson models recover what was planted in simulated counts."""
import numpy as np

from qtrade.research.poisson import PoissonHMM, fit_ingarch, ingarch_filter


def test_ingarch_recovers_self_excitation():
    rng = np.random.default_rng(0)
    w, a, b = 0.3, 0.35, 0.5
    n, lam = np.zeros(6000), np.zeros(6000)
    lam[0] = w / (1 - a - b)
    for t in range(6000):
        if t:
            lam[t] = w + a * n[t - 1] + b * lam[t - 1]
        n[t] = rng.poisson(lam[t])
    w2, a2, b2 = fit_ingarch(n)
    assert abs(a2 - a) < 0.06 and abs(b2 - b) < 0.1 and abs((a2 + b2) - (a + b)) < 0.04
    # the filter starts from the sample mean; that start-up difference dies out geometrically
    np.testing.assert_allclose(ingarch_filter(n, w, a, b)[200:], lam[200:], rtol=1e-9)


def test_poisson_hmm_recovers_regime_rates():
    rng = np.random.default_rng(1)
    A = np.array([[0.98, 0.02], [0.05, 0.95]])
    rates = np.array([1.0, 8.0])
    s = np.zeros(5000, dtype=int)
    for t in range(1, 5000):
        s[t] = rng.choice(2, p=A[s[t - 1]])
    n = rng.poisson(rates[s]).astype(float)
    hmm = PoissonHMM(2).fit(n)
    np.testing.assert_allclose(hmm.rates, rates, rtol=0.1)
    assert (hmm.filter(n).argmax(axis=1) == s).mean() > 0.95
