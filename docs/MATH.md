# The mathematics, step by step

This document follows one trading day through the system and explains the
mathematics at each stage. File names point to the code that implements it.

Notation: $r_{i,t}$ is stock $i$'s return on day $t$, $N$ is the number of
stocks, and $T$ the number of days. "Cross-sectional" means *across stocks on
one day*.

---

## 1. Statistical factors: PCA eigenportfolios
*`qtrade/features/factors.py`*

Stocks move together, mostly because of a few common forces (the market,
sectors, styles). Statistical arbitrage bets on the part of each move that is
**not** explained by those forces.

Take the last $W = 252$ days of returns and standardize each stock:
$Z_{t,i} = (r_{i,t} - \bar r_i)/\sigma_i$. The empirical correlation matrix is
$\rho = \frac{1}{W} Z^\top Z$. Its eigenvectors $v^{(1)}, \dots, v^{(k)}$ (computed
through the SVD of $Z$) are the directions of greatest common variation. Each one
becomes a portfolio with weights $Q_{ij} = v^{(j)}_i / \sigma_i$, called an
*eigenportfolio*. The first is roughly "the market"; the next ones look like
sectors and styles. Their returns are the factors:

$$F_{j,t} = \sum_i Q_{ij}\, r_{i,t}.$$

Regress each stock on the factors over the window,
$r_{i,t} = \alpha_i + \beta_i^\top F_t + \varepsilon_{i,t}$, and on later days define
the **residual** $e_{i,t} = r_{i,t} - \beta_i^\top F_t$. The loadings
$B = [\beta_1 \dots \beta_N]^\top$ are refit monthly. The residuals for the following
month use only the loadings estimated at the refit date, so they use no
future information.

## 2. The Ornstein–Uhlenbeck s-score
*`ou_sscore` in `qtrade/signals/library.py`*

Avellaneda and Lee model the cumulative residual $X_t = \sum_{s \le t} e_s$ as
a mean-reverting Ornstein–Uhlenbeck process:

$$dX_t = \kappa(m - X_t)\,dt + \sigma\, dW_t .$$

In discrete time this is an AR(1), $X_{t+1} = a + b X_t + \eta_{t+1}$, with
$b = e^{-\kappa \Delta t}$. Fitting $a, b$ by rolling OLS over 60 days gives:

$$m = \frac{a}{1-b}, \qquad \sigma_{eq} = \sqrt{\frac{\operatorname{Var}(\eta)}{1-b^2}}, \qquad s = \frac{X_t - m}{\sigma_{eq}} .$$

$s$ measures how many equilibrium standard deviations the stock is from fair
value. The signal is $-s$: buy stocks that are cheap relative to their
factors. It is only used when the half-life $\ln 2 / \kappa$ is under about 30
days ($0 < b < e^{-1/30}$).

A useful detail: subtracting a constant $c$ from every $X_t$ leaves $b$ unchanged
and shifts $m$ by exactly $c$. So $s$ does not depend on where the
cumulative sum starts, and one global running sum can serve every
rolling window.

## 3. Hidden Markov regimes
*`qtrade/models/hmm.py`, `qtrade/models/regime.py`*

The market has hidden states $s_t \in \{1..K\}$ that follow a Markov chain with
$P(s_t = j \mid s_{t-1} = i) = A_{ij}$. We observe symptoms
$x_t$ (market return, log realized volatility, log dispersion, correlation
share), with $x_t \mid s_t = k \sim \mathcal N(\mu_k, \Sigma_k)$.

**Forward recursion (filtering)**: the only part used for trading.

$$\alpha_t(j) \propto \Big[\sum_i \alpha_{t-1}(i) A_{ij}\Big]\, \mathcal N(x_t; \mu_j, \Sigma_j), \qquad \alpha_t(j) = P(s_t = j \mid x_{1:t}).$$

Each step is normalized to sum to 1. The normalizing constants $c_t$ give the
log-likelihood $\log p(x_{1:T}) = \sum_t \log c_t$ without numerical underflow.

