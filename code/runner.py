"""Reproducible BIT 2118 examples and individual real-world adaptations."""
from __future__ import annotations

import argparse
from pathlib import Path
import timeit

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson, solve_ivp
from scipy.interpolate import CubicSpline, interp1d
from scipy.linalg import lu_factor, lu_solve
from scipy.optimize import curve_fit, minimize, root, root_scalar

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "results" / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=160)
    plt.close(fig)


def task02():
    print("PDF example: hourly weather-station temperature array")
    c = np.array([18.5,18.0,17.8,17.5,17.9,19.0,21.5,23.8,25.6,27.1,28.3,29.0,29.4,29.1,28.5,27.6,26.2,24.8,23.4,22.1,21.0,20.2,19.6,19.0])
    for label, a in [("Original 24 readings", c), ("Warmer day (+2 C)", c + 2)]:
        print(f"{label}: mean={a.mean():.2f} C, min={a.min():.2f} C, max={a.max():.2f} C")
    # Related case: daily electricity demand by hour; vectorized unit conversion.
    kwh = np.array([0.42,0.38,0.35,0.34,0.37,0.55,0.82,1.10,1.25,1.18,1.06,0.98,1.02,1.15,1.24,1.30,1.42,1.63,1.77,1.55,1.20,0.86,0.65,0.50])
    print(f"Adaptation - 24 hourly lab energy readings: total={kwh.sum():.2f} kWh, peak={kwh.max():.2f} kWh at hour {kwh.argmax():02d}; voltage-equivalent index first 4={np.round(kwh[:4]*1000,1)} Wh")


def task03():
    rng = np.random.default_rng(42)
    x = rng.uniform(5, 250, 1_000_000)
    def loop(): return [float(v / 1000) ** 2 for v in x]
    def vector(): return (x / 1000) ** 2
    # Repeat both paths for a fair, reproducible comparison.
    loop_t = timeit.timeit(loop, number=1)
    vec_t = timeit.timeit(vector, number=3) / 3
    print(f"PDF example, 1,000,000 latency values: first={vector()[:5]}, loop={loop_t:.4f}s, vectorized={vec_t:.4f}s, speed-up={loop_t/vec_t:.1f}x")
    larger = rng.uniform(5, 250, 2_000_000)
    print(f"Changed input: 2,000,000 latency values; mean squared seconds={np.mean((larger/1000)**2):.6f}; output count={len((larger/1000)**2)} (vectorized computation rerun at doubled size).")
    # Related case: sensor signal power for a vibration monitor.
    signal = rng.normal(0, 0.04, 200_000) + 0.2 * np.sin(np.linspace(0, 40*np.pi, 200_000))
    power = signal ** 2
    print(f"Adaptation - vibration sensor: mean-square signal={power.mean():.6f}, peak squared amplitude={power.max():.4f}")


def task04():
    direct, stable = [], []
    for x in [1e-4, 1e-8, 1e-12]:
        direct.append((np.sqrt(1+x)-1)/x); stable.append(1/(np.sqrt(1+x)+1))
    print(f"PDF example: 0.1+0.2={0.1+0.2!r}; exact equality with 0.3={0.1+0.2==0.3}; isclose={np.isclose(0.1+0.2,0.3)}")
    print(f"sqrt(2) approximation absolute error={abs(np.sqrt(2)-1.414):.8f}; relative error={abs(np.sqrt(2)-1.414)/np.sqrt(2):.8%}")
    print("Cancellation test x=[1e-4,1e-8,1e-12]: direct=", np.array(direct), "stable=", np.array(stable))
    # Adaptation: accumulate tiny energy increments beside a large stored total.
    n = 1_000_000
    naive = 1e8
    for _ in range(n): naive += 1e-5
    expected = 1e8 + n * 1e-5
    compensated = 1e8 + np.sum(np.full(n, 1e-5, dtype=np.float64))
    print(f"Adaptation - cumulative metering: large baseline + {n} tiny increments, expected={expected:.6f}, sequential float64={naive:.6f}, abs error={abs(naive-expected):.6f}; NumPy array sum={compensated:.6f}, abs error={abs(compensated-expected):.6f}.")


