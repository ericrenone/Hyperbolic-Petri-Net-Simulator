# Hyperbolic-Petri-Net-Simulator
Visual exploration of Petri net executions in the Poincaré disk.

This work introduces a dual-invariant computational validity criterion requiring joint satisfaction of discrete causal reachability and continuous geometric admissibility in curved spaces.

"If we pretend that a language model's chain-of-thought is secretly firing transitions in a hidden Petri net, can we continuously check two invariants (one symbolic/local + one geometric/global in hyperbolic space) to catch traces that are becoming nonsense / drifting / hallucinating — before they go completely off the rails?"

## Features

- Greedy forward simulation (fires first enabled transition)
- Efficient: hyperbolic distance & admissibility checked only periodically
- Deterministic 128-bit structural fingerprint (safe for negative weights)
- Natural termination detection
