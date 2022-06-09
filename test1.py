from seoanalyzer2 import analyze

print(analyze('http://kevinmartinlaw.com',
    min_title_length=10,
    max_title_length=70,
    min_description_length=120,
    max_description_length=255))