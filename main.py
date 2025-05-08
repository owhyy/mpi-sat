from tests import plot_dp_optimizations, plot_general_method_comparison
import seaborn as sns

from dpll import dpll
from utils import generate_random_formula
from brute_force import brute_force

if __name__ == "__main__":
    sns.set_theme()
    plot_general_method_comparison()
    # plot_dp_optimizations()
    # resolution_optimization_tests()
    # dp_optimization_tests()
