#!/usr/bin/env python3
"""Security check script — runs bandit + pip-audit and fails on issues."""

import subprocess
import sys


def run_command(cmd: list[str], label: str) -> bool:
    """Run a command and return True if it passed."""
    print(f"\n{'='*60}")
    print(f"  Running: {label}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, capture_output=False)
    passed = result.returncode == 0

    status = "PASSED ✅" if passed else "ISSUES FOUND ⚠️"
    print(f"\n  {label}: {status}\n")
    return passed


def main() -> int:
    """Run all security checks."""
    results = []

    # Bandit — Python security linter
    results.append(
        run_command(
            ["bandit", "-r", "app/", "-c", ".bandit", "-ll"],
            "Bandit (Security Linter)",
        )
    )

    # pip-audit — check for vulnerable dependencies
    results.append(
        run_command(
            ["pip-audit", "--strict"],
            "pip-audit (Dependency Vulnerabilities)",
        )
    )

    # Summary
    print(f"\n{'='*60}")
    print("  SECURITY CHECK SUMMARY")
    print(f"{'='*60}")

    checks = ["Bandit", "pip-audit"]
    all_passed = True
    for name, passed in zip(checks, results):
        icon = "✅" if passed else "❌"
        print(f"  {icon} {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n  All security checks passed! 🎉\n")
        return 0
    else:
        print("\n  Some security checks failed. Please review above. 🔍\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
