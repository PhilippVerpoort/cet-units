(() => {
  const root = document.getElementById("cet-calculator");
  if (!root) return;

  // Captured synchronously: `document.currentScript` is only valid while
  // this script (even a deferred one) is initially executing.
  const selfUrl = document.currentScript.src;

  const form = document.getElementById("cet-form");
  const exprInput = document.getElementById("cet-expr");
  const targetInput = document.getElementById("cet-target");
  const contextInput = document.getElementById("cet-context");
  const copyLinkButton = document.getElementById("cet-copy-link");
  const statusEl = document.getElementById("cet-status");
  const resultEl = document.getElementById("cet-result");
  const errorEl = document.getElementById("cet-error");
  const interactiveEls = root.querySelectorAll(
    "#cet-form input, #cet-form select, #cet-form button, .cet-example"
  );

  // Read once at load time, before the fields below get overwritten by the
  // Pyodide setup (e.g. the context dropdown only gets its options once
  // cet_units has loaded).
  const initialParams = new URLSearchParams(window.location.search);
  const initialExpr = initialParams.get("expr") || "";
  const initialTarget = initialParams.get("target") || "";
  const initialContext = initialParams.get("context") || "";
  if (initialExpr) exprInput.value = initialExpr;
  if (initialTarget) targetInput.value = initialTarget;

  function shareUrl() {
    const url = new URL(window.location.href);
    url.search = "";
    const expr = exprInput.value.trim();
    const target = targetInput.value.trim();
    const context = contextInput.value.trim();
    if (expr) url.searchParams.set("expr", expr);
    if (target) url.searchParams.set("target", target);
    if (context) url.searchParams.set("context", context);
    return url;
  }

  function updateUrl() {
    history.replaceState(null, "", shareUrl().toString());
  }

  function setStatus(text) {
    statusEl.textContent = text;
    statusEl.style.display = text ? "block" : "none";
  }

  function showResult(text) {
    resultEl.textContent = text;
    resultEl.style.display = "block";
    errorEl.style.display = "none";
  }

  function showError(text) {
    errorEl.textContent = text;
    errorEl.style.display = "block";
    resultEl.style.display = "none";
  }

  function setInteractive(enabled) {
    interactiveEls.forEach((el) => {
      el.disabled = !enabled;
    });
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Failed to load ${src}`));
      document.head.appendChild(script);
    });
  }

  const PYODIDE_VERSION = "v314.0.3";
  let cetEvaluate = null;

  async function setup() {
    setStatus("Loading Python runtime (Pyodide)…");
    await loadScript(
      `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/pyodide.js`
    );
    const pyodide = await loadPyodide();

    setStatus("Installing cet_units…");
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");

    const wheelFilename = window.CET_UNITS_WHEEL_FILENAME;
    const wheelUrl = new URL(`../dist/${wheelFilename}`, selfUrl).href;
    await micropip.install(wheelUrl);

    await pyodide.runPythonAsync(`
import json

import cet_units
from cet_units import ureg

_flows_dir = cet_units.UNIT_DEFS_PATH / "generated" / "flows"
_emissions_dir = cet_units.UNIT_DEFS_PATH / "generated" / "emissions"

_flows = sorted(p.stem for p in _flows_dir.glob("*.txt"))
_contexts = sorted(
    p.stem
    for p in _emissions_dir.glob("*.txt")
    if p.stem not in ("generic", "species")
)

ureg.define_flows(_flows)

CET_CONTEXTS_JSON = json.dumps(_contexts)


def cet_evaluate(expr, target=None, context=None):
    try:
        # Parsing a not-yet-seen compound unit (e.g. a prefixed species
        # unit like "Mt CO2eq") for the first time while a context is
        # active can leave it half-registered. Parsing it once outside
        # any context first avoids that.
        if target:
            ureg.Unit(target)

        if context:
            with ureg.context(context):
                q = ureg(expr)
                q = q.to(target) if target else q.to_reduced_units()
        else:
            q = ureg(expr)
            q = q.to(target) if target else q.to_reduced_units()

        return json.dumps({"ok": True, "result": str(q)})
    except Exception as exc:
        return json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
`);
    cetEvaluate = pyodide.globals.get("cet_evaluate");

    const contexts = JSON.parse(pyodide.globals.get("CET_CONTEXTS_JSON"));
    contexts.forEach((context) => {
      const option = document.createElement("option");
      option.value = context;
      option.textContent = context;
      contextInput.appendChild(option);
    });
    if (initialContext) contextInput.value = initialContext;

    setStatus("");
    setInteractive(true);

    if (initialExpr) runEvaluate();
  }

  function runEvaluate() {
    if (!cetEvaluate) return;

    const expr = exprInput.value.trim();
    const target = targetInput.value.trim();
    const context = contextInput.value.trim();

    if (!expr) {
      showError("Please enter a quantity or calculation.");
      return;
    }

    const raw = cetEvaluate(expr, target || null, context || null);
    const parsed = JSON.parse(raw);
    if (parsed.ok) {
      showResult(parsed.result);
    } else {
      showError(parsed.error);
    }

    updateUrl();
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    runEvaluate();
  });

  root.querySelectorAll(".cet-example").forEach((button) => {
    button.addEventListener("click", () => {
      exprInput.value = button.dataset.expr || "";
      targetInput.value = button.dataset.target || "";
      contextInput.value = button.dataset.context || "";
      runEvaluate();
    });
  });

  let copyLinkResetTimer = null;

  copyLinkButton.addEventListener("click", () => {
    clearTimeout(copyLinkResetTimer);
    navigator.clipboard
      .writeText(shareUrl().toString())
      .then(() => {
        copyLinkButton.textContent = "Copied!";
      })
      .catch(() => {
        copyLinkButton.textContent = "Copy failed";
      })
      .finally(() => {
        copyLinkResetTimer = setTimeout(() => {
          copyLinkButton.textContent = "Copy Link";
        }, 1500);
      });
  });

  setInteractive(false);

  setup().catch((err) => {
    setStatus("");
    showError(`Failed to load Python runtime: ${err}`);
  });
})();
