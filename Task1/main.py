from datetime import date
from jugaad_data.nse import bhavcopy_save

fileName = bhavcopy_save(date(2023,5,29), ".")
print(fileName)

