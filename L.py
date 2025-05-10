import numpy as np
import matplotlib.pyplot as plt

# Step 1: 构造 ψ(t)
def generate_psi(t, N=10):
    a_n = 1.0 / np.sqrt(np.arange(1, N + 1))
    phi_n = np.linspace(0, 2 * np.pi, N)
    psi = np.zeros_like(t)
    for i in range(N):
        psi += a_n[i] * np.cos((i + 1) * t + phi_n[i])
    return psi

# Step 2: 真实 Frobenius 迹 + 模拟 λ(p)
true_trace = np.array([0, -2, -1, 2, -1, -1, 2, -3, 2, 0, -2, 1])
p_list = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
true_trace_sq = true_trace**2

t = np.linspace(0, 2 * np.pi, 500)
psi = generate_psi(t)
lambda_p = 2 * psi[p_list % len(t)]
lambda_sq = lambda_p**2

# Step 3: 可视化比较
plt.figure(figsize=(8, 5))
plt.plot(p_list, true_trace_sq, 'o-', label='True Tr(ρ(Fr_p))²')
plt.plot(p_list, lambda_sq, 's--', label='Simulated λ(p)²')
plt.xlabel("Prime p")
plt.ylabel("Squared Value")
plt.title("Validation: λ(p)² vs True Frobenius Trace Squared")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Step 4: 输出误差结果
diff = lambda_sq - true_trace_sq
abs_diff = np.abs(diff)
success_rate = np.mean(abs_diff < 5)

print("\nSpectral Frobenius Trace Approximation Test")
print("-" * 50)
print(f"Max Error:   {np.max(abs_diff):.4f}")
print(f"Mean Error:  {np.mean(abs_diff):.4f}")
print(f"Success (<5): {100 * success_rate:.1f}% ({int(success_rate * len(p_list))}/{len(p_list)})")
