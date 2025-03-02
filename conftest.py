import os
import csv
import zipfile
import pytest
from openpyxl import Workbook, load_workbook
from PyPDF2 import PdfWriter, PdfReader

# Фикстура для временной папки
@pytest.fixture(scope="module")
def temp_dir():
    path = "tmp"
    os.makedirs(path, exist_ok=True)
    yield path
    # Удаляем файлы и папку после тестов
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
    os.rmdir(path)

# Фикстура для создания PDF-файла
@pytest.fixture(scope="module")
def pdf_file(temp_dir):
    pdf_path = os.path.join(temp_dir, "book.pdf")
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=200, height=200)
    with open(pdf_path, "wb") as f:
        pdf_writer.write(f)
    return pdf_path

# Фикстура для создания Excel-файла
@pytest.fixture(scope="module")
def excel_file(temp_dir):
    xlsx_path = os.path.join(temp_dir, "table.xlsx")
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Name", "Age"])
    sheet.append(["Kate", 28])
    sheet.append(["Danil", 25])
    workbook.save(xlsx_path)
    return xlsx_path

# Фикстура для создания CSV-файла
@pytest.fixture(scope="module")
def csv_file(temp_dir):
    csv_path = os.path.join(temp_dir, "manual.csv")
    with open(csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["First", "manual"])
        writer.writerow([1, "Put the button"])
        writer.writerow([2, "Check window"])
    return csv_path

# Фикстура для архивации файлов
@pytest.fixture(scope="module")
def zip_file(temp_dir, pdf_file, excel_file, csv_file):
    zip_path = os.path.join(temp_dir, "files.zip")
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.write(pdf_file, arcname="book.pdf")
        archive.write(excel_file, arcname="table.xlsx")
        archive.write(csv_file, arcname="manual.csv")
    return zip_path