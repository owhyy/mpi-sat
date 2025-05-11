from tests import (
    dp_plots,
    dpll_plots,
    resolution_plots,
)

import seaborn as sns

if __name__ == "__main__":
    sns.set_theme()

    resolution_plots()
    dp_plots()
    dpll_plots()    
