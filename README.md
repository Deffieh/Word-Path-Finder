# Word Path Finder (Python Project 2022-2023)

## Introduction
This university project aims to create a system capable of finding paths connecting two words through a predefined set of rules. The goal is to calculate the distance between the words using the fewest possible rules, according to specific criteria.

## Operation
1. **Input of Words**: The program takes two words from the user as input, which can either be already present in the dictionary or new.

2. **Construction of Data Structure**: Using a provided file containing a list of Italian words, the program builds a data structure allowing access to all the words.

3. **Application of Rules**: The system utilizes a set of predefined rules to find paths connecting the two user-input words. These rules include:
   - R1: Adding/removing a letter.
   - R2: Anagram.
   - R3: Substituting a letter.
   - Additional rules as needed.

4. **Calculation of Distance**: The system calculates the distance between the two words by counting the number of rules applied to transform one word into the other.

5. **Optimization**: To improve performance, the program may include heuristics such as limits on the maximum number of rules to apply.

6. **Handling of Absent Words**: The path must only contain words present in the dictionary. If a word is absent, the system should handle it appropriately.

## Implementation
- **Flexibility of Rules**: Rules have varying weights and can be duplicated to handle specific cases, such as adding a letter at the beginning or end of a word.
- **Algorithms**: There are no constraints on the algorithm to use, allowing for implementation of any complexity.
- **Optimization**: For an arbitrary set of rules, the program should be fast, especially when searching for closely related words.
- **Optional Heuristics**: To handle complex situations, optional heuristics like limiting the number of rules applied may be introduced.

## Conclusion
This project provides a method to calculate the distance between two words by applying predefined rules. Its implementation is flexible and can be optimized as needed.
