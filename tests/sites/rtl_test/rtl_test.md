# RTL Test Page

This is a test page to demonstrate Right-to-Left (RTL) script support in the QuantEcon Book Theme.

## Arabic Text Example

هذا نص تجريبي باللغة العربية لاختبار دعم الكتابة من اليمين إلى اليسار في هذا الموضوع. يجب أن يظهر النص بشكل صحيح مع التوجيه المناسب.

## Hebrew Text Example

זהו טקסט לדוגמה בעברית לבדיקת תמיכה בכתיבה מימין לשמאל בנושא זה. הטקסט אמור להיות מוצג כראוי עם הכיוון המתאים.

## Mixed Content

When RTL is enabled, the layout should adjust properly while maintaining readability for:

- Code blocks (should remain LTR)
- Mathematical equations
- Navigation elements
- Lists and content structure

```python
# This code should remain left-to-right for readability
def example_function():
    return "Hello World"
```

## Mathematical Content

Mathematical equations should also remain in LTR direction:

$$E = mc^2$$

The equation above should display properly even in RTL mode.

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Value A  | Value B  | Value C  |

Tables should align to the right in RTL mode.
