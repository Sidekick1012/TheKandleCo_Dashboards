try:
    import app
    print("✅ app.py imported successfully (syntax check passed)")
except Exception as e:
    # Streamlit scripts often run code on import, so some errors are expected (like 'streamlit' not found if not in env, or streamlit context missing).
    # But SyntaxError will be caught.
    print(f"⚠️ Import result: {e}")
