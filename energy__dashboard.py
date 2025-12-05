import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1) DATA LOADER CLASS
# ============================================================
class DataLoader:

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file into a DataFrame."""
        try:
            df = pd.read_csv(file_path)
            print(f"[LOADED] {file_path}")
            return df
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
            return pd.DataFrame()


# ============================================================
# 2) DATA CLEANER CLASS
# ============================================================
class DataCleaner:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataset: convert date & fill missing values."""
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        num_cols = ["Energy_Consumption_kWh", "Water_Usage_Liters", "Maintenance_Cost"]
        for col in num_cols:
            df[col] = df[col].fillna(df[col].mean())

        df = df.sort_values("Date")  # Sort for proper trend plotting
        return df


# ============================================================
# 3) ANALYTICS CLASS
# ============================================================
class Analytics:

    def compute_summary(self, df: pd.DataFrame):
        """Compute statistics."""
        summary = {
            "total_energy": df["Energy_Consumption_kWh"].sum(),
            "avg_energy": df["Energy_Consumption_kWh"].mean(),
            "max_energy": df["Energy_Consumption_kWh"].max(),

            "total_water": df["Water_Usage_Liters"].sum(),
            "avg_water": df["Water_Usage_Liters"].mean(),

            "total_maintenance_cost": df["Maintenance_Cost"].sum(),
            "avg_maintenance_cost": df["Maintenance_Cost"].mean(),
        }
        return summary


# ============================================================
# 4) DASHBOARD VISUALIZER CLASS
# ============================================================
class Dashboard:

    def plot_trends(self, df: pd.DataFrame):
        """Generate building-wise energy, water, and cost trend charts."""

        buildings = df['Building'].unique()

        # Energy plot
        plt.figure(figsize=(10, 5))
        for b in buildings:
            subset = df[df['Building'] == b]
            plt.plot(subset['Date'], subset['Energy_Consumption_kWh'], marker='o', label=f'Building {b}')
        plt.title("Energy Consumption Over Time")
        plt.xlabel("Date")
        plt.ylabel("Energy (kWh)")
        plt.legend()
        plt.tight_layout()
        plt.savefig("energy_trend.png")
        plt.show()

        # Water plot
        plt.figure(figsize=(10, 5))
        for b in buildings:
            subset = df[df['Building'] == b]
            plt.plot(subset['Date'], subset['Water_Usage_Liters'], marker='o', label=f'Building {b}')
        plt.title("Water Usage Over Time")
        plt.xlabel("Date")
        plt.ylabel("Water (Liters)")
        plt.legend()
        plt.tight_layout()
        plt.savefig("water_trend.png")
        plt.show()

        # Maintenance Cost plot
        plt.figure(figsize=(10, 5))
        for b in buildings:
            subset = df[df['Building'] == b]
            plt.plot(subset['Date'], subset['Maintenance_Cost'], marker='o', label=f'Building {b}')
        plt.title("Maintenance Cost Over Time")
        plt.xlabel("Date")
        plt.ylabel("Cost")
        plt.legend()
        plt.tight_layout()
        plt.savefig("maintenance_cost_trend.png")
        plt.show()


# ============================================================
# 5) SUMMARY EXPORTER
# ============================================================
class SummaryExporter:

    def export(self, summary: dict):
        """Save summary to text file."""
        with open("summary_report.txt", "w") as f:
            f.write("ENERGY MANAGEMENT – SUMMARY REPORT\n")
            f.write("====================================\n\n")
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")

        print("\n[SUMMARY SAVED] summary_report.txt")


# ============================================================
# 6) MAIN PROGRAM
# ============================================================
def main():

    print("\n📌 Starting Energy Capstone Project...\n")

    loader = DataLoader()
    cleaner = DataCleaner()
    analyzer = Analytics()
    dashboard = Dashboard()
    exporter = SummaryExporter()

    # Load buildings
    dfA = loader.load_csv("BuildingA.csv")
    dfB = loader.load_csv("BuildingB.csv")
    # dfC = loader.load_csv("BuildingC.csv")  # Optional

    # Check for empty files
    if dfA.empty or dfB.empty:
        print("[ERROR] One or more CSV files could not be loaded. Exiting...")
        return

    # Clean data
    dfA = cleaner.clean(dfA)
    dfB = cleaner.clean(dfB)
    # dfC = cleaner.clean(dfC)

    # Add building labels
    dfA["Building"] = "A"
    dfB["Building"] = "B"
    # dfC["Building"] = "C"

    # Merge datasets
    merged_df = pd.concat([dfA, dfB], ignore_index=True)  # Add dfC if needed

    # Compute summary
    summary = analyzer.compute_summary(merged_df)
    print("\n📊 SUMMARY RESULTS:\n", summary)

    # Visualizations
    dashboard.plot_trends(merged_df)

    # Export summary
    exporter.export(summary)

    print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")


# Run Program
if __name__ == "__main__":
    main()
