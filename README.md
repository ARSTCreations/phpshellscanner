# phpshellscanner

an ARSTCreations<br>
**[Disclaimer]**<br>
This program is an experimental tool for educational purpose and is not guaranteed to be accurate and/or complete. Any use of this program is at your own risk.

## A Python Cosine Similarity and Keyword Based PHP Shell Scanner

It scans for shells based on cosine similarity with a given set of php webshells collection.

## How Does it Works?

- It calculates the cosine similarity between a file and the webshells collection.
- If the cosine similarity is greater than 0.3, it suspects the file, prints the webshell name and the cosine similarity.
- if the webshells collection depleted, it continues to scan for common keywords in the file.
- if the file contains common keywords, it suspects the file, prints the webshell name and the keyword.
- if the file contains common keywords and the webshells collection depleted, it will finally decide that the file is not a webshell.

### To-dos

- [x] Cosine Similarity
- [x] Keywords Matching
- [ ] MD5 Hash Matching

### Contributions by pulling requests are welcome :)

phpshellscanner © 2022 by Rizaldy Aristyo is licensed under CC BY-SA 4.0
