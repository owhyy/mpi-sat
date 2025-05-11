from tests import (
    plot_bf_vs_resolution,
    plot_dpll_heuristics,
)
import seaborn as sns

if __name__ == "__main__":
    sns.set_theme()

    plot_dpll_heuristics(30)
    plot_bf_vs_resolution(10)
