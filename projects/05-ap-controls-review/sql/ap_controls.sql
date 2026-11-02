-- SQLite-compatible exception-review patterns for invoice_register.csv.
-- The queries identify candidates for a reviewer; they do not determine fraud.

-- Exact duplicate vendor/invoice-number candidates after basic punctuation normalization.
WITH normalized AS (
    SELECT *, upper(replace(replace(replace(trim(invoice_number), '-', ''), '/', ''), ' ', '')) AS invoice_key
    FROM invoice_register
), duplicate_keys AS (
    SELECT vendor_id, invoice_key
    FROM normalized
    GROUP BY vendor_id, invoice_key
    HAVING COUNT(*) > 1
)
SELECT n.invoice_id, n.vendor_id, n.invoice_number, n.amount_inr, 'duplicate_vendor_invoice_number' AS review_rule
FROM normalized n
JOIN duplicate_keys d ON d.vendor_id = n.vendor_id AND d.invoice_key = n.invoice_key;

-- Unpaid exception rules are separate so an invoice can retain every relevant flag.
SELECT invoice_id, vendor_id, invoice_number, amount_inr, 'missing_po_over_threshold' AS review_rule
FROM invoice_register
WHERE paid_flag = 0 AND amount_inr > 50000 AND (po_number IS NULL OR trim(po_number) = '')
UNION ALL
SELECT invoice_id, vendor_id, invoice_number, amount_inr, 'approval_pending_unpaid'
FROM invoice_register
WHERE paid_flag = 0 AND lower(approval_status) <> 'approved'
UNION ALL
SELECT invoice_id, vendor_id, invoice_number, amount_inr, 'bank_change_pending_unpaid'
FROM invoice_register
WHERE paid_flag = 0 AND bank_change_pending = 1
UNION ALL
SELECT invoice_id, vendor_id, invoice_number, amount_inr, 'overdue_unpaid'
FROM invoice_register
WHERE paid_flag = 0 AND due_date < '2026-11-01';

-- Possible near-duplicate pairs: same vendor, amount, and close invoice date but different normalized number.
SELECT a.invoice_id AS invoice_id_a, b.invoice_id AS invoice_id_b,
       a.vendor_id, a.amount_inr, a.invoice_date AS invoice_date_a, b.invoice_date AS invoice_date_b
FROM invoice_register a
JOIN invoice_register b
  ON a.vendor_id = b.vendor_id
 AND a.invoice_id < b.invoice_id
 AND a.amount_inr = b.amount_inr
 AND abs(julianday(a.invoice_date) - julianday(b.invoice_date)) <= 2
 AND upper(replace(replace(replace(a.invoice_number, '-', ''), '/', ''), ' ', ''))
     <> upper(replace(replace(replace(b.invoice_number, '-', ''), '/', ''), ' ', ''));
