class PDFProcessor:
    def create_rule_book_chunks(self, book, paragraphs):
        chunks = []
        current_chunk = {
            "Book": book,
            "Chapter": None,
            "Section": None,
            "Chunk_Content": "",
            "Content_Type": "Rules",
            "Pages": []  # Added pages list
        }

        for paragraph in paragraphs:
            page_num = paragraph["boundingRegions"][0]["pageNumber"]
            content = paragraph["content"]

            if "role" in paragraph:
                role = paragraph["role"]

                if role == "title":
                    # If we encounter a new chapter, save the current chunk if it has content
                    if current_chunk["Chunk_Content"]:
                        chunks.append(current_chunk)

                    # Start a new chunk for the new chapter
                    current_chunk = {
                        "Book": book,
                        "Chapter": content,
                        "Section": None,
                        "Chunk_Content": "",
                        "Content_Type": "Rules",
                        "Pages": [page_num]  # Start new pages list
                    }

                elif role == "sectionHeading":
                    # If we encounter a new section, save the current chunk if it has content
                    if current_chunk["Chunk_Content"]:
                        chunks.append(current_chunk)

                    # Start a new section within the current chapter
                    current_chunk = {
                        "Book": book,
                        "Chapter": current_chunk["Chapter"],
                        "Section": content,
                        "Chunk_Content": "",
                        "Content_Type": "Rules",
                        "Pages": [page_num]  # Start new pages list
                    }

                elif role == "pageNumber" or role == "pageFooter":
                    # Ignore page numbers and footers
                    continue

            # Add content to the current chunk
            current_chunk["Chunk_Content"] += content + " "
            # Add page number to the current chunk's pages list if it's not already there
            if page_num not in current_chunk["Pages"]:
                current_chunk["Pages"].append(page_num)

        # Add the last chunk if it has content
        if current_chunk["Chunk_Content"]:
            chunks.append(current_chunk)

        # Adding metadata in content  
        for chunk in chunks:
            chunk["Chunk_Content_w_Metadata"] = (
                f"<Book> {chunk['Book']} </Book> \n\n"
                f"<Chapter> {chunk['Chapter']} </Chapter> \n\n"
                f"<Section> {chunk['Section'] if chunk['Section'] else 'N/A'} </Section> \n\n"
                f"<Page Numbers> {', '.join(map(str, chunk['Pages']))} </Page Numbers> \n\n"
                + chunk["Chunk_Content"] 
            )

        return chunks

pdf_processor = PDFProcessor()