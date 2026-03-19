# Architecture Decision Records

## How to fill out an ADR

**Context** — *Why did I need to make a decision at all?*
Describe the situation that forced your hand. What was the problem, constraint, or pressure? What would go wrong if you did nothing?

**Decision** — *What did I choose, and what does it look like?*
State the choice clearly. Name the classes, interfaces, or patterns involved. Just describe what you built.

**Consequences** — *What became easier, harder, or different because of this choice?*
Both positive and negative outcomes. What can you do now that you couldn't before? What did you give up or complicate?

---

## v0.1.0

### ADR-001: Transaction

**Status:** Accepted

**Context:** Input lines (owed, paid) need to be parsed and validated before any denomination logic runs.

**Decision:** Introduce `Transaction` as a dataclass that validates values at construction (`owed >= 0`, `paid > owed`). A `from_string()` factory method handles parsing from string input.

**Consequences:** Any invalid input is rejected early with a typed error before reaching the denomination logic.

---

### ADR-002: Change

**Status:** Accepted

**Context:** The denomination result needs to carry both the change value and the denomination breakdown so both can be verified independently.

**Decision:** `Change[TDenomination]` is a base class holding the change value and a typed denomination. Subclasses implement `__str__()` and `recalculate_value()`, which allows verifying that the denomination adds up to the original change value.

**Consequences:** Both the value and the denomination structure are available on the same object, making it possible to cross-check the math after calculation.

---

### ADR-003: IValueConverter

**Status:** Accepted

**Context:** Each denomination unit (dollar, quarter, dime, nickel, penny) has its own conversion rule. Hardcoding all units in one place makes it hard to add, remove, or reorder them.

**Decision:** Define `IValueConverter` as an interface with `get_identifier()` and `convert(value) -> (count, remaining)`. Each unit is a separate implementation. `get_identifier()` returns the key used to map the converter result to the `Change` DTO. The `Denominator` receives an ordered list of converters.

**Consequences:** New denomination units can be added independently. The converter order controls the greedy algorithm (largest to smallest). A new currency only needs its own converter set.

---

### ADR-004: Denominator

**Status:** Accepted

**Context:** The algorithm for calculating change (iterate converters, accumulate counts, stop early when remainder is zero) is the same regardless of currency or denomination set.

**Decision:** `Denominator` is a base class that owns the `process()` core implementation and delegates to `get_converters()` and `convert_to_change()`, which subclasses provide.

**Consequences:** The change algorithm is defined once. Subclasses only declare which converters to use and how to map the result to a typed `Change` object.

---

### ADR-005: Safeguard converter in DollarDenominatorWithRandomOrder

**Status:** Accepted

**Context:** `DollarDenominatorWithRandomOrder` randomly disables converters each run. If all converters are disabled, the remaining change would have no converter to handle it, producing a mathematically wrong result.

**Decision:** Introduce a `safeguard_converter` (defaults to `PennyConverter`) that is always kept active regardless of random selection. The constructor enforces that the safeguard type is present in the converter list.

**Consequences:** The random denomination always produces a correct result. Any wrong implementation of the converter list is caught at construction time, not silently at runtime.

---

## v0.2.0

### ADR-006: Typed exception hierarchy

**Status:** Accepted

**Context:** Generic exceptions and bare `assert` make it impossible for callers to distinguish expected domain failures (bad input, invalid denomination) from unexpected runtime errors. Additionally, errors propagating across layers lose context about where they originated.

**Decision:** Introduce `CashRegisterError` as the base for all known errors, with subtypes for parsing and command input errors. Known errors are wrapped in `CashRegisterExceptionGroup` enriched with context from the layer that caught it (e.g., line number from the pipeline). Unknown errors are re-raised as-is after logging.

**Consequences:** Callers can handle domain errors explicitly. `CashRegisterExceptionGroup` wraps the error with pipeline context (file name, line number) at the point of failure, making it possible to trace it back to its origin.

---

### ADR-007: IDenominatorSelector

**Status:** Accepted

**Context:** The README raises: *What if the divisor changes? What if another special case is added?* The original handler hardcoded the "divisible by 3 → random denomination" rule inline.

**Decision:** Extract selection logic into `IDenominatorSelector[TInput]`. The handler (`AutoSelectionDenominatorHandler`) depends only on the interface. `DivThreeDenominatorSelector` is the concrete implementation of the current rule.

**Consequences:** New rules (different divisor, additional cases) are added by implementing a new selector, with no changes to the handler.

---

### ADR-008: ITraceablePipelineFile

**Status:** Accepted

**Context:** The pipeline has distinct responsibilities: handling data I/O, providing tracing context, and managing the resource lifecycle. A single class handling all three cannot be partially reused.

**Decision:** Keep the interfaces separate (`IPipeline`, `IPipelineInfo`) and introduce `ITraceablePipelineFile` as a composed interface that combines both with the context manager protocol.

**Consequences:** Each responsibility can evolve independently. Callers that only need one concern depend only on the relevant interface.
