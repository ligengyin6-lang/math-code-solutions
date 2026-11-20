import sympy as sp
import mpmath as mp

# ============================================================
# 第一部分：符号推导
# 原题：
# f(x) = ∫[0, x] e^(cos t) dt
# g(x) = ∫[0, sin x] e^(t^2) dt
# ============================================================

# 声明实变量，u 是换元后使用的积分变量
x, t, u = sp.symbols("x t u", real=True)

# 用 SymPy 表示两个变上限积分
# 不调用 integrate()，因为这两个积分都没有简单的初等原函数
f = sp.Integral(sp.exp(sp.cos(t)), (t, 0, x))
g = sp.Integral(sp.exp(t**2), (t, 0, sp.sin(x)))

# ------------------------------------------------------------
# 计算 f(-x)：令 t = -u
#
# f(-x) = ∫[0, -x] e^(cos t) dt
#       = -∫[0, x] e^(cos(-u)) du
#       = -∫[0, x] e^(cos u) du
#       = -f(x)
#
# 这里使用了余弦函数是偶函数：cos(-u) = cos(u)
# ------------------------------------------------------------
f_minus_x = -sp.Integral(sp.exp(sp.cos(u)), (u, 0, x))

# ------------------------------------------------------------
# 计算 g(-x)：先利用 sin(-x) = -sin(x)，再令 t = -u
#
# g(-x) = ∫[0, -sin x] e^(t^2) dt
#       = -∫[0, sin x] e^((-u)^2) du
#       = -∫[0, sin x] e^(u^2) du
#       = -g(x)
# ------------------------------------------------------------
g_minus_x = -sp.Integral(sp.exp(u**2), (u, 0, sp.sin(x)))

# 将原积分中的积分变量也改名为 u，以便比较两个表达式
# 定积分中的积分变量是“哑变量”，改名不会改变积分值
f_with_u = f.xreplace({t: u})
g_with_u = g.xreplace({t: u})

# 如果 f(-x) = -f(x)，那么 f(-x) + f(x) 应当等于 0
f_parity_check = sp.simplify(f_minus_x + f_with_u)
g_parity_check = sp.simplify(g_minus_x + g_with_u)

print("符号推导结果：")
print("f(-x) + f(x) =", f_parity_check)
print("g(-x) + g(x) =", g_parity_check)

# 两个结果均为 0，说明 f 和 g 都是奇函数
assert f_parity_check == 0
assert g_parity_check == 0

# 另外，f'(x) = e^(cos x) > 0，所以 f 在 R 上严格递增
# 因此 f 不是周期函数，可以排除“两个函数均为周期函数”的选项
f_derivative = sp.diff(f, x)
print("f'(x) =", f_derivative)


# ============================================================
# 第二部分：数值积分复核
# 注意：数值计算只用于检查结果，严格结论由上面的换元推导给出
# ============================================================

# 提高数值计算精度
mp.mp.dps = 30


def f_numeric(x_value):
    """数值计算 f(x) = ∫[0, x] e^(cos t) dt。"""
    return mp.quad(
        lambda t_value: mp.exp(mp.cos(t_value)),
        [0, x_value]
    )


def g_numeric(x_value):
    """数值计算 g(x) = ∫[0, sin x] e^(t^2) dt。"""
    return mp.quad(
        lambda t_value: mp.exp(t_value**2),
        [0, mp.sin(x_value)]
    )


print("\n数值验证（结果应非常接近 0）：")

# 选取多个正数，分别检查 f(-x) + f(x) 和 g(-x) + g(x)
for x_value in [mp.mpf("0.3"), mp.mpf("1.0"), mp.mpf("1.8")]:
    f_error = f_numeric(-x_value) + f_numeric(x_value)
    g_error = g_numeric(-x_value) + g_numeric(x_value)

    print(
        f"x = {x_value}: "
        f"f(-x)+f(x) = {mp.nstr(f_error, 6)}, "
        f"g(-x)+g(x) = {mp.nstr(g_error, 6)}"
    )

print("\n结论：f(x) 和 g(x) 均为奇函数，选择 C。")