def task05():
    pts = np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
    def transform(angle_deg, sx, sy):
        a=np.deg2rad(angle_deg); r=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        s=np.diag([sx,sy]); m=r@s
        return m, pts@m.T
    for label, pars in [("PDF example",(45,2,1.5)),("Changed scale",(45,3,1.5))]:
        m,p=transform(*pars); print(f"{label}: transformation=\n{m}\npoints=\n{p}\ndeterminant={np.linalg.det(m):.4f}")
    # Adaptation: rotate and anisotropically scale a small floor-plan footprint.
    m,p=transform(12,1.04,0.97)
    print(f"Adaptation - floor-plan survey correction (12-degree orientation, x/y scale 1.04/0.97): transformed corner 3={p[2]}, area scale={np.linalg.det(m):.4f}")


def task06():
    A=np.array([[4.,2.],[8.,12.]])
    for label,b in [("PDF example",np.array([20.,72.])),("Changed demand",np.array([24.,80.]))]:
        x=np.linalg.solve(A,b); print(f"{label}: type-A={x[0]:.4f}, type-B={x[1]:.4f}, residual norm={np.linalg.norm(A@x-b):.2e}")
    # Adaptation: infer two overlapping water uses from aggregate meter channels.
    W=np.array([[1.,1.],[2.,0.5]]) # total flow and pressure-weighted response
    y=np.array([18.,24.])
    q=np.linalg.solve(W,y)
    print(f"Adaptation - two shared-branch water flows: branch estimates={q} L/min; reconstructed meter totals={W@q}; interpretation: two independent meter equations separate otherwise overlapping demand.")


def task07():
    A=np.array([[4.,-1.,0.],[-1.,4.,-1.],[0.,-1.,3.]])
    sets=[np.array([15.,10.,10.]),np.array([16.,11.,9.]),np.array([14.,12.,11.])]
    lu,piv=lu_factor(A)
    for i,b in enumerate(sets,1):
        x=lu_solve((lu,piv),b); print(f"PDF example set {i}: x={np.round(x,6)}, residual={np.linalg.norm(A@x-b):.2e}")
    # Adaptation: reuse the same pipe-network model for several hourly demands.
    demands=[np.array([21.,8.,13.]),np.array([18.,12.,16.])]
    for i,b in enumerate(demands,1):
        x=lu_solve((lu,piv),b); print(f"Adaptation - shared water-network demand period {i}: branch corrections={np.round(x,4)}; residual={np.linalg.norm(A@x-b):.2e}")


def task08():
    A=np.diag([2.]*5)+np.diag([-1.]*4,1)+np.diag([-1.]*4,-1)
    b=np.array([100.,0.,0.,0.,20.])
    def jacobi(tol):
        D=np.diag(A); R=A-np.diagflat(D); x=np.zeros_like(b); errs=[]
        for _ in range(500):
            xn=(b-R@x)/D; e=np.linalg.norm(xn-x,np.inf); errs.append(e); x=xn
            if e<tol: break
        return x,errs
    def gs(tol):
        x=np.zeros_like(b); errs=[]
        for _ in range(500):
            old=x.copy()
            for i in range(5): x[i]=(b[i]-A[i,:i]@x[:i]-A[i,i+1:]@old[i+1:])/A[i,i]
            e=np.linalg.norm(x-old,np.inf); errs.append(e)
            if e<tol: break
        return x,errs
    xj,ej=jacobi(1e-8); xg,eg=gs(1e-8); exact=np.linalg.solve(A,b)
    xlo,elo=jacobi(1e-3)
    print(f"PDF example five-node wall temperatures: Jacobi={xj}, Gauss-Seidel={xg}, direct={exact}; iterations J/GS={len(ej)}/{len(eg)}")
    print(f"Changed tolerance 1e-3: Jacobi iterations={len(elo)}, solution error infinity norm={np.linalg.norm(xlo-exact,np.inf):.3e}")
    fig,ax=plt.subplots(); ax.semilogy(ej,label="Jacobi"); ax.semilogy(eg,label="Gauss-Seidel"); ax.set(xlabel="Iteration",ylabel="Maximum update (C)",title="Task 8 convergence"); ax.legend(); ax.grid(True); save(fig,"task08_convergence.png")
    print("Adaptation - wall grid used as a simplified multi-zone thermal model: the solution decreases from 100 C to 20 C across interior locations; boundary temperatures are fixed and radiation is ignored.")


