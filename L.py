import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Step 1: 真实 Frobenius trace 数据
true_trace = np.array([0, -2, -1, 2, -1, -1, 2, -3, 2, 0, -2, 1])
p_list = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
true_trace_sq = true_trace ** 2

# Step 2: 构造 ψ(t) 的超高维谱模型
N = 90  # 频率数
t = np.linspace(0, 2 * np.pi, 500)

# 优化目标函数：λ(p)^2 拟合 Tr(ρ)^2
def objective(params):
    a_n = params[:N]
    phi_n = params[N:]
    psi = np.zeros_like(t)
    for i in range(N):
        psi += a_n[i] * np.cos((i + 1) * t + phi_n[i])
    lambda_p = 2 * psi[p_list % len(t)]
    lambda_sq = lambda_p**2
    return np.mean((lambda_sq - true_trace_sq) ** 2)

# 初始值与优化边界
a0 = 1.0 / np.sqrt(np.arange(1, N + 1))
phi0 = np.linspace(0, 2 * np.pi, N)
x0 = np.concatenate([a0, phi0])
bounds = [(0.01, 2.0)] * N + [(0, 2 * np.pi)] * N

# Step 3: 执行优化
res = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)
opt_params = res.x
a_opt = opt_params[:N]
phi_opt = opt_params[N:]

# Step 4: 构造 λ(p)^2 并比较
psi_opt = np.zeros_like(t)
for i in range(N):
    psi_opt += a_opt[i] * np.cos((i + 1) * t + phi_opt[i])
lambda_p = 2 * psi_opt[p_list % len(t)]
lambda_sq = lambda_p**2

# Step 5: 可视化
plt.figure(figsize=(8, 5))
plt.plot(p_list, true_trace_sq, 'o-', label='True Tr(ρ(Fr_p))²')
plt.plot(p_list, lambda_sq, 's--', label='Simulated λ(p)²')
plt.title("Extreme Precision: λ(p)² vs Frobenius Trace² (N=90)")
plt.xlabel("Prime p")
plt.ylabel("Squared Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 6: 输出误差结果
diff = lambda_sq - true_trace_sq
abs_diff = np.abs(diff)
success_rate = np.mean(abs_diff < 5)

print("\nFrobenius Simulation Result (Extreme N=90)")
print("------------------------------------------------")
print(f"MSE:           {np.mean(abs_diff**2):.6e}")
print(f"Max Error:     {np.max(abs_diff):.6f}")
print(f"Mean Error:    {np.mean(abs_diff):.6f}")
print(f"Success (<5):  {success_rate * 100:.1f}%")
print(f"a_n[:5]:       {np.round(a_opt[:5], 4).tolist()}")
print(f"phi_n[:5]:     {np.round(phi_opt[:5], 4).tolist()}")
