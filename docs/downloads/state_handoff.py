#!/usr/bin/env python3
"""A scalar handoff thought experiment, NOT a robot simulator or benchmark.

Python 3.10+; standard library only. No network, model, hardware or file writes.
All methods get at most two operations per episode. Failed policy calls do not
change state. Bridge uses one operation. Oracle sees privileged true state.
Run: python3 state_handoff.py --episodes 200 --seed 7 --noise 0.10
"""
import argparse
import csv
import math
import random
import sys


def positive_int(value):
    number = int(value)
    if not 1 <= number <= 1_000_000:
        raise argparse.ArgumentTypeError('episodes must be between 1 and 1000000')
    return number


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError('must be a finite nonnegative number')
    return number


def experiment(episodes=200, seed=7, noise=0.10, bridge_error=0.05):
    rng = random.Random(seed)
    threshold = 0.25
    totals = {name: {'successes': 0, 'calls': 0, 'inside_n': 0,
                      'inside_successes': 0, 'outside_n': 0, 'outside_successes': 0}
              for name in ('direct_retry', 'observed_bridge', 'oracle_bridge')}
    for _ in range(episodes):
        # Draw once per episode, independently of which method is evaluated.
        x = rng.uniform(-1, 1)
        observation_error = rng.gauss(0, noise)
        actuation_error = rng.gauss(0, bridge_error)
        y = x + observation_error
        inside = abs(x) <= threshold
        outcomes = {
            'direct_retry': (inside, 1 if inside else 2),
            'observed_bridge': (abs(x - y + actuation_error) <= threshold, 2),
            'oracle_bridge': (abs(actuation_error) <= threshold, 2),
        }
        for method, (success, calls) in outcomes.items():
            stats = totals[method]
            group = 'inside' if inside else 'outside'
            stats['successes'] += int(success)
            stats['calls'] += calls
            stats[group + '_n'] += 1
            stats[group + '_successes'] += int(success)
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=positive_int, default=200)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--noise', type=nonnegative, default=0.10,
                        help='Gaussian observation noise standard deviation')
    parser.add_argument('--bridge-error', type=nonnegative, default=0.05,
                        help='Gaussian bridge execution error standard deviation')
    args = parser.parse_args()
    print('# Teaching scalar model; no physics, vision or learned policy.', file=sys.stderr)
    print('# Maximum operations = 2 per episode; oracle uses privileged state.', file=sys.stderr)
    fields = ['method', 'episodes', 'seed', 'noise', 'bridge_error', 'successes',
              'success_rate', 'mean_operations', 'inside_n', 'inside_successes',
              'outside_n', 'outside_successes']
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for method, stats in experiment(args.episodes, args.seed, args.noise, args.bridge_error).items():
        writer.writerow(dict(method=method, episodes=args.episodes, seed=args.seed,
            noise=args.noise, bridge_error=args.bridge_error, successes=stats['successes'],
            success_rate=round(stats['successes']/args.episodes, 4),
            mean_operations=round(stats['calls']/args.episodes, 4),
            **{k: stats[k] for k in ('inside_n','inside_successes','outside_n','outside_successes')}))


if __name__ == '__main__':
    main()
