# 三角関数のグラフ探究
# trigonometric_function_explorer2A.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

# ================================
# pi_label関数
# ================================

def pi_label(x):

    if abs(x) < 1e-10:
        return "0"

    frac = Fraction(
        x / np.pi
    ).limit_denominator(12)

    n = frac.numerator
    d = frac.denominator

    if d == 1:

        if n == 1:
            return "π"

        if n == -1:
            return "-π"

        return f"{n}π"

    else:

        if n == 1:
            return f"π/{d}"

        if n == -1:
            return f"-π/{d}"

        return f"{n}π/{d}"


# =====================================================
# フォント設定
# =====================================================
from matplotlib import font_manager
font_manager.fontManager.addfont("ipaexg.ttf")
plt.rcParams["font.family"] = "IPAexGothic"

# ======================================
# 画面設定
# ======================================

st.set_page_config(
    page_title="三角関数グラフ探究",
    layout="wide"
)

# ======================================
# 教科書表記
# ======================================


def make_formula(func_name, a, b, p):

    # a

    if a == 1:
        a_part = ""

    elif a == -1:
        a_part = "-"

    else:
        a_part = str(int(a))

    # p

    if abs(p) < 1e-10:

        inside = "x"

    elif p > 0:

        inside = f"(x-{pi_label(p)})"

    else:

        inside = f"(x+{pi_label(abs(p))})"

    # b

    if abs(b - 1) < 1e-10:

        b_part = ""

    elif abs(b - 0.5) < 1e-10:

        b_part = "1/2"

    else:

        b_part = str(int(b))

    return f"y={a_part}{func_name}{b_part}{inside}"
        
# ======================================
# タイトル
# ======================================

st.title("三角関数グラフ探究アプリ")

st.markdown(r"""
## 学習する関数

\[
y=a\sin b(x-p)
\]

\[
y=a\cos b(x-p)
\]

\[
y=a\tan b(x-p)
\]

### 注目するポイント

- 振幅
- 周期
- 位相移動
- 基準グラフとの違い
""")

# ======================================
# 関数選択
# ======================================

func_type = st.radio(
    "グラフを選択",
    ["sin", "cos", "tan"],
    horizontal=True
)

# ======================================
# 表示方法
# ======================================

mode = st.radio(
    "x軸表示",
    ["弧度法", "度数法"],
    horizontal=True
)

st.markdown("### パラメータ設定")

# 振幅

a_dict = {
    "-3": -3,
    "-2": -2,
    "-1": -1,
    "1": 1,
    "2": 2,
    "3": 3
}

a_label = st.radio(
    "振幅 a",
    list(a_dict.keys()),
    horizontal=True,
    index=3
)

a = a_dict[a_label]

# 周期係数

b_dict = {
    "1/2": 0.5,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4
}

b_label = st.radio(
    "周期係数 b",
    list(b_dict.keys()),
    horizontal=True,
    index=1
)

b = b_dict[b_label]

# 位相移動

phase_dict = {
    "-π": -np.pi,
    "-3π/4": -3*np.pi/4,
    "-π/2": -np.pi/2,
    "-π/3": -np.pi/3,
    "-π/4": -np.pi/4,
    "-π/6": -np.pi/6,
    "0": 0,
    "π/6": np.pi/6,
    "π/4": np.pi/4,
    "π/3": np.pi/3,
    "π/2": np.pi/2,
    "3π/4": 3*np.pi/4,
    "π": np.pi
}

phase_label = st.radio(
    "位相移動 p（右へ正）",
    list(phase_dict.keys()),
    horizontal=True,
    index=6
)

p = phase_dict[phase_label]




# ======================================
# 表示範囲
# ======================================

st.markdown("### グラフ表示範囲")

col3, col4 = st.columns(2)

with col3:

    x_range = st.slider(
        "x方向表示範囲（π倍）",
        1,
        5,
        2
    )

with col4:

    y_range = st.slider(
        "y方向表示範囲",
        2,
        20,
        5
    )

# ======================================
# オプション
# ======================================

show_base = st.checkbox(
    "基準グラフを表示",
    value=True
)

show_special = st.checkbox(
    "特別角を表示",
    value=True
)

# ======================================
# データ
# ======================================

xmin = -x_range * np.pi
xmax = x_range * np.pi

x = np.linspace(
    xmin,
    xmax,
    5000
)

# ======================================
# 現在グラフ
# ======================================

if func_type == "sin":

    y = a * np.sin(
        b * (x - p)
    )

    base = np.sin(x)

elif func_type == "cos":

    y = a * np.cos(
        b * (x - p)
    )

    base = np.cos(x)

else:

    y = a * np.tan(
        b * (x - p)
    )

    base = np.tan(x)

    y[np.abs(y) > y_range] = np.nan
    base[np.abs(base) > y_range] = np.nan

# ======================================
# 式
# ======================================

formula = make_formula(
    func_type,
    a,
    b,
    p
)

