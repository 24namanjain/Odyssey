-> Factory Design Pattern

* Intent
    * Prvide a way to create objects using a common interface without exposing creation logic
    * Allows the actual object type to be determined at runtime
* Problem
    * We want to localize the object creation logic
* Solution
    * Create a factory class that creates objects for us
    * The factory class will have a method that creates the object

* Use Case
    * When we want to create an object but we don't know the actual type of the object at compile time