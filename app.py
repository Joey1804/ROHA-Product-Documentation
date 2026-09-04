import streamlit as st
from jinja2 import Template
from weasyprint import HTML
import os

# Đường dẫn đến file wkhtmltopdf.exe đã cài ở Bước 1
PATH_TO_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

st.set_page_config(page_title="SPEC PDF Generator", layout="wide")

st.title("📄 Công Cụ Tạo File Material Specification")
st.write("Nhập các thông số")

# 1. Thông tin chung
st.subheader("1. Thông tin Chung (Header & Metadata)")
col1, col2, col3 = st.columns(3)

with col1:
    material_desc = st.text_input("Material Desc.", "SIMACID BLUE 80 (ABL80)")
    material_no = st.text_input("Material No.", "SMID000026698")
    cas_no = st.text_input("CAS No.", "4474-24-2")

with col2:
    issue_no = st.text_input("Issue No.", "2")
    issue_date = st.date_input("Issue Date")
    status = st.selectbox("Status", ["Approved", "Pending", "Draft"])

with col3:
    ci_name = st.text_input("C.I. Name", "Acid Blue 80")
    einecs_no = st.text_input("EINECS No.", "224-748-4")
    shelf_life = st.text_input("Shelf Life", "1825 Days from the date of delivery in packed conditions.")

st.markdown("---")

# 2. Bảng chỉ tiêu kỹ thuật
st.subheader("2. Thông số Kỹ thuật (Specification Items)")

default_specs = [
    {"spec_name": "Appearance", "method": "", "uom": "", "requirement": "Blue powder"},
    {"spec_name": "Strength", "method": "", "uom": "%", "requirement": "(Min) 95,00"},
    {"spec_name": "pH Value", "method": "", "uom": "", "requirement": "6,0-10,0"},
]

# Sử dụng data_editor cho phép thêm/xóa/sửa hàng trực tiếp như Excel
edited_specs = st.data_editor(
    default_specs,
    num_rows="dynamic",
    column_config={
        "spec_name": "Specification",
        "method": "Method",
        "uom": "UOM",
        "requirement": "Requirements"
    },
    use_container_width=True
)

st.markdown("---")

# 3. Nút Tạo PDF & Tải về
st.subheader("3. Xuất File PDF")

if st.button("🚀 Tạo File PDF SPEC", type="primary", use_container_width=True):
    if not os.path.exists("template.html"):
        st.error("Không tìm thấy file 'template.html' trong cùng thư mục!")
    else:
        try:
            # 1. Đọc file HTML Template
            with open("template.html", "r", encoding="utf-8") as f:
                html_template = f.read()

            # 2. Gom dữ liệu
            context = {
                "company_name": "PT.ROHA LAUTAN PEWARNA",
                "slogan": "INNOVATING FOR YOU WITH YOU",
                "address": "Kawasan Green Land, Kav. Batavia BD/2, Cikarang Pusat-17530",
                "tel": "62-21-8997 0302",
                "fax": "62-21-8997 3247",
                "email": "roha.indonesia@rohagroup.com",
                "material_desc": material_desc,
                "material_no": material_no,
                "cas_no": cas_no,
                "issue_no": issue_no,
                "issue_date": issue_date.strftime("%d.%m.%Y"),
                "status": status,
                "ci_name": ci_name,
                "einecs_no": einecs_no,
                "shelf_life": shelf_life,
                "items": edited_specs
            }

            # 3. Render HTML
            template = Template(html_template)
            rendered_html = template.render(context)

            # 4. Xuất PDF bằng WeasyPrint
            pdf_bytes = HTML(string=rendered_html).write_pdf()

            st.success("Tạo file PDF thành công!")
            st.download_button(
                label="📥 Tải Xuống File PDF SPEC",
                data=pdf_bytes,
                file_name=f"SPEC_{material_no}_{material_desc}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi xuất PDF: {str(e)}")