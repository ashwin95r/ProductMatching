# ProductMatching
A simple product matching using Rabin-Karp algorithm

1) Clone the repository
2) Install python
3) Make sure you can import sys and json in python
4) Run :
    python match.py <products file> <listing file> <result file>
  
    The result will be written to <result file> in this format :
      {
        "listings": Array[Listing], 
        "product_name": String
      }
