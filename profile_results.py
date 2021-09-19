import pstats
from pstats import SortKey

p = pstats.Stats("profile.out")
# p.sort_stats("cumulative").print_stats(10)
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()
