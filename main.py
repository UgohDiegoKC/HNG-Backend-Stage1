from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

def is_armstrong(number: int) -> bool:
    """Check if a number is an Armstrong number"""
    digits = [int(d) for d in str(number)]
    power = len(digits)
    return sum(d ** power for d in digits) == number

def get_fun_fact(number: int) -> str:
    """Fetch a fun fact about the number from Numbers API"""
    response = requests.get(f"http://numbersapi.com/{number}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

@app.get("/api/classify-number")
async def classify_number(number: str):
    """Classifies a number based on mathematical properties"""
    if not number.isdigit():
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

    number = int(number)
    is_prime = number > 1 and all(number % i != 0 for i in range(2, int(number ** 0.5) + 1))
    is_perfect = sum(i for i in range(1, number) if number % i == 0) == number
    digit_sum = sum(int(digit) for digit in str(number))
    
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    return {
        "number": number,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": get_fun_fact(number)
    }
