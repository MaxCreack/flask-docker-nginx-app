#!/bin/bash

BASE_URL="http://localhost:5000"

echo "Testing / route..."
curl "$BASE_URL/"
echo -e "\n"

echo "Testing /add route (5 + 3)..."
curl "$BASE_URL/add?x=5&y=3"
echo -e "\n"

echo "Testing /subtract route (10 - 4)..."
curl "$BASE_URL/subtract?x=10&y=4"
echo -e "\n"

echo "Testing /multiply route (7 * 6)..."
curl "$BASE_URL/multiply?x=7&y=6"
echo -e "\n"

echo "Testing /divide route (20 / 5)..."
curl "$BASE_URL/divide?x=20&y=5"
echo -e "\n"

echo "Testing /divide route with division by zero..."
curl "$BASE_URL/divide?x=20&y=0"
echo -e "\n"

echo "Testing /add with missing parameters..."
curl "$BASE_URL/add?x=10"
echo -e "\n"
