from tests import plot_dp_optimizations, plot_dpll_optimizations, plot_general_method_comparison, plot_resolution_optimizations
import seaborn as sns

from dpll import dpll
from utils import generate_random_formula
from brute_force import brute_force

if __name__ == "__main__":
    sns.set_theme()

    # plot_general_method_comparison()
    # plot_dpll_optimizations()
    plot_resolution_optimizations()
    # dp_optimization_tests()
