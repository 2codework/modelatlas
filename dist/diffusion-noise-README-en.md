# Diffusion noise and prediction error

Prerequisites: two-dimensional vectors, square roots and mean squared error (MSE). Outcome: compute a forward noisy signal, distinguish oracle inversion from a supplied wrong estimate, and explain error amplification. Original numerical teaching fixtures, not images, latent tensors or model outputs. No training, reverse sampling, image/video generation, quality benchmark or provider execution.

## 1 · What the symbols mean

x0 is the known original signal; epsilon is the supplied noise; a = alpha_bar is cumulative alpha, not a single-step beta, time or image quality. The paper's marginal distribution uses standard Gaussian noise. Our fixed illustrative epsilon is not a random Gaussian draw and does not test that distribution. Comparing different a with fixed epsilon is NOT a forward Markov trajectory.

xt = sqrt(a) * x0 + sqrt(1-a) * epsilon

x0_hat = (xt - sqrt(1-a) * epsilon_hat) / sqrt(a)

The supplied epsilon_hat is NOT a trained predictor. If epsilon_hat equals the known epsilon, inversion is an algebraic oracle. We already know what was added; this is not generation from pure noise.

## 2 · Follow the full worked trace

W: x0=[1,-1], epsilon=[0.5,-0.5], a=0.64, epsilon_hat=[0.3,-0.3]. sqrt(a)=0.8 and sqrt(1-a)=0.6. Signal term=[0.8,-0.8]; noise term=[0.3,-0.3]; xt=[1.1,-1.1]. Oracle reconstruction=[1,-1]. Wrong estimate reconstruction=[1.15,-1.15]; error=[0.15,-0.15]; MSE=(0.15²+(-0.15)²)/2=0.0225.

x0_hat-x0 = sqrt((1-a)/a) * (epsilon-epsilon_hat). Therefore reconstruction MSE = ((1-a)/a) * noise-estimate MSE. The noise-estimate MSE is 0.04. At a=0.04, reconstruction MSE=0.96: 42.6667 times the W result, under the same fixed estimation error. Real model errors need not stay fixed across noise levels. This MSE uses the known teaching x0; it is not a universal image-quality score.

## 3 · Run the complete source offline

Download and extract diffusion-noise-lab.zip, open a terminal in its diffusion-noise directory. Python 3.9+ standard library only; no installation, account, API key, GPU, internet or model weights. Run exactly:

    python3 -B demo.py

    python3 -B -m unittest -v

The default demo prints every intermediate value for W and high noise as JSON, without revealing T. Expected MSE values are 0.0225 and 0.96, within floating-point tolerance. Nine unit tests cover the identities, oracle and validation. Edit a copy of fixtures.json to try a different estimate; tests intentionally retain the reference fixtures. Never round intermediate values; display rounding does not feed back into calculation.

## 4 · Independent transfer before the reference

T: x0=[-0.5,1], epsilon=[1,-0.25], a=0.36, epsilon_hat=[0.7,-0.1]. Without opening the reference or running the T preset, predict xt, reconstruction, coordinate errors and MSE. What happens to reconstruction error if a decreases while estimation error stays fixed? Explain why an oracle is not a generation model. Record your calculation and one limitation in WORKSHEET-en.md, then compare with REFERENCE-en.md. Only after attempting T, run demo.py with the --include-transfer flag to reveal its computed reference. Opening the reference does not establish mastery.

## 5 · Recovery and next step

Allowed inputs: a in [0.01,1] and exactly two finite components in [-10,10] for each input vector. Booleans, empty input, strings in the Python API, NaN and infinity are rejected, never silently clipped. Derived outputs may exceed input bounds. a=0 cannot be inverted; 0.01 is only a teaching/numerical guardrail, not a physical diffusion limit. Browser edits hide previous results until Calculate; presets set inputs without revealing answers. Reset restores W and clears output; no learning records are written. Language navigation preserves only valid region and shared section, not unfinished input or computed output. If JavaScript is disabled, use the trace and Python packet. Invalid JSON: restore the downloaded fixture. Wrong directory: enter the extracted diffusion-noise directory. Missing Python: install a supported interpreter through your normal trusted workflow.

Success means explaining the mechanism and limits, not reporting a generated image. Continue with video sampling to distinguish arithmetic from temporal evidence; use tiny training to learn what parameter optimization actually means. This unit does not train an epsilon predictor or implement classifier-free guidance.
