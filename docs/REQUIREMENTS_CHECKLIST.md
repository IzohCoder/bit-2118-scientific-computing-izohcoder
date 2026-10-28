# Requirements checklist

Source of truth: `BIT_2118_Scientific_Computing Group Work.pdf`. The PDF says every group must complete all listed tasks, and each individual must keep an individual GitHub repository. For every task it asks for inputs and mathematical operations, a changed input/parameter and explanation, output interpretation (including graphs where relevant), and a different related real-world case documented with assumptions, data, results, and interpretation.

| PDF requirement | Completed in this project | Status / remaining action |
|---|---|---|
| Tasks 2–20: NumPy arrays and numerical computation | `code/Task_02_numpy_arrays.py`, `code/runner.py` task02 | Complete; baseline and warmer-day comparison, lab energy adaptation |
| Task 3: mathematical functions and vectorization | Task 03 | Complete; loop/vectorized timing and doubled array size |
| Task 4: floating point and numerical errors | Task 04 | Complete; closeness, absolute/relative error, cancellation and meter accumulation |
| Task 5: matrix algebra and operations | Task 05 | Complete; rotation/scaling and floor-plan coordinate correction |
| Task 6: solve linear systems | Task 06 | Complete; solve and residual check, shared water meter model |
| Task 7: Gaussian elimination and LU | Task 07 | Complete; factor reused for multiple right-hand sides, residual checks |
| Task 8: iterative linear methods | Task 08 | Complete; Jacobi/Gauss-Seidel, tolerance change, direct solution and convergence graph |
| Task 9: eigenvalues/eigenvectors | Task 09 | Complete; dominant eigenpair and residual; changed network edge |
| Task 10: bisection/fixed point | Task 10 | Complete; root/residual, start-guess change, equilibrium graph |
| Task 11: Newton/secant | Task 11 | Complete; method comparison, cash-flow change, separate solar investment case |
| Task 12: polynomial/nonlinear systems | Task 12 | Complete; both intersections, residuals, changed inspection-zone radius |
| Task 13: interpolation | Task 13 | Complete; linear/spline comparison, missing smart-meter estimate, graph |
| Task 14: curve fitting/approximation | Task 14 | Complete; residual RMSE, changed observation, filter-flow adaptation, graph |
| Task 15: numerical differentiation | Task 15 | Complete; GPS estimates, downsampling change, tank leak-rate adaptation, graph |
| Task 16: numerical integration | Task 16 | Complete; trapezoid/Simpson comparison and irregular smart-meter data |
| Task 17: Euler ODE | Task 17 | Complete; exact comparison, step-size change, grain moisture adaptation, graph |
| Task 18: SciPy ODE solver | Task 18 | Complete; exact comparison, voltage change, battery-equivalent adaptation, graph |
| Task 19: numerical optimization | Task 19 | Complete; capacity change, continuous/integer solutions, vaccine-cooler adaptation |
| Task 20: random numbers/Monte Carlo | Task 20 | Complete; seeded estimate and standard error, uncertainty change, solar-pump shortfall adaptation, convergence graph |
| Report actual outputs and interpretations | `docs/TECHNICAL_REPORT.md`, `results/runs/` | Complete for the recorded run; benchmark time is machine-dependent |
| Compare assignment with optional reference repository | `docs/TECHNICAL_REPORT.md` | README/topic and file-layout comparison completed. Individual reference source pages could not be retrieved, so a line-by-line code comparison remains unverified. PDF remains authoritative. |
| Reproducible setup and run instructions | `README.md`, `requirements.txt` | Complete |
| Individual repository; do not use group repository | Local Git repository and commit `1d18bc9`; planned GitHub name `bit-2118-scientific-computing-izohcoder` | Local commit complete. Public publication is awaiting explicit user approval after automatic review blocked external disclosure; CLI authentication also needs refresh. |
| Student identifiers and personal details | `FINAL_SUBMISSION_GUIDE.md` | Placeholder retained; enter only if required by lecturer/VLMS |
| VLMS upload and final submission | `FINAL_SUBMISSION_GUIDE.md` | Must be completed by the student; no VLMS access was supplied |

## Verification record

- All 19 task launchers completed successfully in the recorded run.
- Numerical residuals and/or exact/analytical comparisons are printed where appropriate; captured output is in `results/runs/`.
- Figures are generated into `results/figures/`; their visual review is part of this handover.
- The GitHub CLI initially completed browser authentication, but the project execution environment later reported its stored token invalid and could not reach the GitHub API. Automatic review blocked the public create-and-push request as external disclosure. No remote publication is claimed.
