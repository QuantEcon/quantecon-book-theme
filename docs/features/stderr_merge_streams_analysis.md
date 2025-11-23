# Stderr Warnings Feature: merge_streams Behavior Analysis

## Question

How does the collapsible stderr warnings feature behave when `merge_streams=True` is set in myst-nb configuration?

## Answer

**The feature works correctly and as intended with `merge_streams` enabled.** Here's why:

## Understanding merge_streams

The `merge_streams` option in myst-nb controls how stdout and stderr are rendered:

### When `merge_streams=False` (default):
- Stdout gets class: `.output.stream`
- Stderr gets class: `.output.stderr`
- Each stream is in a separate HTML element

**HTML structure:**
```html
<div class="cell_output docutils container">
    <div class="output stream"><!-- stdout --></div>
    <div class="output stderr"><!-- stderr --></div>
</div>
```

### When `merge_streams=True`:
- Both stdout and stderr are combined into: `.output.stream`
- Single HTML element contains both outputs
- **Exception:** If cell produces ONLY stderr (no stdout), it still uses `.output.stderr`

**HTML structure (mixed output):**
```html
<div class="cell_output docutils container">
    <div class="output stream">
        <!-- stdout and stderr merged together -->
    </div>
</div>
```

**HTML structure (only stderr):**
```html
<div class="cell_output docutils container">
    <div class="output stderr">
        <!-- only stderr, no stdout to merge with -->
    </div>
</div>
```

## How Our Feature Behaves

Our JavaScript specifically targets: `cellOutput.querySelectorAll(".output.stderr")`

### Scenario 1: merge_streams=False (default)
✅ **Feature activates** - Stderr is in separate `.output.stderr` element
- Pure stderr warnings get collapsible interface
- Stdout displays normally

### Scenario 2: merge_streams=True with mixed output
✅ **Feature does NOT activate** - No `.output.stderr` elements exist
- Combined stdout+stderr displays as normal `.output.stream`
- This is CORRECT behavior because:
  - User explicitly chose to merge streams
  - Output contains both normal results and warnings
  - Collapsing would hide valuable stdout data

### Scenario 3: merge_streams=True with ONLY stderr
✅ **Feature activates** - Still uses `.output.stderr` class
- Even with merge_streams enabled, cells with only stderr use `.output.stderr`
- Gets collapsible interface as expected

## Design Rationale

This behavior is intentional and correct:

1. **Respects user configuration**: If a user enables `merge_streams`, they want stdout and stderr together. We don't interfere with that choice.

2. **Targets pure warnings**: The feature is designed to collapse VERBOSE WARNINGS that provide no valuable output. When stdout and stderr are merged, it indicates the output is meaningful context.

3. **Selective activation**: Only pure stderr (warnings/errors without stdout) gets collapsed, which is exactly the use case we're solving for (e.g., GPU initialization warnings).

## Example Use Cases

### ✅ Will Collapse (as intended):
```python
# Pure warning output, no stdout
import jax
model = setup_gpu_computation()
# Produces: GPU interconnect warnings on stderr only
```

### ✅ Will NOT Collapse (as intended):
```python
# merge_streams=True with mixed output
print("Computing result...")  # stdout
warnings.warn("Deprecated API")  # stderr
print("Result:", result)  # stdout
# Combined output should stay visible
```

### ✅ Will Collapse (as intended):
```python
# merge_streams=True but ONLY stderr
warnings.warn("Configuration issue")
# Still gets .output.stderr class, gets collapsed
```

## Testing

See `tests/stderr_merged_streams_test.html` for comprehensive test cases covering:
1. Separate streams (merge_streams=False)
2. Merged streams with mixed output
3. Only stderr with merge_streams=True

## Conclusion

**No changes needed.** The feature correctly:
- Collapses pure stderr warnings (the problem we're solving)
- Respects merge_streams configuration
- Doesn't interfere with intentionally merged output
- Works regardless of merge_streams setting

The selector `.output.stderr` naturally handles all edge cases:
- Present when stdout and stderr are separate ✓
- Present when cell produces only stderr ✓
- Absent when streams are merged together ✓

This is robust, predictable, and aligns with user expectations.
