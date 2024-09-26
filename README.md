**This is a draft**

How to set up the project? 
1. Open your terminal and navigate to the project directory.
2. Install the dependencies by running the following command:

```pip install -r requirement.txt```

Info for analytics:
1. year = 0 means that no year was provided while entering the data into the system

Info of the data:
1. Data is pre-cleaned:
    - duplicates are removed (there are movies of the same title but different directors, hence different movies)
    - whitespaces are trimmed
2. Data is normalized:
    - consistent formatting, such as capitalizing the title and director names
    - consistent data type

What hasn't been done:
- verification of outliers