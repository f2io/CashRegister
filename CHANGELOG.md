# Changelog

## [0.2.0] - 2026-03-16

### Added
- **`IDenominatorSelector`** interface; denominator selection logic extracted into `DivThreeDenominatorSelector`, decoupling the rule from the handler
- **`ITraceablePipelineFile`** interface combines pipeline I/O with context manager and tracing
- **Typed exception hierarchy** (`CashRegisterError`, `CashRegisterExceptionGroup`, parser and command errors); known errors are wrapped with pipeline context, unknown errors are logged and re-raised as-is

### Changed
- Error output redirected to **stderr**

### Fixed
- Output file is **reset on failure**: if an error propagates during processing, the output is truncated to prevent partial results from being written

### Breaking Change
- `DualDenominatorHandler` renamed to `AutoSelectionDenominatorHandler`; module renamed from `dual_denominator.py` to `filesystem_denominator.py`

---

## [0.1.0] - 2026-03-12

### Added
- Dollar denomination and shuffle-order denomination (applied when owed is divisible by 3)
- Filesystem pipeline, CLI entrypoint, and unit tests
