# 三角関数のグラフ探究
# trigonometric_function_explorer.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

    if abs(a - 1) < 1e-10:
        a_part = ""

    elif abs(a + 1) < 1e-10:
        a_part = "-"

    else:
        a_part = f"{a:.1f}"

    # p

    if abs(p) < 1e-10:
        inside = "x"

    elif p > 0:
        inside = f"(x-{p:.2f})"

    else:
        inside = f"(x+{abs(p):.2f})"

    # b

    if abs(b - 1) < 1e-10:
        inside_part = inside

    else:
        inside_part = f"{b:.1f}{inside}"

    return f"y={a_part}{func_name}{inside_part}"


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

# ======================================
# パラメータ
# ======================================

col1, col2 = st.columns(2)

with col1:

    a = st.slider(
        "振幅 a",
        -5.0,
        5.0,
        1.0,
        0.1
    )

with col2:

    b = st.slider(
        "周期係数 b",
        0.5,
        5.0,
        1.0,
        0.1
    )

p = st.slider(
    "位相移動 p",
    -np.pi,
    np.pi,
    0.0,
    0.1
)

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

# 特別角

if show_special:

    special = [
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
    "sin", r"\sin"
)

latex_formula = latex_formula.replace(
    "cos", r"\cos"
)

latex_formula = latex_formula.replace(
    "tan", r"\tan"
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
        f"周期 = 2π/{b:.1f} = {period:.2f}"
    )

else:

    st.write(
        f"周期 = π/{b:.1f} = {period:.2f}"
    )

st.write(
    f"位相移動 = {p:.2f}"
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
