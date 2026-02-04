
def line(prompt):
    print("\n\n",("=" * 10),prompt,("=" * 10))


line("counting word numbers")
sentence = "What is the Airspeed Velocity of an Unladen Swallow?"
words=sentence.split(" ")
result = {word:len(word) for word in words}
print(result)



line("converting celsius to fahrenheit")
weather_c = {"Monday": 12, "Tuesday": 14, "Wednesday": 15, "Thursday": 14, "Friday": 21, "Saturday": 22, "Sunday": 24}
weather_f ={key:(value * 9/5) + 32 for (key,value) in weather_c.items()}
print(weather_f)