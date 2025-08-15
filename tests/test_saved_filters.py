from src.snow_client import get_complex_manual_query, get_saved_filter_query


def test_saved_filter_query():
    """Test that saved filter queries are properly formatted"""

    # Test the PYTHON: MAJOR IM saved filter
    saved_query = get_saved_filter_query("PYTHON: MAJOR IM")

    # Verify the query structure
    assert "priorityIN1,2" in saved_query, "Priority filter missing"
    assert "location.u_region=EMEA" in saved_query, "EMEA region filter missing"
    assert "u_resolvedBETWEEN" in saved_query, "Resolved date filter missing"
    assert "javascript:gs.dateGenerate" in saved_query, "Date generation function missing"
    assert "gs.endOfToday()" in saved_query, "End date function missing"

    print("✅ Saved filter query structure validation passed")

def test_saved_filter_fallback():
    """Test that unknown saved filters fall back to default"""

    # Test unknown filter
    fallback_query = get_saved_filter_query("UNKNOWN_FILTER")

    # Should fall back to default
    assert fallback_query == "priorityIN1,2", "Should fall back to default query"

    print("✅ Saved filter fallback validation passed")

def test_complex_manual_query():
    """Test that complex manual query is available as fallback"""

    manual_query = get_complex_manual_query()

    # Verify the complex query structure
    assert "location.u_region=EMEA" in manual_query, "EMEA region filter missing"
    assert "priorityIN1,2" in manual_query, "Priority filter missing"
    assert "assignment_group=" in manual_query, "Assignment group filter missing"
    assert "u_resolved>=" in manual_query, "Resolved date start filter missing"
    assert "u_resolved<=" in manual_query, "Resolved date end filter missing"

    print("✅ Complex manual query validation passed")

def test_query_comparison():
    """Compare saved filter vs manual query approaches"""

    saved_query = get_saved_filter_query("PYTHON: MAJOR IM")
    manual_query = get_complex_manual_query()

    # Saved filter should be simpler
    assert len(saved_query) < len(manual_query), "Saved filter should be more concise"

    # Both should contain priority filter
    assert "priorityIN1,2" in saved_query, "Saved filter missing priority"
    assert "priorityIN1,2" in manual_query, "Manual query missing priority"

    print("✅ Query comparison validation passed")
    print(f"📊 Saved filter length: {len(saved_query)} characters")
    print(f"📊 Manual query length: {len(manual_query)} characters")

def test_saved_filter_usage():
    """Test that saved filter can be used without network calls"""

    # Test that we can get the query string
    query = get_saved_filter_query("PYTHON: MAJOR IM")

    # Verify it's a string and not empty
    assert isinstance(query, str), "Query should be a string"
    assert len(query) > 0, "Query should not be empty"

    # Test that it contains expected components
    assert "priorityIN1,2" in query, "Priority filter missing"
    assert "EMEA" in query, "EMEA region missing"

    print("✅ Saved filter usage validation passed")
    print(f"🔍 Generated query: {query[:100]}...")
