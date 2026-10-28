# Final submission guide

## What the assignment asks

The supplied BIT 2118 assignment asks for Tasks 2–20. For each task, identify its inputs and numerical operation, change at least one input or parameter and explain the effect, interpret the output and any graph, and adapt the program to a different related real-world problem. The GitHub work must be an individual repository. The repository link and documentation are to be submitted through MKU VLMS.

## What is prepared

- A runnable Python program for every task, in `code/Task_*.py`.
- The PDF-style example, an input/parameter variation, and a distinct practical adaptation in each program; shared logic is in `code/runner.py`.
- Actual output captures in `results/runs/` and generated plots in `results/figures/`.
- Setup/run instructions in `README.md`, dependencies in `requirements.txt`, and requirement tracking in `docs/REQUIREMENTS_CHECKLIST.md`.
- Methods, calculations, interpretations, assumptions, limitations, and reference comparison in `docs/TECHNICAL_REPORT.md`.

## How to run

From the project folder in PowerShell:

```powershell
python -m pip install -r requirements.txt
python code\Task_10_bisection_fixed_point.py
```

Replace the example filename to run a different task. Programs save any relevant plot automatically in `results/figures/`.

## Main findings to understand

- Direct solutions and LU solves reproduce their right-hand sides with residuals near floating-point precision; iterative methods trade additional updates for an approximate solution.
- Root-finding methods locate the heat-balance equilibrium at about 27.5252 °C. Newton and secant both find the investment example's IRR of about 11.5425%.
- Linear and cubic interpolation give slightly different estimates between measurements; a smooth curve is an assumption, not new observed data.
- Smaller Euler steps reduce the cooling error in this example. `solve_ivp` agrees closely with the exact RC curve.
- Continuous optimization may return fractional equipment counts; the integer comparison is the physically purchaseable option.
- Monte Carlo outputs are estimates with sampling uncertainty. They depend on the specified distributions and are not measured failure rates.

Before discussing the work, be ready to explain the method used in each task, the changed input, how a residual/error was checked, and which assumptions would need real measurements before applying the adapted model in practice.

## Student details to fill if required

- Student name: `[enter your name]`
- Registration number: `[enter your registration number]`
- Unit / lecturer details: `[enter only if requested]`

## GitHub and VLMS

- Verified individual public repository: <https://github.com/IzohCoder/bit-2118-scientific-computing-izohcoder>.
- The `main` branch is published, and the pushed commit was verified against the local branch.
- MKU VLMS was not available from this workspace. The student must sign in to VLMS and upload/submit the repository URL and required documentation using the assignment's submission area.

## Final checklist

- [x] Confirm the GitHub repository is published and opens under your account.
- [ ] Review the README and the report for any changes your lecturer requested.
- [ ] Replace personal-detail placeholders only where required.
- [ ] Open the assignment submission on MKU VLMS.
- [ ] Upload the requested documentation/files and provide the verified individual repository link.
- [ ] Confirm VLMS shows the submission as received before the deadline.
