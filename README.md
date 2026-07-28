# First Aid RAG Assistant

مشروع RAG بسيط بيحول كتاب إسعافات أولية (PDF) لمساعد يجاوب على الأسئلة بناءً على محتوى الكتاب.

## تسلسل الأنابيب (Pipeline)
```
documents -> preprocessing -> chunking -> vector representation -> vector store -> context retrieval -> prompting -> Streamlit UI
```

## طريقة التشغيل محليًا (بالترتيب، مرة واحدة فقط)

1. حطي ملف `first_aid_book.pdf` في نفس المجلد.
2. ثبتي المتطلبات:
   ```bash
   pip install -r requirements.txt
   sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-ara
   ```
3. اعملي ملف `.env` (منسوخ من `.env.example`) وحطي فيه مفتاحك الحقيقي — الملف ده متعرفش تعمليه commit لأنه موجود في `.gitignore`.
4. شغلي الخطوات بالترتيب:
   ```bash
   python 01_documents.py
   python 02_preprocessing.py
   python 03_chunking.py
   python 04_vector_representation.py
   python 05_create_chroma_store.py
   ```
5. اختباري الاسترجاع والـ prompting (اختياري):
   ```bash
   python 06_retrieve_context.py
   python 07_prompting.py
   ```
6. شغلي الواجهة:
   ```bash
   streamlit run streamlit_app.py
   ```

## النشر على Streamlit Cloud
1. ارفعي المشروع على GitHub — **بدون** ملف `.env` وبدون المفتاح الحقيقي.
2. في Streamlit Cloud: افتحي التطبيق -> Manage app -> Secrets، وضيفي:
   ```toml
   OPENROUTER_API_KEY = "your_openrouter_key_here"
   OPENROUTER_MODEL = "openai/gpt-4o-mini"
   ```
3. ملف `packages.txt` موجود عشان يتثبت `poppler` و`tesseract` تلقائيًا على السيرفر.
4. لازم تكوني رفعتي مجلد `chroma_store/` (الناتج من خطوة 5) مع المشروع، أو تشغلي خطوات 1-5 قبل الرفع، لأن السيرفر مش هيعمل OCR من الصفر كل مرة.

## Checklist قبل التسليم
- [ ] كل الملفات المطلوبة موجودة (01 -> 07 + streamlit_app.py + requirements.txt)
- [ ] `requirements.txt` موجود
- [ ] مفيش مفتاح API حقيقي في الـ ZIP أو الـ GitHub repo
- [ ] Streamlit secrets متظبطة بصيغة TOML صحيحة
- [ ] التطبيق شغال على Streamlit فعليًا
- [ ] الإجابة مبنية على السياق المسترجع (retrieved context)
- [ ] الإجابة بتذكر المصادر (sources)
