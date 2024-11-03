"""Program to convert PDF documents to markdown format
using the Docling library"""

import streamlit as st
from docling.document_converter import DocumentConverter

# Display the title of the page
st.title("Convert Documents with Docling")

# Display a message to inform users about the purpose of the tool
st.write("This tool uses Docling to convert PDF documents into Markdown format.")

# Create a text input field for users to enter the URL of the PDF document
pdf_url = st.text_input("Enter the URL of the PDF document to convert:", "")

# Check if the user has entered a valid URL
if pdf_url:
    # Convert the PDF document using Docling and write the output to the display
    converter = DocumentConverter()
    try:
        with st.spinner(text="Processing document..."):
            result = converter.convert(pdf_url)
            st.success("Conversion completed successfully.")
        st.markdown(result.document.export_to_markdown())
    except RuntimeError as e:
        st.error("Error converting PDF document:", str(e))
else:
    # Display an error message if the user hasn't entered a valid URL
    st.error("Please enter a valid URL for the PDF document.")
