from langchain_community.document_loaders import WebBaseLoader

def immunefi_data(program_name):
      url1 = f"https://immunefi.com/bug-bounty/{program_name}/information"
      url2 = f"https://immunefi.com/bug-bounty/{program_name}/scope"
      url3 = f"https://immunefi.com/bug-bounty/{program_name}/resources"

      data1 = WebBaseLoader(url1)
      data2 = WebBaseLoader(url2)
      data3 = WebBaseLoader(url3)

      docs1 = data1.load()
      docs2 = data2.load()
      docs3 = data3.load()

      # print("========== PROGRAM ==========")
      # print(docs1[0].page_content)
      # print(docs2[0].page_content)
      # print(docs3[0].page_content)

      return {
            "information": docs1[0].page_content,
            "scope": docs2[0].page_content,
            "resources": docs3[0].page_content,
      }

# program_name = input("name: ")
# result = immunefi_data(program_name)

# print(result)