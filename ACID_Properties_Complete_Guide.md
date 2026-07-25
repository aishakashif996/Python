# ACID Properties: Reliable Database Management

A comprehensive study guide covering **Atomicity, Consistency, Isolation, and Durability**—the four pillars of database reliability.

**Derived from Database Management lectures and course materials.**

---

## Table of Contents

1. [Introduction](#introduction)
2. [A - Atomicity](#a---atomicity-all-or-nothing)
3. [C - Consistency](#c---consistency-valid-state-to-valid-state)
4. [I - Isolation](#i---isolation-concurrent-independence)
5. [D - Durability](#d---durability-permanent-disk-storage)
6. [ACID Quick Reference](#acid-quick-reference)
7. [Code Examples](#code-examples)
8. [Key Takeaways](#key-takeaways)

---

## Introduction

### What is ACID?

**ACID** is an acronym for four properties that guarantee reliable database transactions:

- **A**tomicity - All or nothing
- **C**onsistency - Valid state to valid state
- **I**solation - No interference between concurrent transactions
- **D**urability - Permanent disk storage

These properties ensure that databases maintain data integrity even during failures, concurrent access, and system crashes.

### Why ACID Matters

Without ACID properties:
- ❌ Partial transactions could corrupt data
- ❌ Concurrent users could overwrite each other's changes
- ❌ Power failures could lose data permanently
- ❌ Invalid states could be visible to users

---

## A - ATOMICITY (All or Nothing)

### One-Liner Definition

> **"Atomicity ensures that a transaction is all-or-nothing: either all operations complete successfully and commit, or none do and the transaction rolls back."**

### Detailed Explanation

Atomicity prevents partial transactions. If any operation fails, the entire transaction is rolled back to maintain database integrity. This prevents inconsistent states where some changes are applied and others are not.

### Money Transfer Example: A ⇒ B (500 from each)

**Initial State:** A = 2000, B = 2000 | Total = 4000

#### With Atomicity (All-or-Nothing) ✅

```
Step 1: A debit 500 → A = 1500 (in progress)
Step 2: B credit 500 → B = 2500 (in progress)
Step 3: COMMIT → Final: A = 1500, B = 2500 ✅

Status: Both operations committed successfully
Result: Total = 4000 (money conserved)
```

#### Without Atomicity (Risky) ❌

```
Step 1: A debit 500 → A = 1500 (committed)
Step 2: B credit 500 → CRASH! ⚡ (not committed)

After reboot:
A = 1500 (debit happened)
B = 2000 (credit never happened)
Total = 3500 ❌ MONEY LOST!
```

#### If Crash Before COMMIT ✅

```
Step 1: A debit 500 → A = 1500 (in progress)
Step 2: ⚡ POWER CRASH (before COMMIT)

Recovery: ROLLBACK entire transaction
Result: A = 2000, B = 2000 (back to original state) ✅
```

### Key Takeaway

**Atomicity = "Either entire transaction succeeds or fails completely—no half-transactions."**

---

## C - CONSISTENCY (Valid State to Valid State)

### One-Liner Definition

> **"Consistency ensures database moves from one valid state to another. Rules/constraints never violated."**

### Detailed Explanation

Database constraints (primary keys, foreign keys, checks) enforce consistency. The database maintains invariants—rules that must always be true.

Examples of invariants:
- No negative account balances
- Total money in system stays constant
- No duplicate primary keys
- No null values in required fields

### Money Transfer Consistency Rule

**Constraint:** Sum of all account balances = Total_Money (always 4000)

#### Valid State Transitions ✅

```
Before Transaction: A=2000, B=2000 → Total=4000 ✅ VALID

During Step 1 (debit only): A=1500, B=2000 → Total=3500 ❌ INVALID
(This state is NEVER visible to users—transaction in progress)

After Step 2 (both complete): A=1500, B=2500 → Total=4000 ✅ VALID

The database ensures it never shows the INVALID state to users!
```

#### Invalid State Prevention

```
Transaction: UPDATE seats SET available = -5 WHERE id = 1

Constraint: CHECK (available >= 0)

Result: ❌ REJECTED (violates constraint)
Database prevents impossible state (negative seats)
```

### Key Takeaway

**Consistency = "Database never shows impossible/invalid data—constraints enforced."**

---

## I - ISOLATION (Concurrent Independence)

### One-Liner Definition

> **"Isolation ensures concurrent transactions don't interfere. Each runs independently via locks."**

### Detailed Explanation

Multiple transactions can run at the same time, but locks prevent conflicts. Transactions are isolated from each other, as if they execute serially (one after another).

### Airline Ticket Example: 1 Seat Left

Scenario: **Passenger A & Passenger B try to book the same seat simultaneously**

Goal: **Prevent double booking**

---

## Quick Reference: All Three Isolation Levels

```
Transaction A: Book 1 seat
Transaction B: Book same seat

READ UNCOMMITTED:
├─ A: reads 1 seat (uncommitted change seen by B)
├─ B: reads 1 seat (dirty read!)
└─ Both book → CONFLICT ❌

READ COMMITTED:
├─ A: reads 1 seat, books, COMMITS
├─ B: reads 0 seats (waits for A to commit)
└─ B gets error (no seat) ✅

SERIALIZABLE:
├─ A: LOCKS seat row
├─ B: waits (blocked)
├─ A: books, releases lock
└─ B: books (if available) ✅
```

---

### Level 1: READ UNCOMMITTED (Risky) ❌

#### Definition
Transactions can read **uncommitted (dirty) changes** from other transactions.

#### Problems It Causes
- ✅ Dirty reads (most risky)
- ✅ Lost updates
- ✅ Non-repeatable reads
- ✅ Phantom reads

#### How It Fails

```
Time | Passenger A (Tx1) | Passenger B (Tx2) | Seats | Status
-----|------------------|------------------|-------|--------
 1   | BEGIN            |                   | 1     |
 2   | READ seats → 1   |                   | 1     |
 3   |                  | BEGIN             | 1     |
 4   |                  | READ seats → 1    | 1     | DIRTY READ!
 5   | UPDATE seats = 0 |                   | 0     | (uncommitted)
 6   |                  | BOOK same seat    | 0     |
 7   | COMMIT           |                   | 0     |
 8   |                  | COMMIT            | 0     |

RESULT: ❌ CONFLICT! Both booked same seat (double booking)
```

#### Timeline
```
A: reads 1 seat (uncommitted change seen by B)
B: reads 1 seat (dirty read!)
Both book → CONFLICT ❌
```

#### Why It Fails
- B reads uncommitted change from A
- Both think 1 seat available
- Both book → impossible state created
- Money/seat lost

#### Speed
🟢 **Fastest** (no locks = fastest execution)

#### Use Case
Rarely used. Only for non-critical reporting where speed matters more than accuracy.

---

### Level 2: READ COMMITTED (Default in Most Databases) ✅

#### Definition
Transactions can only read **committed data**. Prevents dirty reads but allows other conflicts.

#### Problems It Prevents
- ❌ Dirty reads (PREVENTED)

#### Problems It Allows
- ✅ Lost updates
- ✅ Non-repeatable reads
- ✅ Phantom reads

#### How It Works

```
Time | Passenger A (Tx1) | Passenger B (Tx2) | Seats | Status
-----|------------------|------------------|-------|--------
 1   | BEGIN            |                   | 1     |
 2   | READ seats → 1   |                   | 1     |
 3   | UPDATE seats = 0 |                   | 0     | (locked)
 4   |                  | BEGIN             | 1     |
 5   |                  | TRY READ seats    | 1     | (waits...)
 6   | COMMIT           |                   | 0     | (lock released)
 7   |                  | READ seats → 0    | 0     | (now can read)
 8   |                  | Cannot book!      | 0     | ❌ No seat
 9   |                  | COMMIT (error)    | 0     |

RESULT: ✅ CORRECT! B cannot book (no seat available)
```

#### Timeline
```
A: reads 1 seat, books, COMMITS
B: reads 0 seats (waits for A to commit)
B gets error (no seat) ✅
```

#### Why It Works
- A's write lock prevents B from reading during transaction
- B waits for A's lock to be released
- B reads actual current value (0 seats)
- B gets correct error: no seat available

#### Locking Mechanism
- **Read operations:** No lock (released immediately)
- **Write operations:** Lock held until COMMIT

#### Speed
🟡 **Medium** (moderate locking overhead)

#### Use Case
Default in PostgreSQL, Oracle. Most web applications. Good balance between safety and performance.

---

### Level 3: SERIALIZABLE (Highest Safety) ✅

#### Definition
Complete isolation. Transactions execute **as if they run one after another** (serially).

#### Problems It Prevents
- ❌ Dirty reads (PREVENTED)
- ❌ Lost updates (PREVENTED)
- ❌ Non-repeatable reads (PREVENTED)
- ❌ Phantom reads (PREVENTED)

#### All Problems Solved! 
**No conflicts possible.**

#### How It Works

```
Time | Passenger A (Tx1) | Passenger B (Tx2) | Seats | Locks   | Status
-----|------------------|------------------|-------|---------|--------
 1   | BEGIN            |                   | 1     |         |
 2   | LOCK entire rows |                   | 1     | A:FULL  |
 3   | READ seats → 1   |                   | 1     | A:FULL  |
 4   |                  | BEGIN             | 1     |         |
 5   |                  | TRY READ seats    | 1     |         | BLOCKED!
 6   | UPDATE seats = 0 |                   | 0     | A:FULL  |
 7   |                  |                   | 0     |         | (waiting...)
 8   | COMMIT           |                   | 0     |         | (lock released)
 9   |                  | LOCK entire rows  | 0     | B:FULL  | (gets lock)
 10  |                  | READ seats → 0    | 0     | B:FULL  |
 11  |                  | Cannot book       | 0     | B:FULL  |
 12  |                  | COMMIT            | 0     |         |

RESULT: ✅ CORRECT! Complete isolation (serial-like execution)
```

#### Timeline
```
A: LOCKS seat row
B: waits (blocked)
A: books, releases lock
B: books (if available) ✅
```

#### Why It Works
- A locks entire seat range/table (full lock)
- B completely blocked (cannot proceed at all)
- Transactions appear to execute one-after-another
- Maximum safety, but slowest speed

#### Locking Mechanism
- **Full locks** on rows AND ranges
- **Highest lock overhead**
- Transactions are serialized

#### Speed
🔴 **Slowest** (maximum locking = maximum safety)

#### Use Case
Critical systems: banking, stock trading, medical records, airline reservations—where data integrity is paramount and correctness matters more than speed.

---

### Isolation Levels Comparison

| Level | Read Locks | Write Locks | Dirty Reads | Lost Updates | Repeatable Reads | Phantom Reads | Speed |
|-------|:----------:|:-----------:|:-----------:|:------------:|:----------------:|:-------------:|-------|
| **READ UNCOMMITTED** | None | Short | ✅ YES | ✅ YES | ✅ YES | ✅ YES | 🟢 Fast |
| **READ COMMITTED** | None | Until commit | ❌ NO | ✅ YES | ✅ YES | ✅ YES | 🟡 Medium |
| **REPEATABLE READ** | Full tx | Full tx | ❌ NO | ❌ NO | ❌ NO | ✅ YES | 🟡 Medium |
| **SERIALIZABLE** | Full range | Full range | ❌ NO | ❌ NO | ❌ NO | ❌ NO | 🔴 Slow |

### Key Takeaway

**Isolation = "Concurrent transactions are independent—locks prevent conflicts, series-like execution."**

---

## D - DURABILITY (Permanent Disk Storage)

### One-Liner Definition

> **"Durability ensures committed data permanently survives to disk—even power outages."**

### Detailed Explanation

Implementation: **Write-Ahead Logging (WAL)**. Logs are written to disk BEFORE commit.

The principle: Never overwrite data on disk until you've written a log entry that says "this transaction committed."

### WAL Process: Step-by-Step

```
Step 1: Transaction executes
        ├─ UPDATE seats = 0
        └─ Data in RAM (volatile, temporary)

Step 2: Write to WAL log file
        ├─ "UPDATE seats = 0" saved to DISK
        └─ Log file is permanent

Step 3: COMMIT command
        ├─ Mark log entry as "committed"
        └─ Signal disk: data is permanent

Step 4: ⚡ POWER CRASH
        └─ (happens before main database write)

Step 5: System reboots
        ├─ Read WAL log from disk
        └─ Log file survived!

Step 6: Recovery process
        ├─ Replay: "UPDATE seats = 0"
        ├─ Data restored to database
        └─ RESTORED ✅
```

### Without WAL (Risky) ❌

```
Step 1: UPDATE seats = 0 (RAM only, volatile)
Step 2: ⚡ POWER CRASH (before disk write)
Step 3: Reboot → No log on disk → Data LOST ❌

Result: Money/data permanently gone
```

### With WAL (Safe) ✅

```
Step 1: UPDATE seats = 0 (RAM)
Step 2: Write to WAL log (DISK) ✅
Step 3: ⚡ POWER CRASH (doesn't matter now)
Step 4: Reboot → Read WAL log from disk
Step 5: Replay from log → Data RESTORED ✅

Result: No data loss
```

### Memory Hierarchy (Speed vs Permanence)

```
CPU Registers    → Fastest, but lost on crash
        ↓
L1/L2/L3 Cache   → Fast, but lost on crash
        ↓
RAM (volatile)   → Medium speed, lost on crash
        ↓
SSD/HDD (disk)   → Slower, but PERMANENT ✅

DURABILITY = Moving from RAM to disk
```

### Key Takeaway

**Durability = "Committed data on disk survives anything—WAL logs guarantee recovery."**

---

## ACID Quick Reference

### All Four Properties at a Glance

| Property | Definition | Ensures | Example |
|----------|-----------|---------|---------|
| **A**tomicity | All or nothing | Complete or rollback | Money transfer completes fully or not at all |
| **C**onsistency | Valid state → valid state | Rules enforced | Total money stays constant |
| **I**solation | No interference | Concurrent safety | A & B don't double-book same seat |
| **D**urability | Permanent storage | Crash safety | Power loss recovery via WAL logs |

### Quick Summary

```
A = Atomicity:    All-or-nothing commitment
C = Consistency:  Valid state to valid state
I = Isolation:    No interference between transactions (locks)
D = Durability:   Permanent disk storage (WAL logs)
```

---

## Code Examples

### PostgreSQL: Setting Isolation Levels

```sql
-- For the entire session
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- For a specific transaction
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  SELECT * FROM seats WHERE id = 1 FOR UPDATE;
  UPDATE seats SET available = available - 1 WHERE id = 1;
  INSERT INTO bookings (passenger_id, seat_id) VALUES (101, 1);
COMMIT;
```

### MySQL: Isolation Levels

```sql
-- View current isolation level
SELECT @@transaction_isolation;

-- Set for session
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Explicit locking
START TRANSACTION;
  SELECT * FROM seats WHERE id = 1 FOR UPDATE;  -- Lock row
  UPDATE seats SET available = available - 1 WHERE id = 1;
COMMIT;
```

### Python + SQLAlchemy

```python
from sqlalchemy import create_engine, text

# PostgreSQL with SERIALIZABLE isolation
engine = create_engine(
    "postgresql://user:password@localhost/airline",
    isolation_level="SERIALIZABLE"
)

# Usage
with engine.begin() as conn:
    # Booking logic
    result = conn.execute(text(
        "SELECT available FROM seats WHERE id = :seat_id"
    ), {"seat_id": 1})
    
    seats = result.scalar()
    
    if seats > 0:
        conn.execute(text(
            "UPDATE seats SET available = available - 1 WHERE id = :seat_id"
        ), {"seat_id": 1})
        
        conn.execute(text(
            "INSERT INTO bookings (passenger_id, seat_id) VALUES (:pid, :sid)"
        ), {"pid": passenger_id, "sid": 1})
        
    # Auto-commit on successful exit
```

### Java (JDBC)

```java
Connection conn = DriverManager.getConnection(dbURL, user, password);

// Set isolation level
conn.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE);
conn.setAutoCommit(false);

try {
    // Booking query
    String query = "SELECT available FROM seats WHERE id = 1";
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery(query);
    
    if (rs.next()) {
        int seats = rs.getInt("available");
        
        if (seats > 0) {
            // Update seats
            stmt.executeUpdate(
                "UPDATE seats SET available = " + (seats - 1) + " WHERE id = 1"
            );
            
            // Insert booking
            stmt.executeUpdate(
                "INSERT INTO bookings (passenger_id, seat_id) VALUES (101, 1)"
            );
            
            // Commit
            conn.commit();
            System.out.println("Booking successful!");
        } else {
            System.out.println("No seats available");
            conn.rollback();
        }
    }
} catch (SQLException e) {
    try {
        conn.rollback();
    } catch (SQLException ex) {
        ex.printStackTrace();
    }
    e.printStackTrace();
}
```

---

## Key Takeaways

### Exam/Viva Answers

**Q: What is ACID?**  
**A:** ACID (Atomicity, Consistency, Isolation, Durability) are four properties that guarantee reliable database transactions, ensuring data integrity even during failures.

**Q: Explain Atomicity with an example.**  
**A:** Atomicity means "all-or-nothing." In a money transfer (A→B), either both debit and credit happen, or neither does. If a crash occurs, the transaction rolls back completely.

**Q: What is Isolation and why is it needed?**  
**A:** Isolation prevents concurrent transactions from interfering. Without it, two users might book the same seat (dirty read). Locking mechanisms ensure each transaction runs independently.

**Q: What are the four isolation levels?**  
**A:** 
1. READ UNCOMMITTED (risky, fast)
2. READ COMMITTED (default, balanced)
3. REPEATABLE READ (safe reads, MySQL default)
4. SERIALIZABLE (safest, slowest)

**Q: How does WAL ensure Durability?**  
**A:** Write-Ahead Logging (WAL) writes transaction logs to disk BEFORE committing. If a crash occurs, the system replays logs from disk during recovery, restoring all committed transactions.

**Q: What's the difference between Consistency and Isolation?**  
**A:** 
- **Consistency:** Database enforces rules (constraints, no negative seats)
- **Isolation:** Concurrent transactions don't interfere (via locks)

---

## Common Problems and Solutions

### Dirty Read
**Problem:** Reading uncommitted data  
**Solution:** Use READ COMMITTED or higher

### Lost Update
**Problem:** One transaction overwrites another  
**Solution:** Use REPEATABLE READ or higher

### Non-Repeatable Read
**Problem:** Same query returns different values  
**Solution:** Use REPEATABLE READ or higher

### Phantom Read
**Problem:** New rows appear mid-transaction  
**Solution:** Use SERIALIZABLE only

---

## Decision Tree: Which Isolation Level?

```
Is data critical (banking, trading)?
├─ YES → SERIALIZABLE (safest)
└─ NO  → Need repeatable reads within transaction?
         ├─ YES → REPEATABLE READ
         └─ NO  → READ COMMITTED (default, balanced)
```

---

## Summary

**ACID Properties ensure:**

✅ **Atomicity** - Complete or nothing  
✅ **Consistency** - Valid states only  
✅ **Isolation** - No concurrent conflicts  
✅ **Durability** - Permanent storage  

**Together, they guarantee:**
- Data integrity
- Crash safety
- Concurrent reliability
- Transaction consistency

---

## References

- ACID Properties in Relational Databases
- Transaction Isolation Levels (SQL Standard)
- Concurrency Control Mechanisms
- Write-Ahead Logging (WAL)
- Database Management Systems (DBMS)

---

## Author Notes

This guide is designed for:
- 📚 Database course students
- 🎓 Viva exam preparation
- 💼 Job interview preparation
- 🔧 Production system design

**Format:** Lecture-based study guide with examples and code snippets

**Last Updated:** 2026

---

**Ready to learn more?** Check out related topics:
- Transactions and ACID
- Concurrency Control
- Locking Mechanisms
- Database Optimization

**Questions?** Open an issue or discuss with your instructor!

---

*This guide is derived from database management lectures and includes practical examples for real-world understanding.*
