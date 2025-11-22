import pypdf
from typing import Dict, Optional

# This can be dynamically generated, but for now, a static map is fine.
LAW_DOCS_PATH = "calendar_agent/docs/"
LAW_FILES: Dict[str, str] = {
    "勞動基準法": f"{LAW_DOCS_PATH}勞動基準法.pdf",
    "勞工保險條例": f"{LAW_DOCS_PATH}勞工保險條例.pdf",
    "勞資爭議處理法": f"{LAW_DOCS_PATH}勞資爭議處理法.pdf",
    "就業服務法": f"{LAW_DOCS_PATH}就業服務法.pdf",
    "性別平等工作法": f"{LAW_DOCS_PATH}性別平等工作法.pdf",
}


def get_law_document(law_name: str) -> Optional[str]:
    """
    Given a law name, returns the content of the law document.
    The available law names are: 勞動基準法, 勞工保險條例, 勞資爭議處理法, 就業服務法, 性別平等工作法.
    """
    file_path = LAW_FILES.get(law_name)
    if not file_path:
        return f"找不到法規 '{law_name}'"

    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except FileNotFoundError:
        return f"找不到法規檔案: {file_path}"
    except Exception as e:
        return f"讀取檔案時發生錯誤: {e}"
