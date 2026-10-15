
# Weather Data Analyzer - Computer Science Project
# Class 12 - A

import matplotlib.pyplot as plt

# ---------------------- File Readers ----------------------

def read_txt(file_name):
    """Reads temperature data from a TXT file"""
    temps = []

    with open(file_name, "r") as file:
        for line in file:
            value = line.strip()

            if value.isdigit():
                temps.append(int(value))

    return temps


def read_csv(file_name):
    """Reads date and temperature data from a CSV file"""
    dates = []
    temps = []

    with open(file_name, "r") as file:
        for line in file:
            if "," in line:
                date, temp = line.strip().split(",", 1)

                try:
                    temps.append(float(temp))
                    dates.append(date)
                except ValueError:
                    continue

    return dates, temps


# ---------------------- Statistics ----------------------

def stats(temps):
    highest = max(temps)
    lowest = min(temps)
    average = sum(temps) / len(temps)

    return highest, lowest, average


# ---------------------- Weather Prediction ----------------------

def predict_future(temps, days=5):
    """Predicts temperatures using a moving average and damped trend"""

    if len(temps) < 2:
        print("Not enough data to predict. Add at least 2 readings.")
        return []

    if days <= 0:
        print("Please enter a positive number of days.")
        return []


    recent_temps = temps[-5:]


    average_temp = sum(recent_temps) / len(recent_temps)

    changes = []

    for i in range(1, len(recent_temps)):
        changes.append(recent_temps[i] - recent_temps[i - 1])

    trend = sum(changes) / len(changes)

    predictions = []
    last_temp = temps[-1]

    for i in range(days):

        damped_trend = trend * (0.5 ** i)


        next_temp = (
            last_temp
            + 0.35 * (average_temp - last_temp)
            + damped_trend
        )

        predictions.append(round(next_temp, 2))
        last_temp = next_temp

    return predictions


# ---------------------- Display Reports ----------------------

def display_report(temps):
    if not temps:
        print("No valid temperature data found.")
        return

    highest, lowest, average = stats(temps)

    print("\n===== WEATHER DATA REPORT =====")
    print(f"Total Days Recorded : {len(temps)}")
    print(f"Highest Temperature : {highest:g}°C")
    print(f"Lowest Temperature  : {lowest:g}°C")
    print(f"Average Temperature : {average:.2f}°C")


def display_predictions(predictions):
    if not predictions:
        return

    print("\n===== FUTURE TEMPERATURE ESTIMATES =====")

    for i, temp in enumerate(predictions, start=1):
        print(f"Day +{i}: {temp:.2f}°C")

    print("\nNote: These are statistical estimates, not official forecasts.")


# ---------------------- Graphs ----------------------

def show_line_graph(dates, temps):
    if not dates or not temps:
        print("No data available to display.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Over Time")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def show_bar_graph(dates, temps):
    if not dates or not temps:
        print("No data available to display.")
        return

    plt.figure(figsize=(10, 5))
    plt.bar(dates, temps)
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Chart")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_prediction_graph(dates, temps, predictions):
    if not dates or not temps or not predictions:
        print("Not enough data to display the prediction graph.")
        return


    all_dates = dates + [
        f"Day+{i}" for i in range(1, len(predictions) + 1)
    ]


    actual_positions = list(range(len(temps)))


    future_positions = list(
        range(len(temps) - 1, len(temps) + len(predictions))
    )

    future_values = [temps[-1]] + predictions

    plt.figure(figsize=(12, 6))

    plt.plot(
        actual_positions,
        temps,
        marker="o",
        label="Actual Temperature"
    )

    plt.plot(
        future_positions,
        future_values,
        linestyle="--",
        marker="o",
        label="Predicted Temperature"
    )

    plt.axvline(
        x=len(temps) - 1,
        linestyle=":",
        alpha=0.7,
        label="Prediction Starts"
    )

    plt.xticks(range(len(all_dates)), all_dates, rotation=45)
    plt.xlabel("Date / Future Day")
    plt.ylabel("Temperature (°C)")
    plt.title("Historical Data and Future Temperature Estimates")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ---------------------- Menu System ----------------------

def main_menu():
    while True:
        print("\n========== WEATHER ANALYZER MENU ==========")
        print("1. Analyze TXT file")
        print("2. Analyze CSV file")
        print("3. Show Line Graph")
        print("4. Show Bar Graph")
        print("5. Predict Future Weather")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                temps = read_txt("data.txt")
                display_report(temps)

            elif choice == "2":
                dates, temps = read_csv("weather.csv")
                display_report(temps)

            elif choice == "3":
                dates, temps = read_csv("weather.csv")
                show_line_graph(dates, temps)

            elif choice == "4":
                dates, temps = read_csv("weather.csv")
                show_bar_graph(dates, temps)

            elif choice == "5":
                dates, temps = read_csv("weather.csv")

                if len(temps) < 2:
                    print("Add at least 2 valid temperature readings to weather.csv.")
                    continue

                days = int(input("Enter number of days to predict: "))

                if days <= 0:
                    print("Please enter a positive number of days.")
                    continue

                predictions = predict_future(temps, days)

                display_predictions(predictions)
                show_prediction_graph(dates, temps, predictions)

            elif choice == "6":
                print("Exiting program...")
                break

            else:
                print("Invalid choice. Please try again!")

        except FileNotFoundError as error:
            print(f"File not found: {error.filename}")
            print("Ensure data.txt and weather.csv are in the project folder.")

        except ValueError:
            print("Invalid input or temperature data. Check your files and try again.")

        except OSError as error:
            print(f"Could not read the file: {error}")


# ---------------------- Run Program ----------------------

if __name__ == "__main__":
    main_menu()
