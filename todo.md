# okx-exec-simulator
- [ ] **Day 1: Data Ingestion & Mid‑Price**
  - [ ] Connect to OKX L2 WebSocket and print raw JSON ticks
  - [ ] Implement `OrderBook` class to store top N bids/asks
  - [ ] Compute and log `mid_price()` per tick
  - [ ] Add basic timestamp‑vs‑processing latency log

- [ ] **Day 2: Core Metrics & CLI Output**
  - [ ] Add `vwap(side, qty)` to `OrderBook`
  - [ ] Hard‑code OKX fee tiers and compute “Expected Fees”
  - [ ] Stub a simple slippage model (`slippage = α * qty`)
  - [ ] Print mid‑price, VWAP, fees, slippage to console

- [ ] **Day 3: Basic UI & Logging**
  - [ ] Spin up a minimal Dash app (two‑panel layout)
  - [ ] Display mid‑price, VWAP, fees, slippage stub in UI
  - [ ] Integrate `structlog` for structured console logging
  - [ ] Write unit tests for WebSocket parsing and `OrderBook`

- [ ] **Day 4: Real‑Time Models**
  - [ ] Implement `SlippageEstimator` with `SGDRegressor.partial_fit`
  - [ ] Integrate Almgren‑Chriss impact model function
  - [ ] Build `MakerTakerPredictor` with `SGDClassifier.partial_fit`
  - [ ] Wire live model predictions into Dash callbacks

- [ ] **Day 5: Polish, Testing & Documentation**
  - [ ] Add end‑to‑end integration tests (WS → models → UI)
  - [ ] Benchmark per‑tick ingestion, model inference, UI update latency
  - [ ] Write up README, models.md, and performance.md
  - [ ] Prepare brief demo notes/video outline
