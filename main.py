from abc import ABC, abstractmethod
from datetime import datetime


# Abstract Base Class
class PlanComponent(ABC):
    @abstractmethod
    def get_details(self):
        pass


# Base Class for Places
class Place(ABC):
    def __init__(self, name, country):
        self._name = name
        self._country = country

    @abstractmethod
    def get_details(self):
        pass


class Destination(Place):
    def __init__(self, name, country, cost_per_day, activities):
        super().__init__(name, country)
        self._cost_per_day = cost_per_day
        self._activities = activities

    def get_details(self):
        return f"Destination: {self._name}, {self._country}, Cost/Day: ${self._cost_per_day:.2f}"

    def list_activities(self):
        return self._activities


class Hotel(Place):
    def __init__(self, name, country, price_per_night, rating):
        super().__init__(name, country)
        self._price_per_night = price_per_night
        self._rating = rating

    def get_details(self):
        return f"Hotel: {self._name}, {self._country}, Price/Night: ${self._price_per_night:.2f}, Rating: {self._rating}⭐"


class Activity:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __str__(self):
        return f"{self.name} (Cost: ${self.cost:.2f})"


class Trip(PlanComponent):
    def __init__(self, destination, days, budget, start_date):
        self._destination = destination
        self._hotels = []
        self._activities = []
        self._days = days
        self._budget = budget
        self._start_date = start_date

    def add_hotel(self, hotel):
        self._hotels.append(hotel)

    def add_activity(self, activity):
        self._activities.append(activity)

    def calculate_total_cost(self):
        accommodation_cost = self._days * self._destination._cost_per_day
        activity_cost = sum(activity.cost for activity in self._activities)
        return accommodation_cost + activity_cost

    def is_within_budget(self):
        return self.calculate_total_cost() <= self._budget

    def get_details(self):
        details = f"\nTrip to {self._destination._name}, {self._destination._country}:\n"
        details += f"Start Date: {self._start_date}, Days: {self._days}, Budget: ${self._budget:.2f}\n\nHotels:\n"
        details += "\n".join([hotel.get_details() for hotel in self._hotels]) + "\n"
        details += "\nActivities:\n"
        details += "\n".join(str(activity) for activity in self._activities)
        total_cost = self.calculate_total_cost()
        details += f"\n\nTotal Estimated Cost: ${total_cost:.2f}\n"
        if total_cost > self._budget:
            details += "⚠️ Warning: Your trip exceeds your budget!\n"
        return details


class User:
    def __init__(self, name):
        self._name = name
        self._trips = []

    def plan_trip(self, destination, days, budget, start_date):
        trip = Trip(destination, days, budget, start_date)
        self._trips.append(trip)
        return trip

    def view_trips(self):
        print(f"\n{self._name}'s Trips:")
        for trip in self._trips:
            print(trip.get_details())

# Main Application
if __name__ == "__main__":
    print("Welcome to the Enhanced Vacation Planner!")

    # User Input
    user_name = input("Enter your name: ")
    user = User(user_name)

    # Destinations with Fixed Activities
    destinations = [
        Destination("Paris", "France", 150, [
            Activity("Visit Eiffel Tower", 50),
            Activity("Louvre Museum", 30),
            Activity("Seine River Cruise", 25),
            Activity("Notre Dame Cathedral Tour", 20),
            Activity("French Cooking Class", 100)
        ]),
        Destination("Tokyo", "Japan", 200, [
            Activity("Tokyo Skytree", 40),
            Activity("Sensoji Temple", 0),
            Activity("Mount Fuji Day Trip", 120),
            Activity("Shibuya Crossing Night Walk", 10),
            Activity("Traditional Tea Ceremony", 60)
        ]),
        Destination("New York", "USA", 180, [
            Activity("Statue of Liberty", 25),
            Activity("Central Park Tour", 15),
            Activity("Broadway Show", 120),
            Activity("Empire State Building", 35),
            Activity("Food Tour in Manhattan", 80)
        ])
    ]

    # Destination Selection
    print("\nAvailable Destinations:")
    for i, dest in enumerate(destinations, 1):
        print(f"{i}. {dest.get_details()}")
    dest_choice = int(input("Choose a destination (1-3): ")) - 1
    chosen_destination = destinations[dest_choice]

    # Input Start Date
    while True:
        try:
            start_date = input("Enter the start date of your trip (YYYY-MM-DD): ")
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please enter the date in YYYY-MM-DD format.")

    # Duration Input
    days = int(input("How many days do you want to stay? "))

    # Budget Input
    budget = float(input("Enter your budget: $"))

    # Create Trip
    trip = user.plan_trip(chosen_destination, days, budget, start_date)

    # Hotel Suggestions Based on Destination
    hotel_suggestions = {
        "Paris": [Hotel("Hotel Ritz", "France", 250, 5), Hotel("Budget Stay Paris", "France", 100, 3)],
        "Tokyo": [Hotel("Tokyo Tower Inn", "Japan", 180, 4), Hotel("Capsule Hotel Tokyo", "Japan", 50, 2)],
        "New York": [Hotel("NYC Grand", "USA", 220, 5), Hotel("Budget Inn NYC", "USA", 120, 3)]
    }
    hotels = hotel_suggestions[chosen_destination._name]

    print("\nSuggested Hotels:")
    for i, hotel in enumerate(hotels, 1):
        print(f"{i}. {hotel.get_details()}")
    hotel_choice = int(input("Choose a hotel (1-2): ")) - 1
    trip.add_hotel(hotels[hotel_choice])

    # Select Fixed Activities
    print("\nAvailable Activities:")
    for i, activity in enumerate(chosen_destination.list_activities(), 1):
        print(f"{i}. {activity}")

    activity_choices = input("Select activities by number : ").split(",")
    for choice in activity_choices:
        trip.add_activity(chosen_destination.list_activities()[int(choice) - 1])

    # View Trip Details
    print("\nYour Trip Details:")
    user.view_trips()