def task09():
    A=np.array([[0.,1.,1.,0.],[1.,0.,1.,1.],[1.,1.,0.,1.],[0.,1.,1.,0.]])
    vals,vecs=np.linalg.eig(A); k=np.argmax(vals.real); v=vecs[:,k].real; score=np.abs(v); score/=score.sum()
    names=["A","B","C","D"]
    print(f"PDF example dominant eigenvalue={vals[k].real:.6f}; centralities={dict(zip(names,np.round(score,4)))}; eigen residual={np.linalg.norm(A@v-vals[k].real*v):.2e}")
    # Change: remove an edge and recompute influence.
    B=A.copy(); B[1,2]=B[2,1]=0
    w,q=np.linalg.eig(B); j=np.argmax(w.real); z=np.abs(q[:,j].real); z/=z.sum()
    print(f"Changed network (edge B-C removed): centralities={dict(zip(names,np.round(z,4)))}")
    # Adaptation: room-to-room transfer network; centrality measures access through neighboring rooms.
    print("Adaptation - campus transfer network: the same eigenvector score ranks rooms by connections to already well-connected rooms; it is a structural proxy, not measured passenger volume.")


def task10():
    f=lambda T:T-25-10*np.exp(-T/20)
    bis=root_scalar(f,bracket=[20,40],method="bisect",xtol=1e-10)
    g=lambda T:25+10*np.exp(-T/20)
    def fixed(start):
        x=float(start); h=[x]
        for _ in range(100):
            xn=g(x); h.append(xn)
            if abs(xn-x)<1e-10: break
            x=xn
        return h
    hist=fixed(30); altered=fixed(10)
    print(f"PDF heat-balance root: bisection={bis.root:.8f} C, residual={f(bis.root):.2e}; fixed point={hist[-1]:.8f} C in {len(hist)-1} iterations")
    print(f"Changed initial guess 10 C: fixed point={altered[-1]:.8f} C in {len(altered)-1} iterations")
    # Adaptation: temperature setpoint at which a room's heat input balances loss.
    fig,ax=plt.subplots(); t=np.linspace(20,40,300); ax.plot(t,f(t)); ax.axhline(0,color="black",lw=.8); ax.axvline(bis.root,ls="--"); ax.set(xlabel="Room temperature (C)",ylabel="Net heat balance",title="Task 10 equilibrium root"); ax.grid(True); save(fig,"task10_heat_balance.png")
    print("Adaptation - room heating equilibrium: root is the modeled balance point; the illustrative exponential heat-gain law is assumed and is not a building-energy calibration.")


def task11():
    cash=[-10000,3000,3500,4000,2500]
    f=lambda r:sum(cf/(1+r)**t for t,cf in enumerate(cash))
    df=lambda r:sum(-t*cf/(1+r)**(t+1) for t,cf in enumerate(cash) if t>0)
    n=root_scalar(f,fprime=df,x0=.10,method="newton",xtol=1e-12)
    s=root_scalar(f,x0=.05,x1=.20,method="secant",xtol=1e-12)
    changed=[cash[0]]+[cf*1.1 for cf in cash[1:]]
    f2=lambda r:sum(cf/(1+r)**t for t,cf in enumerate(changed))
    df2=lambda r:sum(-t*cf/(1+r)**(t+1) for t,cf in enumerate(changed) if t>0)
    n2=root_scalar(f2,x0=.10,fprime=df2,method="newton",xtol=1e-12)
    print(f"PDF investment cash-flow IRR: Newton={n.root:.8%}, secant={s.root:.8%}; NPV residual={f(n.root):.3e}")
    print(f"Changed inflows (+10%): IRR={n2.root:.8%}; interpretation: stronger later inflows raise the break-even rate for the same initial outlay.")
    solar_flows=[-18000,5200,5600,5900,6200,6500]
    solar_npv=lambda r:sum(cf/(1+r)**t for t,cf in enumerate(solar_flows))
    solar=root_scalar(solar_npv,bracket=[0.0,.5],method="brentq")
    print(f"Adaptation - solar pump investment cash flows: break-even discount rate={solar.root:.3%}, NPV residual={solar_npv(solar.root):.2e}; excludes taxes, inflation, maintenance, and uncertainty.")


