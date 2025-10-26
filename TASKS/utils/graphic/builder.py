import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Builder:

    def __init__(self, csv_name: str = None, df: pd.DataFrame = None) -> None:
        if df is not None:
            self.dataset = df
        elif csv_name is not None:
            self.dataset = pd.read_csv('resources/csv/' + csv_name)
        else:
            raise ValueError("Необходимо передать либо csv_name, либо df")

    def build_histograms(self, columns: list) -> None:
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set(style="whitegrid", palette="muted")
        num_columns = len(columns)
        rows = (num_columns // 3) + (num_columns % 3 > 0)
        fig, axes = plt.subplots(rows, 3, figsize=(12, rows * 3))
        axes = axes.flatten()
        for i, column in enumerate(columns):
            sns.histplot(
                self.dataset[column],
                bins=30,
                kde=True,
                color="skyblue",
                edgecolor="black",
                ax=axes[i],
            )
            axes[i].set_title(f"Распределение {column}", fontsize=16, weight='bold')
            axes[i].set_xlabel(f"{column}", fontsize=14)
            axes[i].set_ylabel('Частота', fontsize=14)
            axes[i].tick_params(axis='both', which='major', labelsize=12)
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
        plt.tight_layout()
        plt.show()

    def plot_percentile_line(self, column: str, our_value: float) -> None:
        data = self.dataset[column].values
        percentiles = np.percentile(data, np.arange(0, 101))
        nth_percentile = next(p for p in range(101) if percentiles[p] > our_value)
        plt.figure(figsize=(8, 5))
        sns.histplot(data, bins=30, kde=True, color="skyblue", edgecolor="black")
        plt.axvline(
            our_value,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f"CrunchieMunchies ({our_value} калорий)",
        )
        plt.title(f"Распределение {column} с отмеченным процентилем", fontsize=16, weight='bold')
        plt.xlabel(column, fontsize=14)
        plt.ylabel("Частота", fontsize=14)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
