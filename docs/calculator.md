---
hide:
  - navigation
  - toc
---

# Calculator

Try `cet_units` directly in this page. Enter a quantity or a calculation
(anything [pint](https://pint.readthedocs.io/) can parse) and, optionally, a
target unit and a GWP assessment context.

<div id="cet-calculator" class="cet-calculator">
  <form id="cet-form">
    <div class="cet-field">
      <label for="cet-expr">Quantity or calculation</label>
      <input type="text" id="cet-expr" name="expr" value="" placeholder="e.g. 1 TWh" autocomplete="off" disabled>
    </div>
    <div class="cet-field">
      <label for="cet-target">Target unit <span class="cet-optional">(optional)</span></label>
      <input type="text" id="cet-target" name="target" placeholder="e.g. EJ" autocomplete="off" disabled>
    </div>
    <div class="cet-field">
      <label for="cet-context">GWP context <span class="cet-optional">(optional)</span></label>
      <select id="cet-context" name="context" disabled>
        <option value="">(none)</option>
      </select>
    </div>
    <button type="submit" id="cet-submit" disabled>Evaluate</button>
    <button type="button" id="cet-copy-link" disabled>Copy Link</button>
  </form>

  <p id="cet-status" class="cet-status">Loading Python runtime…</p>
  <pre id="cet-result" class="cet-result" style="display:none;"></pre>
  <pre id="cet-error" class="cet-error" style="display:none;"></pre>

  <p class="cet-examples">
    Examples:
    <button type="button" class="cet-example" data-expr="1 USD_2020" data-target="EUR_2024" data-context="" disabled>USD_2020 → EUR_2024</button>
    <button type="button" class="cet-example" data-expr="1 Mt CH4" data-target="Mt CO2eq" data-context="AR6GWP100" disabled>Mt CH₄ → Mt CO₂eq</button>
    <button type="button" class="cet-example" data-expr="1 kg_H2" data-target="kWh_H2_LHV" data-context="" disabled>kg H₂ → kWh H₂ (LHV)</button>
    <button type="button" class="cet-example" data-expr="100 cubic_meter_NG_norm × (50 EUR_2024/MWh_NG_LHV + (200 g CO2 + 10 g CH4) / kWh_NG_LHV × 80 EUR_2024 / t CO2eq)" data-target="USD_2024" data-context="AR6GWP100" disabled>advanced calculation</button>
  </p>
</div>


## How it works

The calculator above works locally in your browser via 
[Pyodide](https://pyodide.org/) — a WebAssembly build of CPython.

When the field for a target unit is left empty, the expression is
evaluated and reduced to its default units, equivalent to:

```python
from cet_units import ureg

ureg("2 MWh/t * 3 Mt").to_reduced_units()
```

When a target unit is given, `.to(target)` is used instead. When a GWP
context is also given (e.g. `AR6GWP100`), it is passed along as
`.to(target, context)`, as required for converting between different
greenhouse-gas species.

The page address bar always reflects the current inputs, so it can be
copied and shared directly; the "Copy Link" button does the same via the
clipboard. Opening a shared link pre-fills the form and evaluates it
automatically.
