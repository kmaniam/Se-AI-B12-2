PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    customer_id INTEGER,
    customer_name TEXT,
    order_id TEXT,
    complaint TEXT NOT NULL,
    category TEXT,
    urgency TEXT,
    sentiment TEXT,
    kb_sources TEXT,
    response TEXT,
    confidence REAL,
    status TEXT NOT NULL DEFAULT 'Open',
    escalation_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS agent_execution_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    execution_status TEXT,
    executed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id)
        REFERENCES tickets(ticket_id)
);

CREATE TABLE IF NOT EXISTS knowledge_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL UNIQUE,
    category TEXT,
    description TEXT,
    indexed_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS escalations (
    escalation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL,
    escalation_reason TEXT NOT NULL,
    assigned_to TEXT DEFAULT 'Human Support',
    escalation_status TEXT DEFAULT 'Pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved_at TEXT,
    FOREIGN KEY (ticket_id)
        REFERENCES tickets(ticket_id)
);

CREATE INDEX IF NOT EXISTS idx_tickets_status
ON tickets(status);

CREATE INDEX IF NOT EXISTS idx_tickets_category
ON tickets(category);

CREATE INDEX IF NOT EXISTS idx_agent_logs_ticket
ON agent_execution_logs(ticket_id);