def task12():
    def eq(z): x,y=z; return [x*x+y*y-4,y-(x*x-1)]
    roots=[]
    for guess in ([1.,1.],[-1.,1.]):
        sol=root(eq,guess); roots.append(sol.x); print(f"PDF circle/parabola guess={guess}: solution={np.round(sol.x,8)}, residual={np.linalg.norm(eq(sol.x)):.2e}, success={sol.success}")
    radius=3.0
    def route_eq(z):
        x,y=z; return [x*x+y*y-radius**2,y-(x*x-1)]
    sol=root(route_eq,[2.,2.]); print(f"Adaptation - radius-{radius:.0f} inspection zone vs curved route: crossing={np.round(sol.x,8)}, residual={np.linalg.norm(route_eq(sol.x)):.2e}, converged={sol.success}; planar geometry is assumed.")


def task13():
    x=np.array([8,9,10,11,12,13,14.],float); y=np.array([18,20,22.5,24,25,25.5,25.])
    lin=interp1d(x,y); cub=CubicSpline(x,y); target=10.5
    print(f"PDF temperature at 10:30: linear={float(lin(target)):.3f} C, cubic={float(cub(target)):.3f} C")
    # Adaptation: reconstruct missing 10:30 demand between hourly smart meter records.
    demand=np.array([.42,.38,.35,.34,.37,.55,.82,1.10,1.25,1.18,1.06,.98,1.02,1.15,1.24,1.30,1.42,1.63,1.77,1.55,1.20,.86,.65,.50])
    hours=np.arange(24,dtype=float); missing=interp1d(hours,demand,kind="linear")(10.5)
    print(f"Adaptation - half-hour lab energy demand reconstructed from hourly samples: {float(missing):.3f} kW; interpolation is inside sampled range and smooth short-term variation is assumed.")
    grid=np.arange(8,14+1/6,1/6); fig,ax=plt.subplots(); ax.scatter(x,y,label="observations"); ax.plot(grid,lin(grid),label="linear"); ax.plot(grid,cub(grid),label="cubic spline"); ax.set(xlabel="Hour",ylabel="Temperature (C)",title="Task 13 interpolation"); ax.legend(); ax.grid(True); save(fig,"task13_interpolation.png")


def task14():
    x=np.array([50,100,150,200,250,300,350.],float); y=np.array([82,95,115,145,185,238,305.])
    model=lambda u,a,b,c:a*u*u+b*u+c
    p,_=curve_fit(model,x,y); pred=model(x,*p); rmse=np.sqrt(np.mean((y-pred)**2))
    print(f"PDF server-response fit: coefficients={np.round(p,8)}, RMSE={rmse:.3f} ms, predicted at 400 users={model(400,*p):.2f} ms")
    y2=y.copy(); y2[-1]+=35
    p2,_=curve_fit(model,x,y2); print(f"Changed final measurement (+35 ms): predicted at 400={model(400,*p2):.2f} ms; RMSE={np.sqrt(np.mean((y2-model(x,*p2))**2)):.2f} ms")
    # Adaptation: fit a quadratic to repeated filter flow measurements by service cycle.
    cycles=np.array([0,10,20,30,40,50,60.]); flow=np.array([8.4,8.1,7.8,7.1,6.8,6.0,5.7])
    q,_=curve_fit(model,cycles,flow); print(f"Adaptation - reusable water filter flow versus service cycles: fitted flow at cycle 70={model(70,*q):.2f} L/min; extrapolation may be unreliable beyond observed range.")
    grid=np.linspace(50,400,300); fig,ax=plt.subplots(); ax.scatter(x,y,label="observed"); ax.plot(grid,model(grid,*p),label="quadratic fit"); ax.set(xlabel="Concurrent users",ylabel="Response time (ms)",title="Task 14 curve fit"); ax.legend(); ax.grid(True); save(fig,"task14_curve_fit.png")


def task15():
    t=np.arange(7,dtype=float); pos=np.array([0.,4.8,10.2,16.1,22.7,30.,38.])
    v=np.gradient(pos,t,edge_order=1)
    exact=np.array([4.8,5.1,5.65,6.25,6.95,7.65,8.0]) # central/one-sided estimates from the recorded positions
    print(f"PDF GPS position: estimated speeds={np.round(v,3)} m/s")
    td=t[::2]; pd=pos[::2]; vd=np.gradient(pd,td)
    print(f"Changed sampling interval to 2 s (actual downsample): estimates={np.round(vd,3)} m/s; endpoint average={(pd[-1]-pd[0])/(td[-1]-td[0]):.3f} m/s")
    # Adaptation: estimate flow deterioration from tank-volume time measurements.
    sec=np.array([0,10,20,30,40,50,60.]); volume=np.array([500,491,480,468,455,441,426.])
    rate=np.gradient(volume,sec); print(f"Adaptation - tank level derivative: final estimated leak rate={-rate[-1]:.3f} L/s; central differences are noisier when measurements are irregular or noisy.")
    fig,ax=plt.subplots(); ax.plot(t,v,marker="o"); ax.set(xlabel="Time (s)",ylabel="Estimated speed (m/s)",title="Task 15 numerical derivative"); ax.grid(True); save(fig,"task15_derivative.png")


