

import csv
import os
from datetime import datetime, date
import matplotlib.pyplot as plt


class AquaGuard:

    def __init__(self):
        self.filename = "aquaguard_data.csv"
        self.daily_limit = 500  # Litres
        self.categories = [
            "Drinking",
            "Bathing",
            "Cooking",
            "Washing",
            "Cleaning",
            "Gardening",
            "Other"
        ]

        self.initialize_file()

    # Initialize CSV file
    def initialize_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Date",
                    "Time",
                    "Category",
                    "Water Usage (Litres)"
                ])

    # Record water consumption
    def record_usage(self):
        print("\n--- Record Water Usage ---")

        for index, category in enumerate(self.categories, 1):
            print(f"{index}. {category}")

        try:
            choice = int(input("Select category: "))

            if choice < 1 or choice > len(self.categories):
                print("Invalid category!")
                return

            category = self.categories[choice - 1]

            usage = float(input("Enter water usage in litres: "))

            if usage <= 0:
                print("Usage must be greater than zero.")
                return

            now = datetime.now()

            with open(self.filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    category,
                    usage
                ])

            print("\nWater usage recorded successfully!")

            self.check_daily_limit()

        except ValueError:
            print("Please enter valid numeric values.")

    # Read all records
    def get_records(self):
        records = []

        with open(self.filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

        return records

    # Calculate today's water usage
    def get_today_usage(self):
        today = date.today().strftime("%Y-%m-%d")
        total = 0

        for record in self.get_records():
            if record["Date"] == today:
                total += float(record["Water Usage (Litres)"])

        return total

    # Check daily water limit
    def check_daily_limit(self):
        usage = self.get_today_usage()

        print(f"\nToday's Water Consumption: {usage:.2f} Litres")
        print(f"Daily Water Limit: {self.daily_limit} Litres")

        if usage > self.daily_limit:
            print("\nWARNING: Daily water limit exceeded!")
        elif usage >= self.daily_limit * 0.8:
            print("\nALERT: You are approaching your daily water limit!")
        else:
            print("\nWater consumption is within the safe limit.")

    # Display daily report
    def daily_report(self):
        print("\n--- Daily Water Usage Report ---")

        today = date.today().strftime("%Y-%m-%d")
        category_usage = {}
        total = 0

        for record in self.get_records():
            if record["Date"] == today:
                category = record["Category"]
                usage = float(record["Water Usage (Litres)"])

                category_usage[category] = (
                    category_usage.get(category, 0) + usage
                )

                total += usage

        if total == 0:
            print("No water usage recorded today.")
            return

        for category, usage in category_usage.items():
            print(f"{category}: {usage:.2f} Litres")

        print("------------------------------")
        print(f"Total Usage: {total:.2f} Litres")
        print(f"Remaining Limit: {max(0, self.daily_limit - total):.2f} Litres")

    # Display complete usage history
    def usage_history(self):
        print("\n--- Water Usage History ---")

        records = self.get_records()

        if not records:
            print("No records found.")
            return

        for record in records:
            print(
                f"Date: {record['Date']} | "
                f"Time: {record['Time']} | "
                f"Category: {record['Category']} | "
                f"Usage: {record['Water Usage (Litres)']} Litres"
            )

    # Detect unusual water consumption
    def detect_leak(self):
        print("\n--- Unusual Water Usage Detection ---")

        records = self.get_records()

        today = date.today().strftime("%Y-%m-%d")

        hourly_usage = {}

        for record in records:
            if record["Date"] == today:
                hour = record["Time"][:2]
                usage = float(record["Water Usage (Litres)"])

                hourly_usage[hour] = (
                    hourly_usage.get(hour, 0) + usage
                )

        if not hourly_usage:
            print("No usage data available.")
            return

        average = sum(hourly_usage.values()) / len(hourly_usage)

        detected = False

        for hour, usage in hourly_usage.items():
            if usage > average * 2 and usage > 50:
                print(
                    f"WARNING: Unusual water consumption detected "
                    f"at {hour}:00!"
                )
                detected = True

        if not detected:
            print("No unusual consumption detected.")

        print(
            "\nNote: This is a basic usage anomaly check, "
            "not a confirmed leak detector."
        )

    # Set daily water limit
    def set_limit(self):
        print("\n--- Set Daily Water Limit ---")

        try:
            limit = float(
                input("Enter new daily water limit in litres: ")
            )

            if limit <= 0:
                print("Limit must be greater than zero.")
                return

            self.daily_limit = limit

            print(
                f"Daily water limit updated to "
                f"{self.daily_limit:.2f} Litres."
            )

        except ValueError:
            print("Please enter a valid number.")

    # Calculate water bill
    def calculate_bill(self):
        print("\n--- Water Bill Calculator ---")

        try:
            rate = float(
                input("Enter water cost per 1000 litres: ")
            )

            if rate < 0:
                print("Rate cannot be negative.")
                return

            usage = self.get_today_usage()

            bill = (usage / 1000) * rate

            print(f"\nToday's Usage: {usage:.2f} Litres")
            print(f"Rate: ₹{rate:.2f} per 1000 Litres")
            print(f"Estimated Water Bill: ₹{bill:.2f}")

        except ValueError:
            print("Please enter a valid rate.")

    # Generate water usage graph
    def show_graph(self):
        print("\n--- Water Usage Graph ---")

        records = self.get_records()

        category_usage = {}

        for record in records:
            category = record["Category"]
            usage = float(record["Water Usage (Litres)"])

            category_usage[category] = (
                category_usage.get(category, 0) + usage
            )

        if not category_usage:
            print("No data available to generate graph.")
            return

        categories = list(category_usage.keys())
        usage = list(category_usage.values())

        plt.figure(figsize=(9, 5))

        plt.bar(
            categories,
            usage,
            color="skyblue",
            edgecolor="black"
        )

        plt.title("AquaGuard - Water Consumption Analysis")
        plt.xlabel("Water Usage Category")
        plt.ylabel("Water Consumption (Litres)")
        plt.xticks(rotation=30)
        plt.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        plt.show()

    # Display savings suggestions
    def water_saving_tips(self):
        print("\n--- Smart Water Saving Tips ---")

        tips = [
            "Turn off taps when brushing your teeth.",
            "Repair leaking taps and pipes immediately.",
            "Use buckets instead of long showers.",
            "Reuse water for gardening whenever safe.",
            "Run washing machines with full loads.",
            "Avoid unnecessary water usage.",
            "Install water-efficient taps and showerheads.",
            "Water plants during cooler hours.",
            "Monitor daily water consumption regularly.",
            "Collect rainwater for suitable household uses."
        ]

        for index, tip in enumerate(tips, 1):
            print(f"{index}. {tip}")

    # Main menu
    def main_menu(self):

        while True:

            print("\n")
            print("=" * 45)
            print("       AQUAGUARD")
            print("   SMART WATER USAGE MONITOR")
            print("=" * 45)

            print("1. Record Water Usage")
            print("2. View Daily Usage Report")
            print("3. View Complete Usage History")
            print("4. Check Daily Water Limit")
            print("5. Detect Unusual Water Usage")
            print("6. Set Daily Water Limit")
            print("7. Calculate Water Bill")
            print("8. View Water Usage Graph")
            print("9. Water Saving Tips")
            print("10. Exit")

            print("=" * 45)

            choice = input("Enter your choice (1-10): ")

            if choice == "1":
                self.record_usage()

            elif choice == "2":
                self.daily_report()

            elif choice == "3":
                self.usage_history()

            elif choice == "4":
                self.check_daily_limit()

            elif choice == "5":
                self.detect_leak()

            elif choice == "6":
                self.set_limit()

            elif choice == "7":
                self.calculate_bill()

            elif choice == "8":
                self.show_graph()

            elif choice == "9":
                self.water_saving_tips()

            elif choice == "10":
                print("\nThank you for using AquaGuard!")
                print("Save Water, Save Life!")
                break

            else:
                print("Invalid choice! Please select between 1 and 10.")


# Application entry point
if __name__ == "__main__":

    try:
        app = AquaGuard()
        app.main_menu()

    except KeyboardInterrupt:
        print("\n\nAquaGuard application closed.")

    except Exception as error:
        print(f"\nAn unexpected error occurred: {error}")