import sys
from argparse import ArgumentParser, ArgumentTypeError


def parse_numbers(value):
    """
    小数や不正な値を検出する
    """
    try:
        num = float(value)
        if not num.is_integer():
            raise ValueError
        num = int(num)
        if num < 2:
            raise ValueError
        return num
    except ValueError:
        raise ArgumentTypeError(f"'{value}' は無効です。2以上の整数を入力してください。")


def get_integer():
    """
    コマンドライン引数を取得し、バリデーションをクリアするまで再入力を促す
    """
    if len(sys.argv) == 1:
        print("⚠️ 入力が検出されませんでした。スペース区切りで整数を1つ以上入力してください。")
        print("例: python script.py 13 28")
        print("使い方を見るには `--help` をつけてください。")
        sys.exit(1)

    if "-h" in sys.argv or "--help" in sys.argv:
        parser = ArgumentParser(description="与えられた整数に近い素数を見つけるプログラム")
        parser.add_argument(
            "numbers",
            type=parse_numbers,
            nargs="+",
            help="2以上の整数をスペースで区切って入力してください。"
        )
        parser.print_help()
        sys.exit(0)  # ヘルプを表示して正常終了

    while True:
        try:
            parser = ArgumentParser(description="与えられた整数に近い素数を見つけるプログラム")
            parser.add_argument(
                "numbers",
                type=parse_numbers,
                nargs="+",
                help="2以上の整数をスペースで区切って入力してください。"
            )
            # コマンドライン引数を解析
            args = parser.parse_args()

            # 入力が正常であればリストを返す
            return args.numbers
        except SystemExit:
            # argparseのエラーをキャッチし、再入力を促す
            print("入力が無効です。入力方式がわからない場合はhelpを参照し、再入力してください。")
            continue


def is_prime(n: int):
    """
    素数判定を行う
    """
    # このスクリプトでは必要ないが、再利用性を加味してn=1のときもチェックしている
    if n == 1:
        return False
    # n=2は唯一の偶数素数のため、早期にチェック
    if n == 2:
        return True
    # 2以外の偶数は全て合成数のため、排除
    if n % 2 == 0:
        return False

    # この段階では偶数で割り切れることはないため、iは2ずつ加算していく
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def find_upper_primes(n: int, count: int = 5):
    """
    n以上で最も近い素数から上方向にcount個の素数を返す。デフォルト値はcount=5
    """
    prime_list = []
    candidate = n
    # 素数がcount個集まるまでチェック
    while len(prime_list) < count:
        if is_prime(candidate):
            prime_list.append(candidate)
        candidate += 1
    return prime_list


def find_lower_primes(n: int, count: int = 5):
    """
    以上で最も近い素数から下方向にcount個の素数を返す。デフォルト値はcount=5
    """
    prime_list = []
    candidate = n
    # 素数がcount個集まるまでチェック
    while len(prime_list) < count and candidate >= 2:
        if is_prime(candidate):
            prime_list.append(candidate)
        candidate -= 1
    return prime_list[::-1]


def compare_candidates(n: int, upper_list, lower_list):
    """
    入力された整数に最も近い素数をリストとして返す
    """
    upper_candidate = upper_list[0]
    lower_candidate = lower_list[-1]
    # 両者が同じなら、入力された整数は素数だったということ。それを長さ1のリストとして返す。
    if upper_candidate == lower_candidate:
        return [upper_candidate]

    upper_dist = abs(n - upper_candidate)
    lower_dist = abs(n - lower_candidate)

    # 両方の距離が同じなら、2つのcandidateをともにリストに入れて返す
    if upper_dist == lower_dist:
        return [lower_candidate, upper_candidate]
    # あとは、近い方の素数を判定して返す
    elif upper_dist > lower_dist:
        return [lower_candidate]
    else:
        return [upper_candidate]


def display_result(n: int, lower_list, upper_list, prime_list):
    """
    nの近傍の素数と、最も近い素数を表示する
    """
    print(f"{n} に近い素数のリストの下側は '{lower_list}'")
    print(f"{n} に近い素数のリストの上側は '{upper_list}'")

    if len(prime_list) == 1:
        print(f"{n} に最も近い素数は {prime_list[0]} です。")
        return
    else:
        print(f"{n} に最も近い素数は {prime_list[0]} と {prime_list[1]} です。")
        return


def main():
    """
    受け取ったコマンドライン引数それぞれに対して、一連の処理を行う
    """
    nums = get_integer()
    for num in nums:
        upper_primes = find_upper_primes(num, 5)
        lower_primes = find_lower_primes(num, 5)
        prime_list = compare_candidates(num, upper_primes, lower_primes)
        display_result(num, lower_primes, upper_primes, prime_list)


if __name__ == "__main__":
    main()