def task16():
    t=np.arange(0,14,2,dtype=float); p=np.array([.8,1.,1.4,1.8,1.6,1.2,.9])
    trap=np.trapezoid(p,x=t); simp=simpson(p,x=t)
    print(f"PDF smart meter: trapezoidal={trap:.3f} kWh, Simpson={simp:.3f} kWh, difference={abs(simp-trap):.3f} kWh")
    p2=p*1.25; print(f"Changed appliance demand (+25%): trapezoidal={np.trapezoid(p2,x=t):.3f} kWh, Simpson={simpson(p2,x=t):.3f} kWh")
    # Adaptation: integrate lab energy with irregularly spaced readings.
    ts=np.array([0.,1.5,3.5,6.,8.5,11.]); kw=np.array([.42,.36,.41,.88,1.10,.61])
    print(f"Adaptation - lab smart meter, irregular sampling: energy={np.trapezoid(kw,x=ts):.3f} kWh; trapezoids assume linear changes between readings.")


def task17():
    ambient, initial, k, end=25.,90.,.12,30.
    def euler(h):
        n=int(round(end/h)); t=np.linspace(0,end,n+1); T=np.empty(n+1); T[0]=initial
        for i in range(n): T[i+1]=T[i]+h*(-k*(T[i]-ambient))
        exact=ambient+(initial-ambient)*np.exp(-k*t)
        return t,T,exact
    t,T,ex=euler(1.); _,Tsmall,_=euler(.5)
    print(f"PDF cooling after 30 min: Euler h=1 {T[-1]:.4f} C; exact={ex[-1]:.4f} C; error={abs(T[-1]-ex[-1]):.4f} C")
    print(f"Changed step h=0.5 min: Euler={Tsmall[-1]:.4f} C; absolute error={abs(Tsmall[-1]-ex[-1]):.4f} C")
    # Adaptation: moisture loss during grain-store ventilation; first-order model.
    h=.25; ts=np.arange(0,8+h/2,h); m=np.empty_like(ts); m[0]=18.; rate=.08
    for i in range(len(ts)-1): m[i+1]=m[i]+h*(-rate*(m[i]-10.))
    print(f"Adaptation - grain moisture content: after 8 h={m[-1]:.2f}% from 18%; equilibrium=10%; constant-rate coefficient and uniform ventilation assumed.")
    fig,ax=plt.subplots(); ax.plot(t,T,"o-",label="Euler h=1"); ax.plot(t,ex,"--",label="exact"); ax.set(xlabel="Minutes",ylabel="Temperature (C)",title="Task 17 Euler cooling"); ax.legend(); ax.grid(True); save(fig,"task17_euler.png")


def task18():
    vs,r,c,v0=5.,1000.,.001,0.
    def solve(vs):
        f=lambda t,v:[(vs-v[0])/(r*c)]
        return solve_ivp(f,(0,5),[v0],t_eval=np.linspace(0,5,200),rtol=1e-9,atol=1e-11)
    s=solve(vs); exact=vs*(1-np.exp(-s.t/(r*c))); s2=solve(6.)
    print(f"PDF RC charging: V(5s)={s.y[0,-1]:.6f} V, max exact-solution error={np.max(abs(s.y[0]-exact)):.3e} V, success={s.success}")
    print(f"Changed supply 6 V: V(5s)={s2.y[0,-1]:.6f} V")
    # Adaptation: slower energy-store voltage curve with larger time constant.
    r2,c2=1500.,.002; f=lambda t,v:[(4.2-v[0])/(r2*c2)]
    q=solve_ivp(f,(0,10),[2.8],t_eval=np.linspace(0,10,201),rtol=1e-9,atol=1e-11)
    print(f"Adaptation - battery pack voltage recovery: after 10 s={q.y[0,-1]:.3f} V toward 4.2 V; ideal first-order RC-like equivalent, not a chemistry battery model.")
    fig,ax=plt.subplots(); ax.plot(s.t,s.y[0],label="solve_ivp"); ax.plot(s.t,exact,"--",label="exact"); ax.set(xlabel="Seconds",ylabel="Voltage (V)",title="Task 18 adaptive ODE solver"); ax.legend(); ax.grid(True); save(fig,"task18_scipy_ode.png")


