class LogiSense {
  constructor({
    apiKey,
    endpoint,
    batch = true,
    batchSize = 10,
    flushInterval = 3000,
  }) {
    if (!apiKey) throw new Error("LogiSense: API key required");
    if (!endpoint) throw new Error("LogiSense: endpoint is required");

    this.apiKey = apiKey;
    this.endpoint = endpoint.replace(/\/$/, "");
    this.batch = batch;
    this.queue = [];
    this.batchSize = batchSize;
    this.flushInterval = flushInterval;

    if (batch) {
      this.startAutoFlush();
    }
  }

  /** Send a single event */
  async send(event) {
    if (this.batch) {
      this.queue.push(event);
      if (this.queue.length >= this.batchSize) {
        this.flush();
      }
      return;
    }

    return this._post(event);
  }

  /** INTERNAL: POST wrapper */
  async _post(payload) {
    try {
      const res = await fetch(`${this.endpoint}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": this.apiKey,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        console.error("LogiSense: Failed to send event", await res.text());
      }
    } catch (err) {
      console.error("LogiSense: Network error", err);
    }
  }

  /** Flush batch queue */
  async flush() {
    if (this.queue.length === 0) return;

    const toSend = [...this.queue];
    this.queue = [];

    await this._post(toSend);
  }

  /** Auto-flush intervals */
  startAutoFlush() {
    this.timer = setInterval(() => this.flush(), this.flushInterval);
  }

  stopAutoFlush() {
    clearInterval(this.timer);
  }
}

export default LogiSense;
