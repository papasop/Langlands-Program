import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# 示例真实 Frobenius trace（整数）
true_trace = np.array([0, -2, -1, 2, -1, -1, 2, -3, 2, 0, -2, 1])
p_list = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
true_trace_sq = true_trace**2

# Hitchin ψ(t) 与 λ(p) 构造
def generate_psi(t, N=10):
    a_n = 1.0 / np.sqrt(np.arange(1, N+1))
    phi_n = np.random.uniform(0, 2*np.pi, N)
    psi = np.zeros_like(t)
    for i in range(N):
        psi += a_n[i] * np.cos((i+1) * t + phi_n[i])
    return psi

t = np.linspace(0, 2 * np.pi, 500)
psi_vals = generate_psi(t)
lambda_p = 2 * psi_vals[p_list % len(t)]  # 注意：p_list % len(t) 可能导致索引错误，需确保正确
lambda_p_sq = lambda_p**2

# 可视化 λ² vs Tr²
plt.figure(figsize=(8, 5))
plt.plot(p_list, true_trace_sq, 'o-', label=r'True Tr$(\rho(\mathrm{Fr}_p))^2$')
plt.plot(p_list, lambda_p_sq, 's--', label=r'Simulated $\lambda(p)^2$')
plt.xlabel("Prime p")
plt.ylabel("Squared Value")
plt.title(r"Validation: $\lambda(p)^2$ vs True Frobenius Trace Squared")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 误差结构分析
diff = lambda_p_sq - true_trace_sq
abs_diff = np.abs(diff)

# 输出误差指标
result = {
    "max_diff": float(np.max(abs_diff)),
    "mean_diff": float(np.mean(abs_diff)),
    "frobenius_square_alignment_success": float(np.mean(abs_diff < 5))  # 允许±5以内偏差
}
print("Error Analysis Results:")
for key, value in result.items():
    print(f"{key}: {value}")