# ======================================
# グラフ
# ======================================

fig, ax = plt.subplots(
    figsize=(10, 6)
)

# 基準グラフ

if show_base:

    ax.plot(
        x,
        base,
        "--",
        color="gray",
        linewidth=2,
        alpha=0.6,
        label="基準グラフ"
    )

# 現在グラフ

ax.plot(
    x,
    y,
    color="blue",
    linewidth=3,
    label=formula
)

# x軸・y軸

ax.axhline(
    0,
    color="black"
)

ax.axvline(
    0,
    color="black"
)


# 振幅表示

if func_type in ["sin", "cos"]:

    ax.axhline(
        abs(a),
        color="red",
        alpha=0.3
    )

    ax.axhline(
        -abs(a),
        color="red",
        alpha=0.3
    )

# ===========================
# tan の漸近線
# ===========================

if func_type == "tan":

    for k in range(-10, 11):

        xa = (np.pi/2 + k*np.pi)/b + p

        if xmin < xa < xmax:

            ax.axvline(
                xa,
                color="red",
                linestyle="--",
                alpha=0.4
            )    


# 特別角

if show_special:
    
    special = [
        -np.pi/2,
        -np.pi/3,
        -np.pi/4,
        -np.pi/6,
        0,
        np.pi/6,
        np.pi/4,
        np.pi/3,
        np.pi/2
    ]

    for s in special:

        ax.axvline(
            s,
            color="green",
            linestyle=":",
            alpha=0.3
        )

# 周期表示

if func_type in ["sin", "cos"]:

    period = 2*np.pi / b

else:

    period = np.pi / b

ax.annotate(
    "",
    xy=(period, 0),
    xytext=(0, 0),
    arrowprops=dict(
        arrowstyle="<->",
        color="purple",
        lw=2
    )
)

ax.text(
    period/2,
    0.5,
    f"T={period:.2f}",
    color="purple"
)

# 位相表示

ax.annotate(
    "",
    xy=(p, -1),
    xytext=(0, -1),
    arrowprops=dict(
        arrowstyle="<->",
        color="orange",
        lw=2
    )
)

ax.text(
    p/2 if abs(p) > 1e-8 else 0.1,
    -1.4,
    "位相移動",
    color="orange"
)

# ======================================
# x軸目盛
# ======================================

if mode == "弧度法":

    ticks = np.array([
        -2*np.pi,
        -3*np.pi/2,
        -np.pi,
        -np.pi/2,
        0,
        np.pi/2,
        np.pi,
        3*np.pi/2,
        2*np.pi
    ])

    labels = [
        r"$-2\pi$",
        r"$-\frac{3\pi}{2}$",
        r"$-\pi$",
        r"$-\frac{\pi}{2}$",
        "0",
        r"$\frac{\pi}{2}$",
        r"$\pi$",
        r"$\frac{3\pi}{2}$",
        r"$2\pi$"
    ]

    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)

else:

    ticks_deg = np.array([
        -360,
        -270,
        -180,
        -90,
        0,
        90,
        180,
        270,
        360
    ])

    ax.set_xticks(
        np.deg2rad(ticks_deg)
    )

    ax.set_xticklabels(
        [f"{d}°" for d in ticks_deg]
    )

# ======================================
# 表示範囲
# ======================================

ax.set_xlim(
    xmin,
    xmax
)

ax.set_ylim(
    -y_range,
    y_range
)

ax.set_title(
    formula,
    fontsize=18
)

ax.grid(True)

ax.legend()

st.pyplot(fig)

# ======================================
# 式表示
# ======================================

st.markdown("## 現在の式")

latex_formula = formula

latex_formula = latex_formula.replace(
    "sin",
    r"\sin "
)

latex_formula = latex_formula.replace(
    "cos",
    r"\cos "
)

latex_formula = latex_formula.replace(
    "tan",
    r"\tan "
)

st.latex(latex_formula)
# ======================================
# 関数の性質
# ======================================

st.markdown("## 現在の設定")

st.write(
    f"振幅 = {abs(a):.2f}"
)

if func_type in ["sin", "cos"]:

    st.write(
        f"周期 = {pi_label(period)}"
    )

else:

    st.write(
        f"周期 = {pi_label(period)}"
    )

if p > 0:

    st.write(
        f"位相移動 = 右へ {pi_label(p)}"
    )

elif p < 0:

    st.write(
        f"位相移動 = 左へ {pi_label(abs(p))}"
    )

else:

    st.write(
        "位相移動 = なし"
    )


# ======================================
# 探究課題
# ======================================

st.markdown(r"""
## 考察してみよう

### 問1
振幅を大きくするとグラフはどう変化するだろうか。

### 問2
周期係数 b を大きくすると周期はどう変化するだろうか。

### 問3
位相移動 p を変えるとグラフは左右どちらへ動くだろうか。

### 問4
基準グラフと比較して違いを説明しよう。

### 問5
sin, cos, tan の周期の違いを説明しよう。
""")