**Backward recursion and smoothing**: used only for fitting.
$\beta_t(i) = \sum_j A_{ij}\, \mathcal N(x_{t+1}; \mu_j, \Sigma_j)\, \beta_{t+1}(j) / c_{t+1}$, and
$\gamma_t(k) = P(s_t = k \mid x_{1:T}) \propto \alpha_t(k)\beta_t(k)$.

**Baum–Welch (EM)**: repeat until the likelihood stops improving.

$$\xi_t(i,j) \propto \alpha_t(i) A_{ij}\, \mathcal N(x_{t+1}; \mu_j, \Sigma_j)\, \beta_{t+1}(j)$$
$$A_{ij} \leftarrow \frac{\sum_t \xi_t(i,j)}{\sum_t \sum_j \xi_t(i,j)}, \quad \mu_k \leftarrow \frac{\sum_t \gamma_t(k) x_t}{\sum_t \gamma_t(k)}, \quad \Sigma_k \leftarrow \frac{\sum_t \gamma_t(k)(x_t - \mu_k)(x_t-\mu_k)^\top}{\sum_t \gamma_t(k)}$$

EM only finds a local optimum, so it is run from several starting points
(spread out k-means++-style) and the best likelihood wins. The model is refit
once a year on an expanding window, warm-started from the last fit. States are
sorted by volatility so that "state 0 = calm" keeps the same meaning across
refits. The expected time spent in a regime is $1/(1 - A_{kk})$ days.

## 4. Turning 44 signals into one forecast
*`qtrade/models/combiners.py`, `qtrade/models/walkforward.py`*

**Target.** $y_{i,t}$ is stock $i$'s return from the open of $t+1$ to the open of
$t+1+h$ (with $h = 5$), ranked across stocks and mapped to normal scores
$\Phi^{-1}(\text{rank}/N)$. Ranking removes the market move and tames fat tails.

**Ridge regression.** $\hat b = (X^\top X + \lambda n I)^{-1} X^\top y$, with
$\lambda$ chosen by forecasting the most recent 20% of the training window
from the earlier 80%. A five-day gap separates the two parts, so overlapping
labels can't leak between them.

**Regime ridge.** The features are the products $x_{i,t} \otimes p_t$, where $p_t$ is the
vector of HMM probabilities. The forecast is then
$\sum_k p_{k,t}\, x_{i,t}^\top b_k$: each regime gets its own signal weights,
blended by how sure we are of the regime.