def task19():
    cost=lambda z:12*z[0]+18*z[1]
    cap=lambda z:100*z[0]+170*z[1]-1000
    sol=minimize(cost,[5,3],method="SLSQP",bounds=[(0,None),(0,None)],constraints={"type":"ineq","fun":cap})
    intbest=min((12*a+18*b,a,b,100*a+170*b) for a in range(20) for b in range(20) if 100*a+170*b>=1000)
    cap2=lambda z:100*z[0]+170*z[1]-1200
    sol2=minimize(cost,[5,4],method="SLSQP",bounds=[(0,None),(0,None)],constraints={"type":"ineq","fun":cap2})
    print(f"PDF capacity planning: continuous A/B={sol.x}, capacity={100*sol.x[0]+170*sol.x[1]:.2f}, cost={sol.fun:.2f}; integer best cost/A/B/capacity={intbest}")
    print(f"Changed requirement 1200: continuous allocation={np.round(sol2.x,3)}, cost={sol2.fun:.2f}")
    cooler_cost=lambda z:38*z[0]+61*z[1]
    cooler_capacity=lambda z:18*z[0]+32*z[1]-150
    cold=minimize(cooler_cost,[3,3],method="SLSQP",bounds=[(0,None),(0,None)],constraints={"type":"ineq","fun":cooler_capacity})
    cold_integer=min((38*a+61*b,a,b,18*a+32*b) for a in range(20) for b in range(20) if 18*a+32*b>=150)
    print(f"Adaptation - vaccine cooler capacity planning: continuous small/large={np.round(cold.x,3)}, cost={cold.fun:.2f}, capacity={18*cold.x[0]+32*cold.x[1]:.1f} L; integer option cost/small/large/capacity={cold_integer}; counts are simplified and ignore route constraints.")


def task20():
    rng=np.random.default_rng(42); n=100_000; demand=rng.normal(850.,120.,n); overload=demand>1000.
    p=overload.mean(); se=np.sqrt(p*(1-p)/n)
    rng2=np.random.default_rng(42); demand2=rng2.normal(850.,150.,n); p2=np.mean(demand2>1000.)
    print(f"PDF Monte Carlo: overload={p:.4%} ({overload.sum()}/{n}), estimated standard error={se:.4%}")
    print(f"Changed uncertainty std 150: overload={p2:.4%}; greater demand variability raises modeled overload risk.")
    # Adaptation: Monte Carlo availability risk for solar pump output vs uncertain daily demand.
    rng=np.random.default_rng(2118); solar=np.clip(rng.normal(72,14,n),0,None); water=np.clip(rng.normal(65,10,n),0,None)
    fail=solar<water; run=np.cumsum(fail)/np.arange(1,n+1)
    print(f"Adaptation - solar pump shortfall probability={fail.mean():.4%}; simulated daily supply and use are independent normal approximations, so this is a planning estimate rather than a field reliability result.")
    idx=np.unique(np.logspace(1,np.log10(n),200).astype(int))-1; fig,ax=plt.subplots(); ax.semilogx(idx+1,run[idx]); ax.axhline(fail.mean(),ls="--",label=f"final {fail.mean():.3f}"); ax.set(xlabel="Simulations",ylabel="Estimated shortfall probability",title="Task 20 Monte Carlo convergence"); ax.legend(); ax.grid(True); save(fig,"task20_monte_carlo.png")


TASKS={2:task02,3:task03,4:task04,5:task05,6:task06,7:task07,8:task08,9:task09,10:task10,11:task11,12:task12,13:task13,14:task14,15:task15,16:task16,17:task17,18:task18,19:task19,20:task20}

def main(task_override=None):
    if task_override is None:
        parser=argparse.ArgumentParser(description="Run one BIT 2118 scientific computing task")
        parser.add_argument("task",type=int,choices=TASKS)
        task=parser.parse_args().task
    else:
        task=task_override
    print(f"\n=== BIT 2118 Task {task} ===")
    TASKS[task]()

if __name__=="__main__": main()
