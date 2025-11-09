# C-Suite MI Dashboard - Efficiency Improvement Report

## Executive Summary
This report identifies several efficiency improvement opportunities in the C-Suite MI Dashboard codebase. The analysis focuses on DataFrame operations, API client patterns, and data processing inefficiencies that could impact performance, especially with larger datasets.

## Identified Inefficiencies

### 1. **Unnecessary DataFrame Copies in KPI Functions** (HIGH IMPACT)
**Location**: `src/kpis.py` - Lines 6, 14, 21
**Issue**: All KPI functions create unnecessary DataFrame copies using `.copy()` when filtering for major incidents.

```python
# Current inefficient code:
def mttr_hours(df: pd.DataFrame) -> float:
    d = df[df["is_major"]].copy()  # Unnecessary copy
    d = d[(~d["opened_at"].isna()) & (~d["resolved_at"].isna())]
    # ... rest of function

def weekly_counts(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df["is_major"]].copy()  # Unnecessary copy
    # ... rest of function

def p1_ratio(df: pd.DataFrame) -> float:
    d = df[df["is_major"]].copy()  # Unnecessary copy
    # ... rest of function
```

**Impact**: Creates unnecessary memory overhead and CPU cycles for DataFrame copying
**Solution**: Remove `.copy()` calls and work directly with filtered views

### 2. **Inefficient DataFrame Shape Access** (MEDIUM IMPACT)
**Location**: `app/main.py` - Line 93
**Issue**: Using `.shape[0]` on filtered DataFrame instead of more efficient counting methods.

```python
# Current code:
col2.metric("MIs (YTD)", int(df[df.get("is_major", True)].shape[0]))
```

**Impact**: Less readable and potentially less efficient than direct counting
**Solution**: Use `.sum()` on boolean mask or `.count()` method

### 3. **Inefficient Column Renaming Pattern** (MEDIUM IMPACT)
**Location**: `app/main.py` - Lines 113-115
**Issue**: Sequential DataFrame reassignment in loop instead of batch renaming.

```python
# Current inefficient code:
for old_col, new_col in column_mapping.items():
    if old_col in df.columns:
        df = df.rename(columns={old_col: new_col})  # Creates new DataFrame each iteration
```

**Impact**: Creates multiple intermediate DataFrame objects
**Solution**: Build rename dictionary and apply once

### 4. **Duplicate Datetime Parsing Logic** (LOW-MEDIUM IMPACT)
**Location**: `src/transforms.py` (Line 33) and `app/main.py` (Line 128)
**Issue**: Similar datetime parsing logic exists in two places with slight differences.

```python
# In transforms.py:
df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S", errors="coerce", utc=True)

# In main.py:
df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S", errors="coerce")
```

**Impact**: Code duplication and potential inconsistency (UTC handling differs)
**Solution**: Centralize datetime parsing logic

### 5. **Redundant Environment Variable Loading** (LOW IMPACT)
**Location**: `src/snow_client.py` - Multiple functions call `_load_env()`
**Issue**: Environment variables are loaded multiple times unnecessarily.

**Impact**: Minor performance overhead from repeated dotenv loading
**Solution**: Load environment variables once at module level or cache results

## Recommended Implementation Priority

1. **HIGH PRIORITY**: Remove unnecessary `.copy()` calls in KPI functions
   - **Estimated Impact**: 20-40% memory reduction for KPI calculations
   - **Risk**: Low (read-only operations don't need copies)
   - **Effort**: Low (simple removal of `.copy()` calls)

2. **MEDIUM PRIORITY**: Fix inefficient column renaming pattern
   - **Estimated Impact**: Reduced memory churn during CSV processing
   - **Risk**: Low (straightforward refactor)
   - **Effort**: Low

3. **MEDIUM PRIORITY**: Optimize DataFrame counting operations
   - **Estimated Impact**: Minor performance improvement, better readability
   - **Risk**: Very Low
   - **Effort**: Very Low

4. **LOW PRIORITY**: Consolidate datetime parsing logic
   - **Estimated Impact**: Better maintainability, consistency
   - **Risk**: Medium (need to ensure UTC handling is correct)
   - **Effort**: Medium

## Performance Testing Recommendations

- Test with larger datasets (1000+ incidents) to measure actual performance impact
- Profile memory usage before and after optimizations
- Benchmark KPI calculation times with and without `.copy()` calls

## Conclusion

The most impactful improvement is removing unnecessary DataFrame copies in KPI functions. This change is low-risk and provides immediate memory and performance benefits, especially important for executive dashboards that need to be responsive.
