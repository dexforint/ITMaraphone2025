import sys
import itertools


def read_input():
    try:
        lines = [line.strip() for line in sys.stdin if line.strip()]

        # Кол-во заклятий
        n = int(lines[0])
        if not (1 <= n <= 100):
            raise ValueError

        # n строк с заклятиями
        if len(lines) < 1 + n + 1:
            raise ValueError
        spells = []
        for i in range(1, 1 + n):
            parts = lines[i].split()
            if len(parts) != 2:
                raise ValueError
            length, power = map(int, parts)
            if length <= 0 or power <= 0:
                raise ValueError
            spells.append((length, power))

        # Кол-во свитков
        k = int(lines[1 + n])
        if not (1 <= k <= 3):
            raise ValueError

        # Лимиты свитков
        limit_line = lines[2 + n]
        limits = list(map(int, limit_line.strip().split()))
        if len(limits) != k:
            raise ValueError
        if any(l <= 0 for l in limits):
            raise ValueError

        return spells, k, limits

    except Exception:
        print(-1)
        sys.exit(0)


def solve(spells, k, limits):
    n = len(spells)

    # Мы будем использовать динамическое программирование с мемоизацией
    from functools import lru_cache

    # Преобразуем список заклятий в отдельные списки длины и силы
    lengths = [spell[0] for spell in spells]
    powers = [spell[1] for spell in spells]

    @lru_cache(maxsize=None)
    def dp(i, *capacities):
        if i == n:
            return 0  # Больше заклятий нет

        max_power = dp(i + 1, *capacities)  # Пропустить текущее заклятие

        # Попробовать положить текущее заклятие в один из свитков
        for w in range(k):
            if lengths[i] <= capacities[w]:
                new_capacities = list(capacities)
                new_capacities[w] -= lengths[i]
                max_power = max(max_power, powers[i] + dp(i + 1, *new_capacities))

        return max_power

    return dp(0, *limits)


def main():
    spells, k, limits = read_input()
    result = solve(spells, k, limits)
    print(result)


if __name__ == "__main__":
    main()


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def solve(n, spells, m, limits):
    memo = {}

    def dp(idx, remainings):
        if idx == n:
            return 0

        state = (idx, remainings)
        if state in memo:
            return memo[state]

        max_power = dp(idx + 1, remainings)

        length, power = spells[idx]
        for i in range(m):
            if remainings[i] >= length:
                remainings_list = list(remainings)
                remainings_list[i] -= length
                new_remainings = tuple(remainings_list)
                max_power = max(max_power, dp(idx + 1, new_remainings) + power)

        memo[state] = max_power
        return max_power

    return dp(0, tuple(limits))


def main():
    try:
        n = int(input().strip())
        if not 1 <= n <= 100:
            print(-1)
            return

        spells = []
        for _ in range(n):
            length, power = map(int, input().strip().split())
            if length <= 0 or power <= 0:
                print(-1)
                return
            spells.append((length, power))

        m = int(input().strip())
        if not 1 <= m <= 3:
            print(-1)
            return

        limits = list(map(int, input().strip().split()))
        if len(limits) != m or any(limit <= 0 for limit in limits):
            print(-1)
            return

        result = solve(n, spells, m, limits)
        print(result)
    except:
        print(-1)


if __name__ == "__main__":
    main()
