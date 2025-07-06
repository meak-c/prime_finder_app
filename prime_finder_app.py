from math import sqrt

import streamlit as st

st.set_page_config(
    page_title="最も近い素数を表示するアプリ",
    page_icon="🔍",
    layout="centered",
)


# 素数判定
@st.cache_data
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


# 上方向の素数
def find_upper_primes(n, count):
    primes = []
    candidate = n
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes


# 下方向の素数
def find_lower_primes(n, count):
    primes = []
    candidate = n
    while len(primes) < count and candidate >= 2:
        if is_prime(candidate):
            primes.append(candidate)
        candidate -= 1
    return primes[::-1]


# 最も近い素数を比較
def compare_candidates(n, upper_list, lower_list):
    up = upper_list[0]
    down = lower_list[-1]
    if up == down:
        return [up]
    dist_up = abs(n - up)
    dist_down = abs(n - down)
    if dist_up == dist_down:
        return [down, up]
    return [down] if dist_down < dist_up else [up]


# Streamlit UI
st.title("🔮 最も近い素数を探すアプリ")

MAX = 1_000_000
n = st.number_input("整数を入力してください（2~1,000,000）", min_value=2, step=1)
count = st.selectbox("上下に表示する素数の個数", [1, 3, 5, 10], index=2)

if n > MAX:
    st.error("⚠️ 入力値が大きすぎます。1000000 以下の整数を入力してください。")
    st.stop()  # 残りの処理を止めて、ボタン非表示にする

if st.button("計算する"):
    upper = find_upper_primes(n, count)
    lower = find_lower_primes(n, count)
    nearest = compare_candidates(n, upper, lower)

    st.markdown(f"### 入力された整数： `{n}`")
    st.markdown(f"**下側の素数 {count}個**: {lower}")
    st.markdown(f"**上側の素数 {count}個**: {upper}")

    if len(nearest) == 1:
        st.success(f"🧮 最も近い素数は {nearest[0]} です。")
    else:
        st.success(f"🧮 最も近い素数は {nearest[0]} と {nearest[1]} です。")