**Kernel ridge with random Fourier features.** The Gaussian kernel
$k(x, x') = e^{-\|x-x'\|^2 / 2\ell^2}$ is the Fourier transform of a Gaussian
(Bochner's theorem). So with $w \sim \mathcal N(0, \ell^{-2} I)$ and
$b \sim U[0, 2\pi]$, the features
$z(x) = \sqrt{2/D}\, \cos(Wx + b)$ satisfy $\mathbb E[z(x)^\top z(x')] = k(x,x')$.
Ridge on $z$ is therefore approximately kernel ridge regression: a nonlinear
model at linear cost.

**IC weighting.** For each signal $j$ and day $t$, the information coefficient
$IC_{j,t} = \operatorname{corr}(x_{\cdot j t}, y_{\cdot t})$. The weight is the
information ratio $\overline{IC}_j / \operatorname{sd}(IC_j)$, shrunk to zero
by the factor $\max(0, 1 - 4/t_j^2)$ when its t-statistic is small.

**Walk-forward.** Models are refit every 63 days on the previous 1,260 days.
The label for day $d$ is only known at the open of $d+1+h$, so a refit on day
$r$ trains on rows $d \le r - 1 - h$. Nothing after $r$ is ever seen.

## 5. From forecast to portfolio
*`qtrade/portfolio/optimizer.py`, `qtrade/portfolio/decider.py`*

**Expected returns: Grinold's formula.** If a forecast's cross-sectional
z-score $z_i$ has information coefficient $IC$, its best linear prediction of
return is

$$\alpha_i = IC \cdot \sigma_i \sqrt{h} \cdot z_i ,$$

where $\sigma_i$ is the stock's daily idiosyncratic volatility. $IC$ is the
model's own *realized* out-of-sample IC over the past year, treated as a
Bayesian average with a prior of 0.01 worth 252 pseudo-days:

$$\widehat{IC} = \max\!\Big(0,\ \frac{\sum_{s} IC_s + 0.01 \cdot 252}{n + 252}\Big).$$

A model whose edge disappears is therefore sized down automatically, to zero
if its IC turns negative.

**Kelly with neutrality.** Maximizing expected log-growth to second order,
$\max_w\ w^\top\alpha - \tfrac12 w^\top \Sigma w$, subject to $C^\top w = 0$ where
$C = [\mathbf 1, B]$ (zero net dollars and zero exposure to every PCA factor).
With the factor model $\Sigma = B F B^\top + D$, the constraint $B^\top w = 0$
cancels the factor term entirely. Using a Lagrangian:

$$w^* = D^{-1}(\alpha - C\lambda), \qquad \lambda = (C^\top D^{-1} C)^{-1} C^\top D^{-1} \alpha .$$

This is a closed form, with no numerical optimizer needed.

**Leverage.** The scale $s = \min(\tfrac12,\ \sigma_{target}/\sigma(w^*),\ G_{max}/\|w^*\|_1)$
combines half-Kelly, a 10% annual volatility target, and the 2× gross cap.
Names over the 2% cap are clipped. The book is projected back onto the
neutral subspace $w \leftarrow w - C(C^\top C)^{-1}C^\top w$, and exposure is
refilled across the uncapped names ("water-filling").

**The no-trade band.** Trading stock $i$ costs about $c_i$ per unit of
weight (spread + slippage + impact). The single-name problem

$$\max_w\ a w - \tfrac{\gamma}{2} d w^2 - c\,|w - w_0|$$

has the solution: keep $w_0$ if it lies in
$\big[\frac{a - c}{\gamma d}, \frac{a + c}{\gamma d}\big]$; otherwise trade to the nearest
edge. Because a position is held for several forecast periods, $c$ is
amortized over $L = 1/(1-\rho)$ periods, where $\rho$ is the rank
autocorrelation between today's forecast and the forecast $h$ days ago.
On the synthetic market, the unscaled band beat both
lighter and heavier cost penalties.

## 6. Costs
*`qtrade/backtest/costs.py`*

Trading $Q$ dollars of a stock with daily volatility $\sigma$ and average daily
dollar volume $V$ costs

$$\text{cost} = |Q|\Big(\text{half-spread} + \text{slippage} + \eta\,\sigma\sqrt{|Q|/V}\Big),$$

where the last term is the empirical *square-root law* of market impact
($\eta = 0.5$). Shorts also pay a 50 bp/yr borrow fee.

## 7. Is the Sharpe ratio real?
*`qtrade/backtest/metrics.py`*

**Probabilistic Sharpe ratio.** Given $n$ daily returns with Sharpe
$\widehat{SR}$, skewness $\gamma_3$ and kurtosis $\gamma_4$:

$$PSR(SR^*) = \Phi\!\left(\frac{(\widehat{SR} - SR^*)\sqrt{n-1}}{\sqrt{1 - \gamma_3 \widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}}\right).$$

**Deflated Sharpe ratio.** Trying $N$ strategies and keeping the best inflates
its Sharpe even when none has skill. The expected maximum Sharpe of $N$
worthless strategies is approximately

$$SR^* = \sqrt{\operatorname{Var}[\widehat{SR}_n]}\left((1-\gamma)\,\Phi^{-1}\!\Big(1 - \tfrac1N\Big) + \gamma\, \Phi^{-1}\!\Big(1 - \tfrac{1}{Ne}\Big)\right),$$

where $\gamma \approx 0.5772$ is the Euler–Mascheroni constant. DSR is $PSR(SR^*)$:
the probability that the chosen strategy beats the best of $N$ duds. The report
computes it from the Sharpe ratios of all seven models it tried.
